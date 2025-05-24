# coding=utf-8
import traceback

from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from loguru import logger
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from login.auth import CustomJSONWebTokenAuthentication
from myblog.models import Category, Blog
from myblog.serializers import BlogSerializer
from sers.serializers import CategorySerializer
from utils.id_util import idgen


class AuthView(APIView):
    authentication_classes = [CustomJSONWebTokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_authenticators(self):
        # GET 请求不使用认证类
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()


    def get_permissions(self):
        # 针对 GET 方法返回 AllowAny，其他方法保持默认
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()


class CategoryView(AuthView):
    throttle_classes = [AnonRateThrottle]
    cache_key = "optimized_category_list"

    def post(self, request: Request) -> Response:
        token = request.headers.get("token")
        if not token:
            return Response(data={
                "code": 401,
                "msg": "请先登录"
            }, status=status.HTTP_200_OK)
        logger.debug(f"Category creation request: {request}")
        _id = idgen.next_id()
        try:
            logger.debug(f"CategoryView generated id = {_id}")
            name = request.data["name"]
            category = {
                "id": _id,
                "name": name
            }
            with transaction.atomic():
                # 数据验证与保存
                serializer = CategorySerializer(data=category)
                serializer.is_valid(raise_exception=True)  # 自动抛出 ValidationError
                serializer.save()
                cached_data = cache.get(self.cache_key)
                if cached_data:
                    cached_data.append(serializer.data)
                    cache.set(self.cache_key, cached_data, 300)  # 缓存5分钟

                # 返回创建的资源数据
                return Response(data={
                    "code": 200,
                    "msg": "添加成功",
                    "data": serializer.data,
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Category creation failed: {str(e)}")
            return Response({
                    "code": 400,
                    "msg": str(e)
                },
                status=status.HTTP_200_OK
            )

    def get(self, request):
        """获取分类列表"""
        cached_data = cache.get(self.cache_key)
        if not cached_data:
            try:
                queryset = Category.objects.all()
                serializer = CategorySerializer(queryset, many=True)
                cached_data = serializer.data
                cache.set(self.cache_key, cached_data, 300)  # 缓存5分钟
            except Exception as e:
                logger.error(f"Critical error: {str(e)}", exc_info=True)
                return Response(
                    {"error": "服务暂时不可用"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

        return Response({
            "code": 200,
            "msg": "success",
            "data": cached_data,
        }, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            logger.info(f"Category update request: {request.data}")
            category = Category.objects.get(pk=request.data["id"])
            with transaction.atomic():
                serializer = CategorySerializer(instance=category, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(data={
                        "code": 200,
                        "msg": "修改成功",
                        "data": serializer.data,
                    }, status=status.HTTP_200_OK)
                return Response(data={
                    "code": 1002,
                    "msg": serializer.errors,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Update category failed: {str(e)}")
            return Response(data={
                "code": 400,
                "msg": "update failed"
            }, status=status.HTTP_200_OK)

    def delete(self, request, _id):
        try:
            with transaction.atomic():
                category = Category.objects.get(pk=_id)
                category_data = CategorySerializer(category).data
                category.delete()
                cached_data = cache.get(self.cache_key)
                if cached_data:
                    cached_data.remove(category_data)
                    cache.set(self.cache_key, cached_data, 300)  # 缓存5分钟
                return Response(
                    data={"code": 200, "msg": "success"},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Delete category failed: {str(e)}")
            return Response(
                data = {
                    "code": 1001,
                    "msg": "delete failed"
                }, status=status.HTTP_200_OK
            )


class BlogView(AuthView):

    def post(self, request: Request) -> Response:
        try:
            request.data.update({"id": idgen.next_id()})
            with transaction.atomic():
                article = BlogSerializer(data=request.data)
                article.is_valid(raise_exception=True)
                article.save()
                return Response(data={
                    "code": 200,
                    "msg": "添加成功",
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Blog creation failed: {str(e)}")
            return Response({
                "code": 400,
                "msg": "服务器错误"
            },status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        try:
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("pageSize", 10))
            keyword = request.query_params.get("keyword")
            category_id = int(request.query_params.get("categoryId", 0))
        except ValueError:
            return Response({"error": "Invalid page number"}, status=400)
        # 过滤数据库查询
        params = []
        where_sql_strs = []
        if category_id:
            where_sql_strs.append(" `category_id` = %s ")
            params.append(category_id)

        if keyword:
            where_sql_strs.append(" (`title` LIKE %s OR `content` LIKE %s) ")
            params.append("%" + keyword + "%")
            params.append("%" + keyword + "%")

        where_sql_str = ""
        if len(where_sql_strs) > 0:
            where_sql_str = " WHERE " + " AND ".join(where_sql_strs)
        # sqlite中使用substr(`content`, 0, 50)
        sql = '''
        SELECT `id`,`category_id`,`create_time`,`title`,substr(`content`, 1, 50) AS `content` 
        FROM `blog` ''' + where_sql_str + '''
        ORDER BY `create_time`
        DESC 
        '''
        queryset = Blog.objects.raw(sql, params)

        # 分页处理（伪代码）
        paginated_books = queryset[(page - 1) * page_size: page * page_size]
        # paginated_books = queryset
        # 返回结果
        return Response({
            "code": 200,
            "msg": "success",
            "data": {
                "results": BlogSerializer(paginated_books, many=True).data,
                "page": page,
                "page_size": page_size,
                "count": len(queryset),
            }
        })

    def put(self, request: Request) -> Response:
        article = Blog.objects.get(pk=request.data["id"])
        article_sers = BlogSerializer(instance=article, data=request.data)
        if article_sers.is_valid():
            article_sers.save()
            return Response(data={
                "code": 200,
                "msg": "更新成功",
            }, status=status.HTTP_200_OK)
        else:
            logger.error(f"Blog creation failed: {traceback.format_exc()}")
            return Response({
                "code": 400,
                "msg": "服务器错误"
            }, status=status.HTTP_200_OK)

    def delete(self, request, _id):
        try:
            blog = Blog.objects.get(pk=_id)
            blog.delete()
            return Response(
                data={"code": 200, "msg": "文章删除成功"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Delete blog failed: {str(e)}")
            return Response(
                data = {
                    "code": 1001,
                    "msg": "文章删除失败"
                }, status=status.HTTP_200_OK
            )


class BlogDetailView(APIView):
    # authentication_classes = [CustomJSONWebTokenAuthentication]

    def get(self, request: Request, _id) -> Response:
        try:
            article = Blog.objects.get(pk=_id)
            serializer = BlogSerializer(article, many=False)
            return Response(data={
                "code": 200,
                "msg": "获取成功",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Blog get failed: {str(e)}")
            return Response({
                "code": 400,
                "msg": "服务器错误"
            }, status=status.HTTP_200_OK)


class SimpleFileUpload(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            fs = FileSystemStorage(location='upload/')  # 强制指定存储目录
            file = request.FILES['file']
            filename = fs.save(file.name, file)
            print(filename)
            print(f"{fs.base_url = }\n{fs.base_location = }")
            return Response({
                'errno': 0,
                'data' :{
                    'url': request.build_absolute_uri(fs.url(filename))
                }
            }, status=201)
        except Exception as e:
            logger.error(f"SimpleFileUpload failed: {str(e)}")
            return Response({
                'errno': 1,
                "message": str(e)
            })



# class CategoryListView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = None  # 默认关闭分页，如需分页可配置
#
#     def list(self, request, *args, **kwargs):
#         try:
#             return super().list(request, *args, **kwargs)
#         except Exception as e:
#             logger.error(f"List categories error: {str(e)}")
#             return Response(
#                 {"error": "获取数据失败"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
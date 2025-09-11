from rest_framework import serializers

from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    # categoryId = serializers.IntegerField(source='category_id', allow_null=True)  # 映射字段

    class Meta:
        model = Blog
        fields = "__all__"
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False}
        }

    def to_internal_value(self, data):
        """
        在数据转换为内部表示时处理 categoryId 到 category 的映射
        """
        # 创建数据副本以避免修改原始数据
        data = data.copy()

        # 如果提供了 categoryId，将其映射到 category 字段
        if 'categoryId' in data:
            try:
                category_id = int(data['categoryId'])
                data['category_id'] = category_id
                # 不需要删除 categoryId，因为它是 write_only 的
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    'categoryId': 'A valid integer is required.'
                })

        return super().to_internal_value(data)
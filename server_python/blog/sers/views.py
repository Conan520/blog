
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from myblog.models import Category
from sers.models import Book


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=32)
#     price = serializers.IntegerField()
#     date = serializers.DateField(source='pub_date')
#
#     def create(self, validated_data):
#         new_book = Book.objects.create(**self.validated_data)
#         return new_book
#
#     def update(self, instance, validated_data):
#         Book.objects.filter(pk=instance.pk).update(**validated_data)
#         updated_book = Book.objects.get(pk=instance.pk)
#         return updated_book

class BookSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='pub_date')

    class Meta:
        model = Book
        # fields = '__all__'
        # fields = ['title', 'price', 'pub_date']
        exclude = ['pub_date']



class BookView(APIView):

    def get(self, request):
        books = Book.objects.all()
        books_serializer = BookSerializer(books, many=True)
        return Response(books_serializer.data, status=200)

    def post(self, request):

        request_serializer = BookSerializer(data=request.data)
        valid = request_serializer.is_valid()
        if valid:
            request_serializer.save()
            return Response(request_serializer.data)
        else:
            return Response(request_serializer.errors, status=400)


class BookDetailView(APIView):

    def get(self, request, id):
        book = Book.objects.get(pk=id)
        book_serializer = BookSerializer(instance=book, many=False)
        return Response(book_serializer.data, status=200)

    def put(self, request, id):
        book = Book.objects.get(pk=id)
        request_serializer = BookSerializer(instance=book, data=request.data)
        if request_serializer.is_valid():
            # Book.objects.filter(pk=id).update(**request_serializer.validated_data)
            # updated_book = Book.objects.get(pk=id)
            # request_serializer.instance = updated_book
            request_serializer.save()
            return Response(request_serializer.data)
        else:
            return Response(request_serializer.errors, status=400)

    def delete(self, request, id):
        book = Book.objects.get(id=id)
        book.delete()



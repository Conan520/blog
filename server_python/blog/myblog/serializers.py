from rest_framework import serializers

from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(source='category_id', allow_null=True)  # 映射字段

    class Meta:
        model = Blog
        fields = "__all__"
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False}
        }
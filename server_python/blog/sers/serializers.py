# Create your views here.
from rest_framework import serializers

from myblog.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False}
        }
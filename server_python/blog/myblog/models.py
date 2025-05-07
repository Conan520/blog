import time

from django.db import models
from django.utils import timezone


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'myblog'
        db_table = 'category'


class Blog(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False)
    category_id = models.BigIntegerField(blank=True, null=True)
    title = models.CharField(blank=True, null=False, max_length=200)
    content = models.TextField(blank=True, null=True)
    create_time = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'blog'

    def save(self, *args, **kwargs):
        if not self.create_time:  # 仅在创建时赋值
            self.create_time = int(time.mktime(timezone.localtime().timetuple()))
            print(f"create_time: {self.create_time}")
        super().save(*args, **kwargs)
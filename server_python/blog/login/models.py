#coding=utf-8
from django.db import models


# class Admin(models.Model):
#     account = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     token = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'admin'
#
#     def __str__(self):
#         return f"{self.__class__.__name__}(account={self.account}, password={self.password}, token={self.token})"


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        db_table = 'user_info'
from django.urls import path

from .views import BlogView

urlpatterns = [
    path('blog/search', BlogView.as_view(), name='blog-search'),
]
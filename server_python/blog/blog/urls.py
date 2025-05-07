"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path

from blog import settings
from myblog.views import CategoryView, SimpleFileUpload, BlogView, BlogDetailView
from login.views import LoginView
from sers.views import BookView, BookDetailView

# from sers import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("blog/admin/login", LoginView.as_view()),
    path("blog/add", BlogView.as_view()),
    path('blog/search', BlogView.as_view(), name='blog-search'),
    path("blog/<int:_id>", BlogView.as_view()),
    path("blog/update", BlogView.as_view()),
    path("blog/detail/<int:_id>", BlogDetailView.as_view()),
    path("upload/rich_editor_upload", SimpleFileUpload.as_view()),
    path("category/add", CategoryView.as_view()),
    path("category/list", CategoryView.as_view()),
    path("category/<int:_id>", CategoryView.as_view()),
    path("category", CategoryView.as_view()),
    path("sers/book", BookView.as_view()),
    path("sers/book/<int:id>", BookDetailView.as_view())
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
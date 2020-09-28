from django.contrib import admin
from django.urls import path

from posts.views import post_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', post_list_view),
    path('posts/', post_list_view)
]


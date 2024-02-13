from django.urls import path
from .views import create_post, post_all, post_detail

urlpatterns = [
    path('create-post/', create_post, name='create-post'),
    path('post/<int:post_id>/', post_detail, name='post-detail'),
    path('post/', post_all, name='post-all'),
]
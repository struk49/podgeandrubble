from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_posts, name='posts'),
    path('<post_id>', views.blog_detail, name='blog_detail')
]
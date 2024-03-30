from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete_review/<int:review_pk>/', views.delete_review,
         name='delete_review'),
    path('add/', views.add_produce, name='add_produce'),
]
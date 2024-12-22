from django.urls import path
from .views import create_part, list_parts, delete_part

urlpatterns = [
    path('create/', create_part, name='create_part'),
    path('list/', list_parts, name='list_parts'),
    path('delete/<int:part_id>/', delete_part, name='delete_part'),
]
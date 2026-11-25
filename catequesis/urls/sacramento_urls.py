from django.urls import path
from catequesis.views import sacramento_list, sacramento_detail

urlpatterns = [
    path('sacramentos/', sacramento_list, name='sacramento_list'),
    path('sacramentos/<int:pk>/', sacramento_detail, name='sacramento_detail'),
]
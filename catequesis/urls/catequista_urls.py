from django.urls import path
from catequesis.views import catequista_list, catequista_detail

urlpatterns = [
    path('catequistas/', catequista_list, name='catequista_list'),
    path('catequistas/<int:pk>/', catequista_detail, name='catequista_detail'),
]
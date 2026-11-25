from django.urls import path
from catequesis.views import participante_list, participante_detail

urlpatterns = [
    path('participantes/', participante_list, name='participante_list'),
    path('participantes/<int:pk>/', participante_detail, name='participante_detail'),
]
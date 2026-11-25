from django.urls import path
from catequesis.views import home

urlpatterns = [
    path('', home, name='home'),
]
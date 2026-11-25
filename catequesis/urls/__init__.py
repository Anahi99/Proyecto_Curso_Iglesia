from django.urls import path
from catequesis.views import home
from catequesis.urls.curso_urls import urlpatterns as curso_urls
from catequesis.urls.inscripcion_urls import urlpatterns as inscripcion_urls

urlpatterns = [
    path('', home, name='home'),
] + curso_urls + inscripcion_urls
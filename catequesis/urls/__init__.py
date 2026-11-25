from django.urls import path
from catequesis.views import home
from catequesis.urls.auth_urls import urlpatterns as auth_urls
from catequesis.urls.sacramento_urls import urlpatterns as sacramento_urls
from catequesis.urls.catequista_urls import urlpatterns as catequista_urls
from catequesis.urls.participante_urls import urlpatterns as participante_urls
from catequesis.urls.curso_urls import urlpatterns as curso_urls
from catequesis.urls.inscripcion_urls import urlpatterns as inscripcion_urls

urlpatterns = [
    path('', home, name='home'),
] + auth_urls + sacramento_urls + catequista_urls + participante_urls + curso_urls + inscripcion_urls
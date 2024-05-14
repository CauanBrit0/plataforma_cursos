from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('curso/<int:id>', views.curso, name="curso"),
    path('aula/<int:id>', views.aula, name = 'aula'),
]

from django.urls import path
from . import views

#deseos/

app_name = 'deseos'

urlpatterns = [
    path('', views.index, name='index'),
]
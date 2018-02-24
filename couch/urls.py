from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stream', views.stream, name='stream'),
    path('record', views.record, name='record'),
    path('new', views.new, name='new'),
]

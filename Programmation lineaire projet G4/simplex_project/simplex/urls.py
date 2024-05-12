from django.urls import path
from . import views

urlpatterns = [
    path('', views.simplex_view, name='simplex_view'),
]

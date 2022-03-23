from django.urls import path

from api import views

urlpatterns = [
    path('address', views.Address.as_view(), name='Address'),
    path('radius', views.RadiusFilter.as_view(), name='RadiusFilter'),
]

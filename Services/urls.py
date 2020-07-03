from django.urls import path

from . import views

urlpatterns = [
    path('',views.services_home_view),
]

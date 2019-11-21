from django.urls import path

from api_client import views

urlpatterns: list = [
    path('pitt', views.PittMobileView.as_view(), name='mobile_pitt'),
    path('registration', views.RegistrationMobileView.as_view(), name='mobile_registration'),
]

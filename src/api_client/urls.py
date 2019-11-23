from django.urls import path

from api_client import views

urlpatterns: list = [
    path('pitt', views.PittMobileView.as_view(), name='mobile_pitt'),

    path('users', views.UsersMobileView.as_view(), name='mobile_users'),
]

from django.urls import path

from api_client import views

urlpatterns: list = [
    path('pitt', views.PittMobileView.as_view(), name='mobile_pitt'),
    path('users', views.UsersMobileView.as_view(), name='mobile_users'),
    path('users/login', views.LoginMobileView.as_view(), name='mobile_login'),
    path('users/logout', views.LogoutMobileView.as_view(), name='mobile_logout'),
]

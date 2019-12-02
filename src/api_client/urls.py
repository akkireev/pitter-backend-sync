from django.urls import path

from api_client import views

urlpatterns: list = [
    path('users', views.UsersMobileView.as_view(), name='mobile_users'),
    path('users/<str:user_id>', views.UserMobileView.as_view(), name='mobile_user'),
    path('users/<str:user_id>/followers', views.FollowersMobileView.as_view(), name='mobile_followers'),
    path('users/<str:user_id>/followers/<str:following_user_id>',
         views.FollowerMobileView.as_view(), name='mobile_subscription'),
    path('users/<str:user_id>/pitts', views.PittsMobileView.as_view(), name='mobile_pitts'),
    path('users/<str:user_id>/pitts/<str:pitt_id>', views.PittMobileView.as_view(), name='mobile_pitt'),
    path('account/login', views.LoginMobileView.as_view(), name='mobile_login'),
    path('account/logout', views.LogoutMobileView.as_view(), name='mobile_logout'),
]

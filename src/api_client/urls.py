from django.urls import path

from api_client import views

urlpatterns: list = [
    path('ticket', views.TicketMobileView.as_view(), name='mobile_ticket'),
    path('pitt', views.PittMobileView.as_view(), name='pitt')
]

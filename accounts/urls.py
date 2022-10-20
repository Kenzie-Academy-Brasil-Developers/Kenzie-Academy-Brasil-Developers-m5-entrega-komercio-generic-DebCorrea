from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from . import views

urlpatterns = [
    path("accounts/", views.AccountView.as_view()),
    path("login/", ObtainAuthToken.as_view()),
    path("accounts/newest/<int:num>/", views.AccountNewestView.as_view()),
    path("accounts/<pk>/", views.AccountUpdateView.as_view()),
]

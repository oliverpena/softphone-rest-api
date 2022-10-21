from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('users/', views.ListUserView.as_view(), name='users'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]

"""
User API Views.
"""
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework import generics

from user.serializers import AuthTokenSerializer, UserSerializers


class ListUserView(generics.ListAPIView):
    """List all users for authenticated users."""
    serializer_class = UserSerializers
    queryset = get_user_model().objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

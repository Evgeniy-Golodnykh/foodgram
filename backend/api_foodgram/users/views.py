from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action

from .serializers import CustomUserSerializer, FollowSerializer
from users.models import Follow

# from rest_framework import status
# from rest_framework.response import Response


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """A viewset for viewing User instances."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

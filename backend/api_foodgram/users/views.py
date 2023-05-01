from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CustomUserSerializer, FollowSerializer
from users.models import Follow

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

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        flag = Follow.objects.filter(author=author, user=request.user).exists()
        if request.method == 'DELETE' and flag:
            Follow.objects.filter(author=author, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST' and not flag:
            follow = Follow.objects.create(author=author, user=request.user)
            serializer = FollowSerializer(follow)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

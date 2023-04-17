from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ChangePasswordSerializer, LoginSerializer, SignUpSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """A viewset to read and edit User instances."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class SignUpView(generics.CreateAPIView):
    """User registration view."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class LoginView(TokenObtainPairView):
    """User login view."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


class MeView(generics.RetrieveAPIView):
    """A view to read own profile."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        resp = UserSerializer(request.user, context=request).data
        return Response(resp, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """A view to change User password."""

    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    http_method_names = ('put')

    def update(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(
            serializer.validated_data['current_password']
        ):
            return Response(
                'Current password does not match.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(
            'Password updated successfully.', status=status.HTTP_200_OK
        )

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def create_follow(
        user_model, follow_model, instance_serializer, request, id
):
    author = get_object_or_404(user_model, id=id)
    if author == request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    instance = follow_model.objects.filter(
        author=author,
        user=request.user
    ).exists()
    if not instance:
        follow = follow_model.objects.create(
            author=author,
            user=request.user
        )
        serializer = instance_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def destroy_follow(user_model, follow_model, request, id):
    author = get_object_or_404(user_model, id=id)
    if author == request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    instance = follow_model.objects.filter(
        author=author,
        user=request.user
    ).exists()
    if instance:
        follow_model.objects.filter(author=author, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

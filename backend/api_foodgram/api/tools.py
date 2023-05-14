from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def create_instance(
        base_model, instance_model, instance_serializer, request, pk
):
    recipe = get_object_or_404(base_model, pk=pk)
    instance = instance_model.objects.filter(
        recipe=recipe,
        user=request.user
    ).exists()
    if not instance:
        instance_model.objects.create(
            recipe=recipe,
            user=request.user
        )
        serializer = instance_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def destroy_instance(base_model, instance_model, request, pk):
    recipe = get_object_or_404(base_model, pk=pk)
    instance = instance_model.objects.filter(
        recipe=recipe,
        user=request.user
    ).exists()
    if instance:
        instance_model.objects.filter(
            recipe=recipe,
            user=request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

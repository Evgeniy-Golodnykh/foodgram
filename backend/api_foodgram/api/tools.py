from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def create_destroy_instances(
        base_model, instance_model, instance_serializer, request, pk
):
    recipe = get_object_or_404(base_model, pk=pk)
    flag = instance_model.objects.filter(
        recipe=recipe,
        user=request.user
    ).exists()
    if request.method == 'DELETE' and flag:
        instance_model.objects.filter(
            recipe=recipe,
            user=request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'POST' and not flag:
        instance_model.objects.create(
            recipe=recipe,
            user=request.user
        )
        serializer = instance_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

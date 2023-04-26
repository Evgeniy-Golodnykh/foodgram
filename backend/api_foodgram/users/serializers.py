from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """A serializer to read User instances."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(author=obj, user=request.user).exists()


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """A serializer to create User instances."""

    password = serializers.CharField(
        write_only=True,
        max_length=150,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Please choose another username')
        if len(value) > 150:
            raise serializers.ValidationError(
                'Username must be less than 150 characters'
            )
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FollowSerializer(serializers.ModelSerializer):
    """A serializer to read Followers."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    # recipes =
    # recipes_count =

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            # 'recipes',
            # 'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(author=obj.author, user=obj.user).exists()


class CurrentAuthorDefault:
    """A function to receive Author ID from path parameter."""

    requires_context = True

    def __call__(self, serializer_field):
        context = serializer_field.context['request'].parser_context
        return get_object_or_404(
            User, id=context.get('kwargs').get('user_id'))


class CreateDestroyFollowSerializer(serializers.ModelSerializer):
    """A serializer to create/destroy Follow instances."""

    author = serializers.HiddenField(default=CurrentAuthorDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowSerializer(instance, context=context).data

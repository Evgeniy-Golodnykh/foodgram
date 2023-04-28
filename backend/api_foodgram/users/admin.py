from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Custom User admin panel."""

    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
admin.site.register(Follow)

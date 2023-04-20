from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('', include(router.urls)),
]

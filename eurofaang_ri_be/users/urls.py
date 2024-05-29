from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from .views import TnaProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tna', TnaProjectViewSet, basename='tna')

app_name = 'tna'
urlpatterns = [
    # path('list/', TnaListAV.as_view(), name='tna-list'),
    # path('<int:pk>/', TnaDetailAV.as_view(), name='tna-detail'),

    path('', include(router.urls)),
]
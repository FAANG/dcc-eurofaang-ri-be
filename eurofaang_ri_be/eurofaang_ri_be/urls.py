from django.urls import path, re_path, include, reverse_lazy
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserLogIn
from tna.views import TnaProjectViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tna', TnaProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-user-login/', UserLogIn.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
    path('tna/', include('tna.urls')),
    path('users/', include('users.urls')),
]

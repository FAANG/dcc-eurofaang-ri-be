from django.urls import path
from .views import UserDetails, UserListAV

app_name = 'users'
urlpatterns = [
    path('list/', UserListAV.as_view(), name='users-list'),
    path('<int:pk>/', UserDetails.as_view(), name='user-detail'),
]

from django.urls import path
from .views import TnaListAV, TnaDetailAV

app_name = 'tna'
urlpatterns = [
    path('list/', TnaListAV.as_view(), name='tna-list'),
    path('<int:pk>/', TnaDetailAV.as_view(), name='tna-detail'),
]

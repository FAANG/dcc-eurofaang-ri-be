from django.urls import path
from .views import TnaListAV, TnaDetailAV

app_name = 'tna'
urlpatterns = [
    # path('list/', views.tna_list, name='tna_list'),
    # path('<int:pk>/', views.tna_project_details, name='tna-detail'),
    path('list/', TnaListAV.as_view(), name='tna-list'),
    path('<int:pk>/', TnaDetailAV.as_view(), name='tna-detail'),
]

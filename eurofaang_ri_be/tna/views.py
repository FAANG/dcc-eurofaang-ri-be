from .models import TnaProject
from .serializers import TnaProjectSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly, SubmittedReadOnly

class TnaProjectViewSet(viewsets.ModelViewSet):
    queryset = TnaProject.objects.all()
    serializer_class = TnaProjectSerializer
    permission_classes = [IsOwnerOrReadOnly, SubmittedReadOnly]
    # throttle_classes = [AnonRateThrottle]

    def perform_create(self, serializer):
        serializer.save(tna_owner=self.request.user)

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import TnaProject
from .serializers import TnaProjectSerializer
from rest_framework import viewsets, status
from .permissions import IsOwnerOrReadOnly, SubmittedReadOnly

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TnaPagination


class TnaProjectViewSet(viewsets.ModelViewSet):
    serializer_class = TnaProjectSerializer
    permission_classes = [IsOwnerOrReadOnly, SubmittedReadOnly]

    pagination_class = TnaPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('principal_investigator__username', 'record_status')
    search_fields = ['project_title', 'context', 'objective', 'impact', 'state_art', 'scientific_question_hypothesis',
                     'approach', 'strategy', 'research_installation_1', 'research_installation_2',
                     'research_installation_3']
    ordering_fields = ['project_title', 'principal_investigator__first_name', 'principal_investigator__last_name',
                        'associated_application', 'id']

    def get_queryset(self):
        user = self.request.user
        user_filter = Q(tna_owner=user) | Q(additional_participants=user)
        return TnaProject.objects.filter(user_filter).distinct()

    def retrieve(self, request, *args, **kwargs):
        project = get_object_or_404(TnaProject, pk=kwargs['pk'])

        queryset = self.get_queryset()
        if not queryset.filter(pk=kwargs['pk']).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.check_object_permissions(request, project)
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(tna_owner=self.request.user)

    def paginate_queryset(self, queryset):
        if 'pagination' in self.request.query_params and self.request.query_params['pagination'] == 'false':
            return None
        return super().paginate_queryset(queryset)

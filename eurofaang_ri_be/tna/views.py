from .models import TnaProject
from .serializers import TnaProjectSerializer
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly, SubmittedReadOnly

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TnaPagination


class TnaProjectViewSet(viewsets.ModelViewSet):
    queryset = TnaProject.objects.all()
    serializer_class = TnaProjectSerializer
    permission_classes = [IsOwnerOrReadOnly, SubmittedReadOnly]

    pagination_class = TnaPagination
    # pagination_class = None
    # http://localhost:8000/api/v1/tna/?page=2
    # http://localhost:8000/api/v1/tna/?page=1&size=10

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ('principal_investigator__username', 'record_status')

    search_fields = ['project_title', 'context', 'objective', 'impact', 'state_art', 'scientific_question_hypothesis',
                     'approach', 'strategy', 'research_installation_1', 'research_installation_2',
                     'research_installation_3']

    ordering_fields = ['project_title', 'principal_investigator__first_name', 'principal_investigator__last_name',
                        'associated_application', 'id']

    # http://localhost:8000/api/v1/tna/?principal_investigator__username=kroochun&record_status=submitted
    # http://localhost:8000/api/v1/tna/?search=108
    # http://localhost:8000/api/v1/tna/?ordering=-project_title
    # http://localhost:8000/api/v1/tna/?ordering=project_title&record_status=submitted&search=Agroscope

    def perform_create(self, serializer):
        serializer.save(tna_owner=self.request.user)

    def paginate_queryset(self, queryset):
        print(self.request.query_params)
        # print(self.request.query_params['pagination'])
        if 'pagination' in self.request.query_params and self.request.query_params['pagination'] == 'false':
            return None

        return super().paginate_queryset(queryset)





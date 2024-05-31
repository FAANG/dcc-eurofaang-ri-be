from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

YES_NO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

STATUSES = (
    ('saved', 'saved'),
    ('submitted', 'submitted'),
)


class TnaProject(models.Model):
    associated_application = models.CharField(choices=YES_NO_CHOICES, default='', blank=True)
    associated_application_title = models.ForeignKey('self', on_delete=models.SET_NULL,
                                                     related_name="associated_project", null=True,
                                                     blank=True, default='')
    project_title = models.CharField(max_length=200, default='', blank=True)
    research_installation_1 = models.CharField(max_length=200, default='', blank=True)
    research_installation_2 = models.CharField(max_length=200, default='', blank=True)
    research_installation_3 = models.CharField(max_length=200, default='', blank=True)
    # rationale
    context = models.CharField(max_length=2000, default='', blank=True)
    objective = models.CharField(max_length=2000, default='', blank=True)
    impact = models.CharField(max_length=2000, default='', blank=True)
    # scientific quality
    state_art = models.CharField(max_length=2000, default='', blank=True)
    scientific_question_hypothesis = models.CharField(max_length=2000, default='', blank=True)
    approach = models.CharField(max_length=2000, default='', blank=True)
    # valorization strategy
    strategy = models.CharField(max_length=2000, default='', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    principal_investigator = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="tna_projects",
                                               default='', blank=True, null=True)
    additional_participants = models.ManyToManyField('users.User', default='', blank=True, null=True)
    tna_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects",
                                  default='', blank=True, null=True)

    record_status = models.CharField(choices=STATUSES, default='', blank=True)

    def __str__(self):
        return self.project_title

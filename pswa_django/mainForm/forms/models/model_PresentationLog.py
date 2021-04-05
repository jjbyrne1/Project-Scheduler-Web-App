from django.db import models
from .model_TeamInformation import TeamInformation


class PresentationLog(models.Model):
    teamId = models.OneToOneField(TeamInformation, verbose_name='TeamID', primary_key=True, on_delete=models.CASCADE)
    requirementsPresentation_Date = models.DateField(null=True)
    requirementsPresentation_Completed = models.BooleanField(default=False)
    designPresentation_Date = models.DateField(null=True)
    designPresentation_Completed = models.BooleanField(default=False)
    FinalPresentation_Date = models.DateField(null=True)
    FinalPresentation_Completed = models.BooleanField(default=False)


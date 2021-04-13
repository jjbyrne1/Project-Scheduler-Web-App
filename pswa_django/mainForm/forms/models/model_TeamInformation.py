from django.db import models
from .model_Advisor import Advisor
from .model_PresentationLog import PresentationLog


class TeamInformation(models.Model):
    TeamId = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    NumberOfTeamMembers = models.IntegerField(default=0)
    AdvisorId = models.ForeignKey(Advisor, on_delete=models.CASCADE, null=True, blank=True)
    Topic = models.CharField(max_length=50, null=True, blank=True)
    LogId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE)
    GithubRepoLink = models.CharField(max_length=100, null=True, blank=True)

from django.db import models
from .model_Advisor import Advisor


class TeamInformation(models.Model):
    teamId = models.IntegerField(primary_key=True, unique=True, default=1)
    numberOfTeamMembers = models.IntegerField()
    advisorId = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    topic = models.CharField(max_length = 50)
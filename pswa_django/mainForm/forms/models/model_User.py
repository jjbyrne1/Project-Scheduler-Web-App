from django.db import models
from .model_TeamInformation import TeamInformation


# Create your models here.
class User(models.Model):
    Name = models.CharField(max_length=50, null=True, blank=False)
    Eid = models.CharField(max_length=50, null=True, blank=True)
    Password = models.CharField(max_length=50, null=True, blank=True)
    Email = models.EmailField(max_length=60, blank=True)
    #teamID = TeamInformation.objects.raw('SELECT "teamId" FROM model_TeamInformation WHERE "NumberofTeamMembers" = 0 GROUP BY TI."TeamID", "NumberofTeamMembers" LIMIT 1;')
    TeamId = models.ForeignKey(TeamInformation, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

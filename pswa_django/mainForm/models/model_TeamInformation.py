from django.db import models
from .model_Advisor import Advisor
from .model_PresentationLog import PresentationLog


class TeamInformation(models.Model):
    #TeamId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE,  primary_key=True)
    TeamId = models.ForeignKey(PresentationLog, on_delete=models.CASCADE, primary_key=True, serialize=False, default=PresentationLog.get_new)
    #TeamId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE, primary_key=True, default=PresentationLog.get_new)
    #TeamId = models.OneToOneField(PresentationLog, primary_key=True, on_delete=models.CASCADE, default=PresentationLog.get_new)
    #TeamId = models.ForeignKey(PresentationLog, on_delete=models.CASCADE, primary_key=True, unique=True) #default=PresentationLog.get_new,)
    NumberOfTeamMembers = models.IntegerField(default=1)
    AdvisorId = models.ForeignKey(Advisor, on_delete=models.CASCADE, null=True, blank=True)
    Topic = models.CharField(max_length=50, null=False, blank=False, default="N/A")
    #LogId = models.ForeignKey(PresentationLog, on_delete=models.CASCADE)
    #LogId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE, parent_link=True)
    GithubRepoLink = models.CharField(max_length=100, null=True, blank=True)

    @property
    def advisorid(self):
        return self.AdvisorId_id

    @property
    def teamid(self):
        return self.TeamId_id

    @classmethod
    def get_new(cls):
        return cls.objects.create().TeamId

    def __str__(self):
        return "Team: " + str(self.TeamId) #+ self.get_Topic

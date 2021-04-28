from django.db import models
from .model_Advisor import Advisor
from .model_PresentationLog import PresentationLog
from .model_User import User

class TeamInformation(models.Model):
    #TeamId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE,  primary_key=True)
    TeamId = models.ForeignKey(PresentationLog, on_delete=models.CASCADE, primary_key=True, serialize=False)
    #TeamId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE, primary_key=True, default=PresentationLog.get_new)
    #TeamId = models.OneToOneField(PresentationLog, primary_key=True, on_delete=models.CASCADE, default=PresentationLog.get_new)
    #TeamId = models.ForeignKey(PresentationLog, on_delete=models.CASCADE, primary_key=True, unique=True) #default=PresentationLog.get_new,)
    #users = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(to=User)
    AdvisorId = models.ForeignKey(Advisor, on_delete=models.CASCADE, null=True, blank=True)
    Topic = models.CharField(max_length=50, null=False, blank=False, default="?")
    #LogId = models.ForeignKey(PresentationLog, on_delete=models.CASCADE)
    #LogId = models.OneToOneField(PresentationLog, on_delete=models.CASCADE, parent_link=True)
    GithubRepoLink = models.CharField(max_length=100, null=True, blank=True)

    @property
    def advisorid(self):
        return self.AdvisorId_id

    @property
    def teamid(self):
        return self.TeamId_id

    @property
    def listOfTeamMembers(self):
        string = ""
        b = True
        userQuarrySet = TeamInformation.objects.get(TeamId=self.TeamId)
        for user in userQuarrySet.users.all():
            if b:
                string = string + str(user)
                b = False
            else:
                string = string + "; " + str(user)
        return string

    def __str__(self):
        return "Team: " + str(self.teamid) + "| Team Members: " + self.listOfTeamMembers

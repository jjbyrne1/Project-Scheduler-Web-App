from django.db import models
from .model_advisors import Advisor
from .model_students import Student


# TeamInformation Model
class TeamInformation(models.Model):
    TeamID = models.AutoField(primary_key=True, serialize=False)
    Students = models.ManyToManyField(Student, null=True, blank=True)
    AdvisorID = models.ForeignKey(Advisor, on_delete=models.SET_NULL, null=True, blank=True)
    Topic = models.CharField(max_length=50, null=True, blank=True)
    Location = models.CharField(max_length=100, null=True, blank=True)

    @property
    def listofTeamMembers(self):
        string = ""
        b = True
        userQuerySet = TeamInformation.objects.get(TeamID=self.teamid)
        for user in userQuerySet.Students.order_by('FullName'):
            if b:
                string = string + str(user)
                b = False
            else:
                string = string + "; " + str(user)
        return string

    @property
    def advisorid(self):
        return self.AdvisorID_id

    @property
    def teamid(self):
        return str(self.TeamID)

    @property
    def topic(self):
        return self.Topic

    @property
    def location(self):
        return self.Location

    def __str__(self):
        return f"Team: {self.teamid} | Team Members: {self.listofTeamMembers}"# | Topic: {self.Topic}"

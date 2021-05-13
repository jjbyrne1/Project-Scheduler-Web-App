from django.core.validators import validate_image_file_extension
from django.db import models
from .model_advisors import Advisor
from .model_students import Student
from .model_presentation_logs import PresentationLog


# TeamInformation Model
class TeamInformation(models.Model):
    TeamID = models.OneToOneField(to=PresentationLog, on_delete=models.CASCADE)
    Students = models.ManyToManyField(Student, null=True, blank=True)
    AdvisorID = models.ForeignKey(Advisor, on_delete=models.SET_NULL, null=True, blank=True)
    Topic = models.CharField(max_length=50, null=True, blank=True)
    """ Validator makes sure that the file content type is an image extension"""
    ProjectAdvertisement = models.FileField(upload_to='advertisements/', validators=[validate_image_file_extension], null=True, blank=True)
    RepoLink = models.URLField(max_length=100, null=True, blank=True)

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
        return str(self.TeamID_id)

    @property
    def topic(self):
        return self.Topic

    @property
    def location(self):
        return self.Location

    def __str__(self):
        return f"Team: {self.teamid} | Team Members: {self.listofTeamMembers}"

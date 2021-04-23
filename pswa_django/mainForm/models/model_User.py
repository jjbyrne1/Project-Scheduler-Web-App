from django.db import models
from .model_TeamInformation import TeamInformation


# Create your models here.
class User(models.Model):
    FirstName = models.CharField(max_length=50, null=False, blank=False, unique=True)
    LastName = models.CharField(max_length=50, null=False, blank=False, unique=True)
    Eid = models.CharField(max_length=50, null=True, blank=True)
    Password = models.CharField(max_length=50, null=True, blank=True)
    Email = models.EmailField(max_length=60, blank=True)
    TeamId = models.ForeignKey(TeamInformation, on_delete=models.CASCADE, primary_key=True, verbose_name="TeamId")
    is_admin = models.BooleanField(default=False)

    @property
    def teamid(self):
        return self.TeamId_id

    def __str__(self):
        return self.LastName + ", " + self.FirstName

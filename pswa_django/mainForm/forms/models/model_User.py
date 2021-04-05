from django.db import models
from .model_TeamInformation import TeamInformation


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False)
    eid = models.CharField(max_length=50, null=True, blank=False)
    password = models.CharField(max_length=50, null=True, blank=False)
    email = models.EmailField(max_length=60)
    teamID = models.ForeignKey(TeamInformation, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

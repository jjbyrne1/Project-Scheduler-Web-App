from django.db import models


class MyModel(models.Model):
    fullname = models.CharField(max_length=200)
    mobile_number = models.IntegerField()


class UpdateTeamInformation(models.Model):
    name = models.CharField(max_length=200)
    advisor = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)

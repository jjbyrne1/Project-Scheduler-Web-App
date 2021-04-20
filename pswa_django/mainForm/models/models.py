from django.db import models


class MyModel(models.Model):
    fullname = models.CharField(max_length=200)
    mobile_number = models.IntegerField()


class UpdateTeamInformation(models.Model):
    #teamId = run querry to get team Id after inputting student name
    #numberOfTeamMembers = run querry to get number of team members from student name to get team id
    #advisorId = run querry to get advisor from student name to get team id
    #githubRepoLink = use name to get team id and return their repo link
    name = models.CharField(max_length=200)
    advisor = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
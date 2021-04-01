from django.db import models


class Advisor(models.Model):
    advisorId = models.IntegerField(unique=True, primary_key=True, default=1)
    advisorName = models.CharField(max_length=25, unique=True)


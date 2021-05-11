from django.db import models


# Advisor Model
class Advisor(models.Model):
    AdvisorID = models.AutoField(primary_key=True, serialize=False)
    FullName = models.CharField(max_length=50, unique=True)

    @property
    def advisorid(self):
        return self.AdvisorID

    @property
    def firstname(self):
        fields = self.FullName.split(',')
        return fields[1]

    @property
    def lastname(self):
        fields = self.FullName.split(',')
        return fields[0]

    def __str__(self):
        return self.FullName

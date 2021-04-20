from django.db import models


class PresentationLog(models.Model):
    TeamId = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    RequirementsPresentation_Date = models.DateField(null=True, blank=True)
    RequirementsPresentation_Completed = models.BooleanField(default=False)
    DesignPresentation_Date = models.DateField(null=True, blank=True)
    DesignPresentation_Completed = models.BooleanField(default=False)
    FinalPresentation_Date = models.DateField(null=True, blank=True)
    FinalPresentation_Completed = models.BooleanField(default=False)

    @property
    def logid(self):
        return self.TeamId

    @classmethod
    def get_new(cls):
        return cls.objects.create().TeamId

    def __str__(self):
        return "LogID: " + str(self.TeamId)

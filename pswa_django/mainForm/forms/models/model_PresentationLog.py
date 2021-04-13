from django.db import models


class PresentationLog(models.Model):
    LogId = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    RequirementsPresentation_Date = models.DateField(null=True)
    RequirementsPresentation_Completed = models.BooleanField(default=False)
    DesignPresentation_Date = models.DateField(null=True)
    DesignPresentation_Completed = models.BooleanField(default=False)
    FinalPresentation_Date = models.DateField(null=True)
    FinalPresentation_Completed = models.BooleanField(default=False)


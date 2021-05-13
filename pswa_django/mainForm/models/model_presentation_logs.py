from django.db import models


# Presentation Log Model
class PresentationLog(models.Model):
    TeamID = models.AutoField(primary_key=True, serialize=False)
    RequirementsPresentation_Date = models.DateField(null=True, blank=True)
    RequirementsPresentation_Completed = models.BooleanField(default=False)
    DesignPresentation_Date = models.DateField(null=True, blank=True)
    DesignPresentation_Completed = models.BooleanField(default=False)
    FinalPresentation_Date = models.DateTimeField(null=True, blank=True)
    FinalPresentation_Completed = models.BooleanField(default=False)
    FinalPresentation_Location = models.CharField(max_length=100, null=True, blank=True)

    @property
    def formatted_requirements_presentation_date(self):
        return self.RequirementsPresentation_Date.__format__('%m/%d/%y')

    @property
    def formatted_design_presentation_date(self):
        return self.DesignPresentation_Date.__format__('%m/%d/%y')

    @property
    def formatted_final_presentation_date(self):
        return self.FinalPresentation_Date.__format__('%m/%d/%y %I:%M %p')

    @property
    def logid(self):
        return str(self.TeamID)

    def __str__(self):
        return f"Presentation Log for Team { str(self.TeamID) }"

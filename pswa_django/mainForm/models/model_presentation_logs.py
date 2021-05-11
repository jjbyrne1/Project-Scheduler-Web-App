from django.db import models
from .model_team_informations import TeamInformation


# Presentation Log Model
class PresentationLog(models.Model):
    TeamID = models.OneToOneField(to=TeamInformation, on_delete=models.CASCADE)
    RequirementsPresentation_Date = models.DateField(null=True, blank=True)
    RequirementsPresentation_Completed = models.BooleanField(default=False)
    DesignPresentation_Date = models.DateField(null=True, blank=True)
    DesignPresentation_Completed = models.BooleanField(default=False)
    FinalPresentation_Date = models.DateTimeField(null=True, blank=True)
    FinalPresentation_Completed = models.BooleanField(default=False)

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
        return str(self.TeamID_id)

    def __str__(self):
        return f"Presentation Log for { str(self.TeamID) }"


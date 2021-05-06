from django.test import TestCase
import datetime
from mainForm.models.model_presentation_logs import PresentationLog
from mainForm.models.model_team_informations import TeamInformation


class PresentaitonLogTestCase(TestCase):
    def setUp(self):
        self.teaminformation = TeamInformation.objects.create()
        self.log = PresentationLog.objects.create(TeamID=self.teaminformation)

    def test_presentation_log_string_representation(self):
        self.assertEqual(str(self.log), f"Presentation Log for { str(self.teaminformation) }")

    def test_presentation_log_correct_formatted_requirements_presentation_date(self):
        date = datetime.date.today()
        self.log.RequirementsPresentation_Date = date
        self.assertEqual(self.log.formatted_requirements_presentation_date,date.__format__('%m/%d/%y'))

    def test_presentation_log_correct_formatted_design_presentation_date(self):
        date = datetime.date.today()
        self.log.DesignPresentation_Date = date
        self.assertEqual(self.log.formatted_design_presentation_date, date.__format__('%m/%d/%y'))

    def test_presentation_log_correct_formatted_final_presentation_date(self):
        date = datetime.date.today()
        self.log.FinalPresentation_Date = date
        self.assertEqual(self.log.formatted_final_presentation_date, date.__format__('%m/%d/%y %I:%M %p'))

from django.test import TestCase
from mainForm.models.model_advisors import Advisor


class AdvisorTestCase(TestCase):
    def setUp(self):
        self.name = "Advisor,A"
        self.advisor = Advisor.objects.create(Name=self.name)

    def test_advisor_string_representation(self):
        self.assertEqual(str(self.advisor), self.name)

    def test_advisor_property_id(self):
        name = "Advisor,B"
        advisor = Advisor.objects.create(Name=name)
        self.assertEqual(advisor.advisorid, self.advisor.advisorid + 1)

    def test_advisor_property_first_name(self):
        self.assertEqual(self.advisor.firstname, "A")

    def test_advisor_property_last_name(self):
        self.assertEqual(self.advisor.lastname, "Advisor")



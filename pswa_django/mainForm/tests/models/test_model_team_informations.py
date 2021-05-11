from django.test import TestCase
from mainForm.models.model_team_informations import TeamInformation
from mainForm.models.model_students import Student
from mainForm.models.model_advisors import Advisor


class TeamInformationTestCase(TestCase):
    def setUp(self):
        self.teaminformation = TeamInformation.objects.create()

    def test_team_information_base_string_representation(self):
        self.assertEqual(str(self.teaminformation),
                         f"Team: {self.teaminformation.teamid} | Team Members: ")#| Topic: ")

    def test_team_information_with_students_string_representation(self):
        name1 = "Student,A"
        student1 = Student.objects.create(FullName=name1)
        name2 = "Student,B"
        student2 = Student.objects.create(FullName=name2)
        self.teaminformation.Students.add(student1, student2)
        self.assertEqual(str(self.teaminformation),
                         f"Team: {self.teaminformation.teamid} | Team Members: {self.teaminformation.listofTeamMembers}")# | Topic: {self.Topic}")

    #def test_team_information_with_topic_string_representation(self):
    #    self.assertEqual(str(self.advisor), self.name)

    #def test_team_information_full_string_representation(self):
    #    self.assertEqual(str(self.advisor), self.name)

    def test_advisor_property_teamid(self):
        teaminformation = TeamInformation.objects.create()
        self.assertEqual(teaminformation.teamid, str(int(self.teaminformation.teamid) + 1))

    def test_advisor_property_advisorid(self):
        name = "Advisor,B"
        advisor = Advisor.objects.create(FullName=name)
        teaminformation = TeamInformation.objects.create(AdvisorID=advisor)
        self.assertEqual(teaminformation.advisorid, advisor.advisorid)

    def test_advisor_property_topic(self):
        topic = "Topic A"
        teaminformation = TeamInformation.objects.create(Topic=topic)
        self.assertEqual(teaminformation.topic, topic)

    def test_advisor_property_location(self):
        location = "Room A"
        teaminformation = TeamInformation.objects.create(Location=location)
        self.assertEqual(teaminformation.location, location)

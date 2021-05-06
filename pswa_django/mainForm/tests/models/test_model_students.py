from django.test import TestCase
from mainForm.models.model_students import Student


class StudentTestCase(TestCase):
    def setUp(self):
        self.name = "Student,A"
        self.student = Student.objects.create(FullName=self.name)

    def test_student_string_representation(self):
        self.assertEqual(str(self.student), self.name)


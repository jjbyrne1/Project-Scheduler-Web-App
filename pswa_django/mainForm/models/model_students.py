from django.db import models


# Student Model
class Student(models.Model):
    FullName = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.FullName


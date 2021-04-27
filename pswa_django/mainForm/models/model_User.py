from django.db import models


# Create your models here.
class User(models.Model):
    FullName = models.CharField(max_length=50, null=False, blank=False, unique=True)
    Eid = models.CharField(max_length=50, null=True, blank=True)
    Password = models.CharField(max_length=50, null=True, blank=True)
    Email = models.EmailField(max_length=60, blank=True)
    is_admin = models.BooleanField(default=False)

    @property
    def fullname(self):
        return str(self.FullName)

    @property
    def firstname(self):
        fields = self.fullname.split(' ')
        return fields[0]

    @property
    def lastname(self):
        fields = self.fullname.split(' ')
        return fields[1]

    def __str__(self):
        return self.lastname + ", " + self.firstname

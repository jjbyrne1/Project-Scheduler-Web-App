from django.db import models


class Advisor(models.Model):
    AdvisorId = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    Name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.Name


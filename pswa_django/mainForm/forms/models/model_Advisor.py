from django.db import models
from sequences import get_next_value


class Advisor(models.Model):
    AdvisorId = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    Name = models.CharField(max_length=25, unique=True)


from django.db import models

# Create your models here.

class IndustryType(models.Model):
    name = models.CharField(
        unique=True,
        verbose_name="Industry type name"
    )
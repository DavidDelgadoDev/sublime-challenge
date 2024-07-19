from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(
        unique=True,
        verbose_name="Industry name"
    )

from django.db import models
from country.models import Country
from industry.models import IndustryType
from .documents import OrganizationDocument

# Create your models here.
class Organization(models.Model):
    index = models.IntegerField(unique=True)
    organization_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=200)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=255)
    founded = models.IntegerField()
    industry = models.ForeignKey(
        IndustryType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    number_of_employees = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        organization_doc = OrganizationDocument(
            meta={'id': self.id},
            index = self.index,
            organization_id = self.organization_id,
            name = self.name,
            website = self.website,
            country = self.country.name,
            description = self.description,
            founded = self.founded,
            industry = self.industry.name,
            number_of_employees = self.number_of_employees,
        )
        organization_doc.save()
    def delete(self, *args, **kwargs):
        organization_doc = OrganizationDocument.get(id=self.id)
        organization_doc.delete()
        super().delete(*args, **kwargs)
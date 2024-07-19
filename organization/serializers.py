from rest_framework import serializers
from .models import Organization
from country.models import Country
from industry.models import IndustryType

class OrganizationSerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    industry = serializers.CharField()

    class Meta:
        model = Organization
        fields = '__all__'


    def create(self, validated_data):
        country_name = validated_data.pop('country')
        industry_name = validated_data.pop('industry')

        country, created = Country.objects.get_or_create(name=country_name)
        industry, created = IndustryType.objects.get_or_create(name=industry_name)

        organization = Organization.objects.create(country=country, industry=industry, **validated_data)
        return organization
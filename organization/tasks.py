import csv
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from .models import Organization
from country.models import Country
from industry.models import IndustryType


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_csv_file(self, file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                process_csv_row.delay(row)
    except Exception as exc:
        # Log the exception or take other actions as necessary
        print(f"Error processing CSV file: {exc}")
        try:
            # Retry the task
            raise self.retry(exc=exc)
        except MaxRetriesExceededError:
            # Handle the case where the maximum number of retries is exceeded
            print("Max retries exceeded for task")
            raise

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_csv_row(self, row):
    try:
        country, country_created = Country.objects.get_or_create(name=row['Country'])
        industry, industry_created = IndustryType.objects.get_or_create(name=row['Industry'])
        try:
            Organization.objects.create(
                    index=row['Index'],
                    organization_id=row['Organization Id'],
                    name=row['Name'],
                    website=row['Website'],
                    country=country,
                    description=row['Description'],
                    founded=int(row['Founded']),
                    industry=industry,
                    number_of_employees=int(row['Number of employees'])
                )
        except Exception as exc:
            print("Couldn't create {} due to {}".format(row['Organization Id'], exc))
    except Exception as exc:
        # Log the exception or take other actions as necessary
        print(f"Error processing row : {exc}")
        try:
            # Retry the task
            raise self.retry(exc=exc)
        except MaxRetriesExceededError:
            # Handle the case where the maximum number of retries is exceeded
            print("Max retries exceeded for task")
            raise
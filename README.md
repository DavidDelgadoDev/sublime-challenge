# sublime-challenge

## Description

This is a docker env which contain the following components:
- Django application
- Postgres DB
- ElasticSearch instance
- RabbitMQ instance

To create the local env you have to execute the following command:
`docker-compose up --build`

Then, to get the celery worker ready:
`docker-compose exec backend celery -A sublime worker --loglevel=info`

The application has the following pages:

- To upload the CSV file: `http://0.0.0.0:8000/upload_csv/`
- For a simple search (For testing purposes): `http://0.0.0.0:8000/search/?q=Ritter`

Once the system get a CSV to be processed, it enqueue a task for the CSV processing, and then, that task enqueue a new task to process each row of the CSV. 

Also, you have a couple of APIs available: 

## To call search organizations endpoint 
curl -X GET 'http://localhost:8000/search-organizations/?q=New&page=1&page_limit=5'

## To call get organization by elasticsearch id
curl -X GET 'http://localhost:8000/get-organization/<organization_id>/'
curl -X GET 'http://localhost:8000/get-organization/1/'

## To add a new organization via API

curl --location 'http://0.0.0.0:8000/add-organization/' \
--header 'Content-Type: application/json' \
--data '{
  "index":654,
  "organization_id": "12345",
  "name": "New Organization",
  "website": "https://neworg.com",
  "country": "United States",
  "description": "A new organization in the tech industry.",
  "founded": 2021,
  "industry": "Technology",
  "number_of_employees": 100
}'


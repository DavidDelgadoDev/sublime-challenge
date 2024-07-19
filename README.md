# sublime-challenge


## To execute local env using docker
docker-compose up --build

## To execute celery worker in docker
docker-compose exec backend celery -A sublime worker --loglevel=info

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
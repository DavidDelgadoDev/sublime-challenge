
from elasticsearch_dsl import Document, Text, Date, Keyword, Integer
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['http://elasticsearch:9200'])

class OrganizationDocument(Document):
    index = Integer()
    organization_id = Text()
    name = Text()
    website = Text()
    country = Text()
    description = Text()
    founded = Integer()
    industry = Text()
    number_of_employees = Integer()

    class Index:
        name = 'organizations'
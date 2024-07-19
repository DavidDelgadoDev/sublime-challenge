import csv
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadCSVForm
from .models import Organization
from .documents import OrganizationDocument
from elasticsearch_dsl import Q
from .tasks import process_csv_file
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import OrganizationSerializer
from rest_framework.response import Response
from django.core.paginator import Paginator
from elasticsearch_dsl.query import MultiMatch
from django.http import JsonResponse, Http404
from elasticsearch.exceptions import NotFoundError


def search_organizations(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    page_limit = request.GET.get('page_limit', 10)

    search = OrganizationDocument.search().query(
        MultiMatch(
            query=query,
            fields=['name', 'description', 'country', 'industry'],
            type='best_fields'
        )
    )

    response = search.execute()
    paginator = Paginator(response, page_limit)
    page_obj = paginator.get_page(page)

    results = [{
        'organization_id': hit.organization_id,
        'name': hit.name,
        'website': hit.website,
        'country': hit.country,
        'description': hit.description,
        'founded': hit.founded,
        'industry': hit.industry,
        'number_of_employees': hit.number_of_employees,
    } for hit in page_obj]

    return JsonResponse({
        'results': results,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_results': paginator.count,
    })

def search(request):
    query = request.GET.get('q')
    if query:
        # Create a search query
        search_query = Q('multi_match', query=query, fields=['name', 'industry'])
        search_results = OrganizationDocument.search().query(search_query)
        organizations = search_results.execute()
    else:
        organizations = None
    
    return render(request, 'organization/search.html', {'organizations': organizations})

def upload_csv(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.path(filename)
            
            # Queue the task to process the CSV file
            process_csv_file.delay(file_path)
            return HttpResponse("CSV file processed successfully!")
    else:
        form = UploadCSVForm()
    
    return render(request, 'organization/upload_csv.html', {'form': form})

@api_view(['POST'])
def add_organization(request):
    if request.method == 'POST':
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            return Response(OrganizationSerializer(organization).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_organization_by_id(request, id):
    try:
        organization = OrganizationDocument.get(id=id)
        result = {
            'organization_id': organization.organization_id,
            'name': organization.name,
            'website': organization.website,
            'country': organization.country,
            'description': organization.description,
            'founded': organization.founded,
            'industry': organization.industry,
            'number_of_employees': organization.number_of_employees,
        }
        return JsonResponse(result)
    except NotFoundError:
        raise Http404("Organization not found")
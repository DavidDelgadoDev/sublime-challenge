
from django.urls import path
from .views import search, upload_csv, add_organization, search_organizations, get_organization_by_id

urlpatterns = [
    path('search/', search, name='search'),
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('add-organization/', add_organization, name='add_organization'),
    path('search-organizations/', search_organizations, name='search_organizations'),
    path('get-organization/<str:id>/', get_organization_by_id, name='get_organization_by_id'),
]
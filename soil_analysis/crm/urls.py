from django.urls import path

from . import views

app_name = 'crm'
urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('company/create', views.CompanyCreateView.as_view(), name='company_create'),
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('<int:company_id>/land_list', views.LandListView.as_view(), name='land_list'),
    path('<int:company_id>/<int:land_id>/land_report_chemical', views.LandReportChemicalListView.as_view(), name='land_report_chemical')
]

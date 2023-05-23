from django.urls import path

from . import views

app_name = 'crm'
urlpatterns = [
    path('', views.CompanyList.as_view(), name='index'),
    path('<int:company_id>/land_list', views.LandList.as_view(), name='land_list'),
    path('<int:company_id>/<int:land_id>/land_report_chemical', views.LandReportChemical.as_view(), name='land_report_chemical')
]

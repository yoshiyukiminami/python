from django.urls import path

from . import views

app_name = 'chemical'
urlpatterns = [
    path('', views.CompanyList.as_view(), name='index'),
    path('<int:pk>/field_list', views.FieldList.as_view(), name='field_list'),
    path('<int:pk>/summary_report', views.SummaryReport.as_view(), name='summary_report')
]

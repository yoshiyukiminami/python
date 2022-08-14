from django.views.generic import ListView, DetailView
from .models import Companies, Fields, FieldAreaDetail


class CompanyList(ListView):
    model = Companies


class FieldList(ListView):
    model = Fields


class SummaryReport(ListView):
    model = FieldAreaDetail

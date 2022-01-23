"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render
from .models import Temperature


def index(request):
    """いわばhtmlのページ単位の構成物です"""
    context = {'latest_list': Temperature.objects.order_by('ymd')}
    print(context)
    # htmlとして返却します
    return render(request, 'test_chartjs/index.html', context)

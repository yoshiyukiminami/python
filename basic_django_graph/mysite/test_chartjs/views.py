"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render
from .models import Temperature


def index(request):
    """いわばhtmlのページ単位の構成物です"""
    context = {'latest_list': Temperature.objects.filter(ymd__range=["2021-01-10 00:00:00", "2021-01-21 00:00:00"]).order_by('ymd')}
    print(context)
    # htmlとして返却します
    return render(request, 'test_chartjs/index.html', context)

#一番最初のコマンド（filterを入れる前）
# """子供のurls.pyがこの処理を呼び出します"""
# from django.shortcuts import render
# from .models import Temperature
#
#
# def index(request):
#     """いわばhtmlのページ単位の構成物です"""
#     context = {'latest_list': Temperature.objects.order_by('ymd')}
#     # htmlとして返却します
#     return render(request, 'test_chartjs/index.html', context)

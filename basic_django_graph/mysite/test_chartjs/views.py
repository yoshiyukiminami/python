"""子供のurls.pyがこの処理を呼び出します"""
from django.shortcuts import render  # 追加！
from .models import DjangoTestTable  # 追加！
from matplotlib import pyplot as pyp


def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # 日付を降順に表示するクエリ
    ret = DjangoTestTable.objects.order_by('-pub_date')

    #  データ加工開始
    x = [1, 3, 5, 30, 55, 100]
    y = range(len(x))
    x2 = [3, 5, 10, 29, 50, 120]
    pyp.title("Matplotlib Graph", {"fontsize": 25})
    pyp.xlabel("x-number", {"fontsize": 15})
    pyp.ylabel("y-number", {"fontsize": 15})
    pyp.plot(x, y, label='graph1')
    pyp.plot(x2, y, label='graph2')
    pyp.legend()
    pyp.show()
    # データ加工終了

    context = {'latest_list': ret}
    # htmlとして返却します
    return render(request, 'test_chartjs/index.html', context)

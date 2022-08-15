from django.views.generic import ListView

from .domain import graph
from .models import Companies, Fields, FieldAreaDetail, FieldAreaSummary


class CompanyList(ListView):
    model = Companies


class FieldList(ListView):
    model = Fields


class SummaryReport(ListView):
    model = FieldAreaDetail

    def get_context_data(self, **kwargs):
        # FieldAreaDetail
        query = FieldAreaDetail.objects.get(id=1)
        x = ['EC(mS/cm)', 'NH4-N(mg/100g)', 'NO3-N(mg/100g)', '無機態窒素', 'NH4/無機態窒素']     # X軸データ
        y = [
            query.ec, query.nh4n, query.no3n, query.nh4no3, query.nh4_per_nh4no3
        ]  # Y軸データ
        chart = graph.plot_graph("窒素関連（A1をグラフ化したもの。９エリアの平均がいいかも）", x, y)  # グラフ作成

        # FieldAreaSummary
        query = FieldAreaSummary.objects.get(id=1)

        context = super().get_context_data(**kwargs)
        context['summary'] = query.comment
        context['chartA1'] = chart
        return context


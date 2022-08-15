from django.views.generic import ListView

from .domain.graph.graph_matplotlib import GraphMatplotlib
from .models import Companies, Fields, FieldAreaDetail, FieldAreaSummary


class CompanyList(ListView):
    model = Companies


class FieldList(ListView):
    model = Fields


class SummaryReport(ListView):
    model = FieldAreaDetail

    def get_context_data(self, **kwargs):
        # FieldAreaDetail
        g = GraphMatplotlib()
        fad = FieldAreaDetail.objects.get(id=1)  # TODO: 同じフィールドidで平均取る
        x = ['EC(mS/cm)', 'NH4-N(mg/100g)', 'NO3-N(mg/100g)', '無機態窒素', 'NH4/無機態窒素', ' ', '  ']
        y = [fad.ec, fad.nh4n, fad.no3n, fad.nh4no3, fad.nh4_per_nh4no3, 0, 0]
        chart1 = g.plot_graph("窒素関連（A1をグラフ化したもの。９エリアの平均がいいかも）", x, y)
        x = ['ph', 'CaO(mg/100g)', 'MgO(mg/100g)', 'K2O(mg/100g)', '塩基飽和度(%)', 'CaO/MgO', 'MgO/K2O']
        y = [fad.ph, fad.cao, fad.mgo, fad.k2o, fad.base_saturation, fad.cao_per_mgo, fad.mgo_per_k2o]
        chart2 = g.plot_graph("塩基類関連（A1をグラフ化したもの。９エリアの平均がいいかも）", x, y)
        x = ['リン吸(mg/100g)', 'P2O5(mg/100g)', ' ', '  ', '   ', '    ', '     ']
        y = [fad.phosphorus_absorption, fad.p2o5, 0, 0, 0, 0, 0]
        chart3 = g.plot_graph("リン酸関連（A1をグラフ化したもの。９エリアの平均がいいかも）", x, y)
        x = ['CEC(meq/100g)', '腐植(%)', '仮比重', ' ', '  ', '   ', '    ']
        y = [fad.cec, fad.humus, fad.bulk_density, 0, 0, 0, 0]
        chart4 = g.plot_graph("土壌ポテンシャル関連（A1をグラフ化したもの。９エリアの平均がいいかも）", x, y)

        # FieldAreaSummary
        query = FieldAreaSummary.objects.get(id=1)

        context = super().get_context_data(**kwargs)
        context['summary'] = query.comment
        context['chartA1_1'] = chart1
        context['chartA1_2'] = chart2
        context['chartA1_3'] = chart3
        context['chartA1_4'] = chart4
        return context


from django.db.models import Avg
from django.views.generic import ListView

from .domain.graph.graph_matplotlib import GraphMatplotlib
from .models import Company, Land, LandScore, LandReview


class CompanyList(ListView):
    model = Company
    template_name = "crm/company/list.html"


class LandList(ListView):
    model = Land
    template_name = "crm/land/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.kwargs['company_id']

        return context


class LandReportChemical(ListView):
    model = LandScore
    template_name = "crm/landreportchemical/list.html"

    def get_context_data(self, **kwargs):
        # LandScore
        land_score = LandScore.objects.filter(land=self.kwargs['land_id'])
        land_score_agg = land_score.aggregate(
            Avg('ec'), Avg('nh4n'), Avg('no3n'), Avg('total_nitrogen'), Avg('nh4_per_nitrogen'),
            Avg('ph'), Avg('cao'), Avg('mgo'), Avg('k2o'), Avg('base_saturation'), Avg('cao_per_mgo'),
            Avg('mgo_per_k2o'), Avg('phosphorus_absorption'), Avg('p2o5'), Avg('cec'), Avg('humus'),
            Avg('bulk_density'),
        )

        g = GraphMatplotlib()
        x = ['EC(mS/cm)', 'NH4-N(mg/100g)', 'NO3-N(mg/100g)', '無機態窒素', 'NH4/無機態窒素', ' ', '  ']
        y = [
            land_score_agg['ec__avg'],
            land_score_agg['nh4n__avg'],
            land_score_agg['no3n__avg'],
            land_score_agg['total_nitrogen__avg'],
            land_score_agg['nh4_per_nitrogen__avg'],
            0,
            0
        ]
        chart1 = g.plot_graph("窒素関連（1圃場の全エリア平均）", x, y)

        x = ['ph', 'CaO(mg/100g)', 'MgO(mg/100g)', 'K2O(mg/100g)', '塩基飽和度(%)', 'CaO/MgO', 'MgO/K2O']
        y = [
            land_score_agg['ph__avg'],
            land_score_agg['cao__avg'],
            land_score_agg['mgo__avg'],
            land_score_agg['k2o__avg'],
            land_score_agg['base_saturation__avg'],
            land_score_agg['cao_per_mgo__avg'],
            land_score_agg['mgo_per_k2o__avg']
        ]
        chart2 = g.plot_graph("塩基類関連（1圃場の全エリア平均）", x, y)

        x = ['リン吸(mg/100g)', 'P2O5(mg/100g)', ' ', '  ', '   ', '    ', '     ']
        y = [
            land_score_agg['phosphorus_absorption__avg'],
            land_score_agg['p2o5__avg'],
            0,
            0,
            0,
            0,
            0
        ]
        chart3 = g.plot_graph("リン酸関連（1圃場の全エリア平均）", x, y)

        x = ['CEC(meq/100g)', '腐植(%)', '仮比重', ' ', '  ', '   ', '    ']
        y = [
            land_score_agg['cec__avg'],
            land_score_agg['humus__avg'],
            land_score_agg['bulk_density__avg'],
            0,
            0,
            0,
            0
        ]
        chart4 = g.plot_graph("土壌ポテンシャル関連（1圃場の全エリア平均）", x, y)

        land_review = LandReview.objects.get(land=self.kwargs['land_id'])

        context = super().get_context_data(**kwargs)
        context['chart_1'] = chart1
        context['chart_2'] = chart2
        context['chart_3'] = chart3
        context['chart_4'] = chart4
        context['company_id'] = self.kwargs['company_id']
        context['land_review_comment'] = land_review.comment

        return context

from django.db import models


class Companies(models.Model):
    """
    法人名（ｎ個の圃場の持ち主）
    name 名称 e.g. (有)アグリファクトリー
    """
    name = models.CharField(max_length=256)
    remark = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)


class Clops(models.Model):
    """
    作物ひとつを１レコードという単位で収録します
    name    作物名 e.g. キャベツ、レタスなど
    """
    name = models.CharField(max_length=256)
    remark = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)


class Fields(models.Model):
    """
    法人が持つ圃場ひとつを１レコードという単位で収録します
    prefecture  都道府県    e.g. 茨城県
    location    住所       e.g. 結城郡八千代町
    latlon      緯度経度    e.g. 36.164677272061,139.86772928159
    class_clops 栽培方法  e.g. 露地、ビニールハウス
    """
    name = models.CharField(max_length=256)
    prefecture = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    latlon = models.CharField(null=True, max_length=256)
    class_clops = models.CharField(max_length=256)
    remark = models.TextField(null=True)
    companies = models.ForeignKey('Companies', on_delete=models.CASCADE)
    clops = models.ForeignKey('Clops', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)


class FieldArea(models.Model):
    """
    圃場のエリアひとつを１レコードという単位で収録します
    name        エリア名    e.g. A1
    """
    name = models.CharField(max_length=256)
    fields = models.ForeignKey('Fields', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fields", "name"],
                name="fields_name_unique"
            ),
        ]


class Period(models.Model):
    """
    時期
    name    時期の名前   e.g. 定植時
    year    西暦年      e.g. 2022
    """
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "name"],
                name="year_name_unique"
            ),
        ]


class FieldAreaSummary(models.Model):
    """
    顧客が持つ圃場ひとつのサマリーレポート用
    """
    comment = models.TextField()
    remark = models.TextField(null=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    fields = models.ForeignKey('Fields', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["period", "fields"],
                name="period_fields_unique"
            ),
        ]


class FieldAreaDetail(models.Model):
    """
    顧客が持つ圃場ひとつのエリアひとつを１レコードという単位で収録します
    圃場ひとつは９つのエリアに分かれる
    ec                      電気伝導率 e.g. 1(mS/cm)
    nh4n                    アンモニア態窒素 e.g. 1(mg/100g)
    no3n                    硝酸態窒素 e.g. 1(mg/100g)
    total_nitrogen          無機態窒素（NH4＋NO3）
    nh4_per_nitrogen        アンモニア態窒素比
    ph                      水素イオン濃度
    cao                     交換性石灰
    mgo                     交換性苦土
    k2o                     交換性加里
    base_saturation         塩基飽和度 e.g. 0.57
    cao_per_mgo             CaO/MgO e.g. 0.57
    mgo_per_k2o             MgO/K2O e.g. 0.57
    phosphorus_absorption   リン酸吸収係数
    p2o5                    可給態リン酸
    cec                     塩基置換容量
    humus                   腐植
    bulk_density            仮比重
    """
    ec = models.FloatField(null=True)
    nh4n = models.FloatField(null=True)
    no3n = models.FloatField(null=True)
    total_nitrogen = models.FloatField(null=True)
    nh4_per_nitrogen = models.FloatField(null=True)
    ph = models.FloatField(null=True)
    cao = models.FloatField(null=True)
    mgo = models.FloatField(null=True)
    k2o = models.FloatField(null=True)
    base_saturation = models.FloatField(null=True)
    cao_per_mgo = models.FloatField(null=True)
    mgo_per_k2o = models.FloatField(null=True)
    phosphorus_absorption = models.FloatField(null=True)
    p2o5 = models.FloatField(null=True)
    cec = models.FloatField(null=True)
    humus = models.FloatField(null=True)
    bulk_density = models.FloatField(null=True)
    remark = models.TextField(null=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    field_area = models.ForeignKey('FieldArea', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["period", "field_area"],
                name="period_field_area_unique"
            ),
        ]
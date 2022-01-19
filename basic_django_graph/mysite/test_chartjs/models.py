from django.db import models


# クラス名がテーブル名です
class DjangoTestTable(models.Model):
    # ここに定義したものがフィールド項目です
    month_code = models.CharField(default='XXX', max_length=3)   # Jun Feb など
    sales = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

class Temperature(models.Model):


    ymd = models.DateTimeField()
    kiatsu_riku = models.FloatField(default=0, null=True)
    kiatsu_umi = models.FloatField(default=0, null=True)
    kousuiryo = models.FloatField(default=0, null=True)
    kion_ave = models.FloatField(default=0, null=True)
    shitsudo_ave = models.FloatField(default=0, null=True)
    fuusoku = models.FloatField(default=0, null=True)
    nissyo = models.FloatField(default=0, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

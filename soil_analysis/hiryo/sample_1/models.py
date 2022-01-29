from django.db import models


class Temperature(models.Model):
    ymd = models.DateTimeField()
    pref_no = models.IntegerField(default=0)
    chiku_no = models.IntegerField(default=0)
    kiatsu_riku = models.FloatField(default=0, null=True)
    kiatsu_umi = models.FloatField(default=0, null=True)
    kousuiryo = models.FloatField(default=0, null=True)
    kion_ave = models.FloatField(default=0, null=True)
    shitsudo_ave = models.FloatField(default=0, null=True)
    fuusoku = models.FloatField(default=0, null=True)
    nissyo = models.FloatField(default=0, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

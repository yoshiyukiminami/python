from django.db import models


class Hojou(models.Model):
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)  # n個発生する可能性はあるのか？
    prefecture = models.CharField(max_length=50)  # n個発生する可能性はあるのか？
    area = models.FloatField(default=0, null=True)  # 面積ってもっとわかりやすい単語はないのか
    map_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


class Item(models.Model):
    name = models.CharField(max_length=50)
    beginning_year = models.CharField(max_length=50)  # 年度まででいいのか？
    hojou = models.ForeignKey(Hojou, verbose_name='圃場名', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

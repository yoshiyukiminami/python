from django.db import models


# クラス名がテーブル名です
class DjangoTestTable(models.Model):
    # ここに定義したものがフィールド項目です
    month_code = models.CharField(default='XXX', max_length=3) # Jun Feb など
    sales = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

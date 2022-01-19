# Generated by Django 4.0 on 2021-12-29 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_chartjs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='djangotesttable',
            name='question_text',
        ),
        migrations.AddField(
            model_name='djangotesttable',
            name='month_code',
            field=models.CharField(default='XXX', max_length=3),
        ),
        migrations.AddField(
            model_name='djangotesttable',
            name='sales',
            field=models.IntegerField(default=0),
        ),
    ]
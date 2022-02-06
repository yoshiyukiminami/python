# Generated by Django 4.0 on 2022-01-29 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ymd', models.DateTimeField()),
                ('pref_no', models.IntegerField(default=0)),
                ('chiku_no', models.IntegerField(default=0)),
                ('kiatsu_riku', models.FloatField(default=0, null=True)),
                ('kiatsu_umi', models.FloatField(default=0, null=True)),
                ('kousuiryo', models.FloatField(default=0, null=True)),
                ('kion_ave', models.FloatField(default=0, null=True)),
                ('shitsudo_ave', models.FloatField(default=0, null=True)),
                ('fuusoku', models.FloatField(default=0, null=True)),
                ('nissyo', models.FloatField(default=0, null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]

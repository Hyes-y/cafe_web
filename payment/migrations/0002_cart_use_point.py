# Generated by Django 3.2.6 on 2021-09-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='use_point',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
# Generated by Django 3.0.2 on 2020-05-26 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20200517_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
# Generated by Django 3.0.5 on 2020-04-29 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paynting', '0008_auto_20200429_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='madewith',
            name='hardware',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='madewith',
            name='software',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='masterpiece',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
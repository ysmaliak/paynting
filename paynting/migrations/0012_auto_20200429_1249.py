# Generated by Django 3.0.5 on 2020-04-29 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paynting', '0011_auto_20200429_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpiece',
            name='uploaded_by',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
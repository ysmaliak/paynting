# Generated by Django 3.0.5 on 2020-05-21 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paynting', '0018_auto_20200521_1114'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='masterpiece',
            name='paynting_ma_masterp_0cbdc6_idx',
        ),
        migrations.AddIndex(
            model_name='masterpiece',
            index=models.Index(fields=['masterpiece_name', 'uploaded_by'], name='paynting_ma_masterp_2f91b7_idx'),
        ),
    ]
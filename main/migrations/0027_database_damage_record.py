# Generated by Django 2.0 on 2019-02-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20190219_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='damage_record',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
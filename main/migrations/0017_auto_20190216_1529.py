# Generated by Django 2.0 on 2019-02-16 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20190216_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='start_date',
            field=models.DateField(default=None, null=True),
        ),
    ]

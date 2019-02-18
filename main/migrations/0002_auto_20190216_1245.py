# Generated by Django 2.0 on 2019-02-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='allotted_to',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='database',
            name='current_center',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='database',
            name='previous_allotment',
            field=models.CharField(default=None, max_length=1000000, null=True),
        ),
        migrations.AddField(
            model_name='database',
            name='previous_centers',
            field=models.CharField(default=None, max_length=1000000, null=True),
        ),
        migrations.AddField(
            model_name='database',
            name='received',
            field=models.BooleanField(default=False),
        ),
    ]
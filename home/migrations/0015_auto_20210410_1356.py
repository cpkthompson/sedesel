# Generated by Django 2.2.18 on 2021-04-10 13:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0014_auto_20210410_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myformfield',
            name='grouping',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]

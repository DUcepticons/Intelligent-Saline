# Generated by Django 3.0.3 on 2020-08-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200603_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]

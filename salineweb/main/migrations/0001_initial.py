# Generated by Django 2.2.1 on 2019-11-05 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.IntegerField(default=0)),
                ('room', models.IntegerField(default=0)),
                ('bed_no', models.IntegerField(default=0)),
                ('percentage', models.IntegerField(default=0)),
                ('device_id', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]

# Generated by Django 2.2.14 on 2020-07-25 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MapCB', '0013_auto_20200725_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='datiprezzi',
            name='zip_code',
            field=models.CharField(default='', max_length=20),
        ),
    ]
# Generated by Django 2.2.14 on 2020-07-25 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MapCB', '0006_auto_20200725_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datiprezzi',
            name='metri_quadri',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

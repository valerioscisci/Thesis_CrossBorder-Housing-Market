# Generated by Django 2.2.14 on 2020-07-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MapCB', '0004_auto_20200725_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datiprezzi',
            name='id',
        ),
        migrations.AddField(
            model_name='datiprezzi',
            name='auto_increment_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]

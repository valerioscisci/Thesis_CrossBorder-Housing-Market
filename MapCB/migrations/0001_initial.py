# Generated by Django 3.0.5 on 2020-07-24 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dati_Prezzi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('web_scraper_order', models.CharField(default='', max_length=20)),
                ('web_scraper_start_url', models.CharField(default='', max_length=300)),
                ('stato', models.CharField(default='', max_length=20)),
                ('regione', models.CharField(default='', max_length=30)),
                ('provincia', models.CharField(default='', max_length=20)),
                ('comune', models.CharField(default='', max_length=20)),
                ('indirizzo', models.CharField(default='', max_length=100)),
                ('nome_annuncio', models.CharField(default='', max_length=500)),
                ('metri_quadri', models.IntegerField()),
                ('prezzo', models.DecimalField(decimal_places=2, max_digits=9)),
                ('affitto_vendita', models.CharField(choices=[('A', 'Affitto'), ('V', 'Vendita')], max_length=1)),
                ('data_inserimento', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('fascia_prezzo', models.CharField(choices=[('B', 'Bassa'), ('M', 'Media'), ('A', 'Alta')], max_length=1)),
                ('latitudine', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitudine', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
    ]

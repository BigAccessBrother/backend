# Generated by Django 2.1.2 on 2018-12-01 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='securitystandard',
            options={'ordering': ['-date_created']},
        ),
    ]

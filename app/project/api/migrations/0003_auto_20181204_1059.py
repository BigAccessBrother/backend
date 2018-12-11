# Generated by Django 2.1.2 on 2018-12-04 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181201_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentresponse',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='api.Agent', verbose_name='agent'),
        ),
        migrations.AlterField(
            model_name='installedapp',
            name='agent_response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installed_apps', to='api.AgentResponse', verbose_name='agent_response'),
        ),
        migrations.AlterField(
            model_name='startupapp',
            name='agent_response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startup_apps', to='api.AgentResponse', verbose_name='agent_response'),
        ),
    ]
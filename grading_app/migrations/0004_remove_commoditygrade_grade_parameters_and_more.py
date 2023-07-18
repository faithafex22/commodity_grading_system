# Generated by Django 4.2.3 on 2023-07-18 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grading_app', '0003_remove_commoditygrade_grade_parameter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commoditygrade',
            name='grade_parameters',
        ),
        migrations.AddField(
            model_name='commoditygrade',
            name='grade_parameter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commodity_grade', to='grading_app.gradeparameter'),
        ),
    ]
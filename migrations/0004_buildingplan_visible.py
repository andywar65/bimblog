# Generated by Django 3.1.2 on 2020-12-29 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bimblog', '0003_delete_buildingelement'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingplan',
            name='visible',
            field=models.BooleanField(default=False, help_text='Check if plan is immediately visible', verbose_name='Visible'),
        ),
    ]

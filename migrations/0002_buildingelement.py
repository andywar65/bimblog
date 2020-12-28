# Generated by Django 3.1.2 on 2020-12-26 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bimblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of the building element', max_length=50, verbose_name='Nome')),
                ('datasheet', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
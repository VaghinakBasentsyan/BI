# Generated by Django 2.2.4 on 2019-08-25 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='data',
            field=models.FileField(upload_to=''),
        ),
    ]

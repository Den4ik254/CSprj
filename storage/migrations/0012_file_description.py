# Generated by Django 3.2.3 on 2021-05-23 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0011_remove_file_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='description',
            field=models.CharField(max_length=256, null=True, verbose_name='Описание'),
        ),
    ]

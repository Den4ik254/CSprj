# Generated by Django 3.2.3 on 2021-05-25 09:32

from django.db import migrations, models
import storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0019_auto_20210525_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=storage.models._user_directory_path, verbose_name='Путь к файлу'),
        ),
    ]

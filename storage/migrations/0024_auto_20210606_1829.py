# Generated by Django 3.2.3 on 2021-06-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0023_file_specialty'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Specialty',
            new_name='Speciality',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='specialty',
            new_name='speciality',
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='specialty',
            new_name='speciality',
        ),
        migrations.RemoveField(
            model_name='user',
            name='specialty',
        ),
        migrations.AddField(
            model_name='user',
            name='speciality',
            field=models.ManyToManyField(blank=True, to='storage.Speciality', verbose_name='Дисциплина'),
        ),
    ]

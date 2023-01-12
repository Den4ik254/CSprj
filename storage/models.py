import os

from django.contrib.auth.models import AbstractUser
from django.db import models


def _user_directory_path(instance, filename):
    """
        Функция создания адреса для сохранения файла
        return: Конечный адрес 'username/folder/file'
    """
    return f'{instance.teacher.username}/{instance.folder.title}/{filename}'


class Speciality(models.Model):
    """
        Модель дисциплин
    """
    class Meta:
        db_table = 'categories'
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['title']

    title = models.CharField(max_length=32, verbose_name='Название дисциплины', db_index=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    """
        Модель пользователей
    """
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']

    privilege = models.CharField(
        max_length=13,
        choices=[('1', 'Учащийся'), ('2', 'Преподаватель'), ('3', 'Администратор')],
        verbose_name='Привилегия',
        null=False,
        default=1
    )
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    speciality = models.ManyToManyField(Speciality, verbose_name='Дисциплина', blank=True)
    initials = models.CharField(max_length=6, verbose_name='Инициалы', null=True, blank=True)

    def get_speciality(self):
        return self.speciality.all()

    def get_transcript(self):
        temp_text = f'{self.last_name} {self.initials}' if self.last_name and self.initials else self.username
        return temp_text

    def __str__(self):
        return f'{self.username if self.last_name == "" else self.last_name} ' \
               f'{"" if self.initials is None else self.initials}'


class Folder(models.Model):
    """
        Модель папок
    """
    class Meta:
        db_table = 'folders'
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'
        ordering = ['title']

    title = models.CharField(max_length=128, verbose_name='Название папки')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    edit_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Преподаватель', null=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, verbose_name='Дисциплина', null=True)
    folder_ptr = models.IntegerField(verbose_name='Родительская папка', null=True, blank=True)

    def __str__(self):
        return self.title


class File(models.Model):
    """
        Модель файлов
    """
    class Meta:
        db_table = 'files'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['title']

    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    edit_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Преподаватель', null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, verbose_name='Папка')
    file = models.FileField(upload_to=_user_directory_path, verbose_name='Путь к файлу')
    hidden = models.BooleanField(verbose_name='Скрыт?', default=0)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, verbose_name='Дисциплина', null=True, blank=True)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def __str__(self):
        return self.title

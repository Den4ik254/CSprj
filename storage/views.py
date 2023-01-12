from typing import List

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import FileForm
from .models import Speciality, Folder, File, User


# получение содержания папки
def get_context_folder(request=None, **kwargs):
    """
        Функция получения данных о папке
    """
    context = {
        'title': Folder.objects.get(pk=kwargs['folder_id']),
        'speciality_id': kwargs['speciality_id'],
        'teacher_id': kwargs['teacher_id'],
        'folder_id': kwargs['folder_id'],
        'teachers': User.objects.filter(speciality=kwargs['speciality_id'], privilege=2),
        'folders': Folder.objects.filter(teacher=kwargs['teacher_id'], speciality=kwargs['speciality_id']),
        'sub_folders': Folder.objects.filter(folder_ptr=kwargs['folder_id']),
        'files': File.objects.filter(folder=kwargs['folder_id'], hidden=False) \
            if int(request.user.privilege) < 2 else File.objects.filter(folder=kwargs['folder_id'])
    }
    return context


# рекурсивное получение подпапок
def _get_sub_folders(sub_folders: List) -> list:
    if sub_folders is not None:
        for __sub_folder in sub_folders:
            try:
                sub_folders.append(Folder.objects.filter(folder_ptr=__sub_folder.pk).get())
            except ObjectDoesNotExist:
                return sub_folders


def _get_last_files(specs):
    __last_files = []
    for __spec in specs:
        __last_files.append(File.objects.filter(speciality=__spec.id, hidden=False).order_by('-upload_date')[:9])
    return __last_files


def index(request):
    """
        Обработчик домашнего адреса приложения
    """
    context = {
        'title': 'Главная',
        'last_specs_files':
            None if not request.user.is_authenticated else _get_last_files(request.user.get_speciality()),
    }
    if request.user.is_authenticated:
        return render(request, 'storage/index.html', context=context)
    else:
        return render(request, 'registration/login.html')


def get_data(request, **kwargs):
    """
        Функция получения донных о дисципленах, преподавателях, папках и файлах
    """
    if 'file_id' in kwargs:
        context = {
            'title': File.objects.get(pk=kwargs['file_id']),
            'speciality_id': kwargs['speciality_id'],
            'teacher_id': kwargs['teacher_id'],
            'folder_id': kwargs['folder_id'],
            'file_id': kwargs['file_id'],
            'teachers': User.objects.filter(speciality=kwargs['speciality_id'], privilege=2),
            'folders': Folder.objects.filter(teacher=kwargs['teacher_id'], speciality=kwargs['speciality_id']),
            'sub_folders': Folder.objects.filter(folder_ptr=kwargs['folder_id']),
            'files':
                File.objects.filter(folder=kwargs['folder_id'], hidden=False) \
                    if int(request.user.privilege) < 2 else File.objects.filter(folder=kwargs['folder_id']),
            'file': File.objects.get(pk=kwargs['file_id'])
        }
        return render(request, 'storage/index.html', context=context)
    elif 'folder_id' in kwargs:
        return render(request, 'storage/index.html', context=get_context_folder(request, **kwargs))
    elif 'teacher_id' in kwargs:
        context = {
            'title': User.objects.get(pk=kwargs['teacher_id']),
            'speciality_id': kwargs['speciality_id'],
            'teacher_id': kwargs['teacher_id'],
            'teachers': User.objects.filter(speciality=kwargs['speciality_id'], privilege=2),
            'folders': Folder.objects.filter(teacher=kwargs['teacher_id'], speciality=kwargs['speciality_id'])
        }

        return render(request, 'storage/index.html', context=context)
    elif 'speciality_id' in kwargs:
        context = {
            'title': Speciality.objects.get(pk=kwargs['speciality_id']),
            'speciality_id': kwargs['speciality_id'],
            'teachers': User.objects.filter(speciality=kwargs['speciality_id'], privilege=2)
        }

        return render(request, 'storage/index.html', context=context)


def create_folder(request, **kwargs):
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        context = {
            'title': 'Создание папки',
            'speciality_id': kwargs['speciality_id'],
            'teacher_id': kwargs['teacher_id'],
            'folders': Folder.objects.filter(teacher=kwargs['teacher_id'],
                                             speciality=kwargs['speciality_id'])
        }
        if request.method == 'POST':
            folder_ptr_id = request.POST.get('folders')
            folder_name = request.POST.get('folder_name')
            if folder_ptr_id != '0':
                new_folder = Folder(title=folder_name,
                                    speciality=Speciality.objects.get(pk=kwargs['speciality_id']),
                                    teacher=User.objects.get(pk=kwargs['teacher_id']),
                                    folder_ptr=folder_ptr_id)
                new_folder.save()
                return render(request, 'storage/index.html', context=get_context_folder(request=request,
                                                                                        folder_id=folder_ptr_id,
                                                                                        **kwargs))
            else:
                new_folder = Folder(title=folder_name,
                                    speciality=Speciality.objects.get(pk=kwargs['speciality_id']),
                                    teacher=User.objects.get(pk=kwargs['teacher_id']))
                new_folder.save()
                context = {
                    'title': User.objects.get(pk=kwargs['teacher_id']),
                    'speciality_id': kwargs['speciality_id'],
                    'teacher_id': kwargs['teacher_id'],
                    'teachers': User.objects.filter(speciality=kwargs['speciality_id'], privilege=2)
                }
                return render(request, 'storage/index.html', context=context)
        return render(request, 'storage/create_folder.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, 'У Вас нет доступа к данному разделу')
        return get_data(request, **kwargs)


def delete_folder(request, **kwargs):
    folder = Folder.objects.filter(pk=kwargs['folder_id'])
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        sub_folders = list(Folder.objects.filter(folder_ptr=kwargs['folder_id']))
        try:
            for sub_folder in _get_sub_folders(sub_folders):
                sub_folder.delete()
        except TypeError:
            for sub_folder in sub_folders:
                sub_folder.delete()
        messages.add_message(request, messages.SUCCESS, f'Папка {folder.get()} успешно удалена')
        folder.delete()
        return get_data(request, speciality_id=kwargs['speciality_id'], teacher_id=kwargs['teacher_id'])
    else:
        messages.add_message(request, messages.ERROR, 'У Вас нет доступа к данному действию')
        return get_data(request, **kwargs)


def rename_folder(request, **kwargs):
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        if request.method == 'POST':
            new_folder_name = request.POST.get('new_folder_name')
            folder = Folder.objects.get(pk=kwargs['folder_id'])
            folder.title = new_folder_name
            folder.save()
            messages.add_message(request, messages.SUCCESS, f'Папка успешно переименована!')
            return get_data(request, **kwargs)
        context = {
            'title': 'Переименовать папку',
            'speciality_id': kwargs['speciality_id'],
            'teacher_id': kwargs['teacher_id'],
            'folders': Folder.objects.filter(teacher=kwargs['teacher_id'],
                                             speciality=kwargs['speciality_id'])
        }
        return render(request, 'storage/rename_folder.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, 'У Вас нет доступа к данному разделу')
        return get_data(request, **kwargs)


# Files
def delete_file(request, **kwargs):
    """
        Обработчик удаления файлов с аккаунта преподавателя
    """
    file = File.objects.get(pk=kwargs['file_id'])
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        file.file.delete(save=True)
        file.delete()
        messages.add_message(request, messages.SUCCESS, f'Файл успешно удален!')
        return render(request, 'storage/index.html', context=get_context_folder(request, **kwargs))
    else:
        messages.add_message(request, messages.ERROR, f'Вы не может удалить данный файл!')
        return render(request, 'storage/index.html', context=get_context_folder(request, **kwargs))


def hide_file(request, **kwargs):
    """
        Обработчик скрытия/показа файлов с аккаунта преподавателя
    """
    file = File.objects.get(pk=kwargs['file_id'])
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        file.hidden = True if file.hidden is False else False
        file.save()
        messages.add_message(request, messages.SUCCESS, f'Файл успешно скрыт!')
        return render(request, 'storage/index.html', context=get_context_folder(request, **kwargs))
    else:
        messages.add_message(request, messages.ERROR, f'Вы не может скрыть данный файл!')
        return render(request, 'storage/index.html', context=get_context_folder(request, **kwargs))


def edit_file(request, **kwargs):
    """
        Обработчик редактирования файлов с аккаунта преподавателя
    """
    file = File.objects.get(pk=kwargs['file_id'])
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        if request.method == 'POST':
            new_folder = request.POST.get('folder')
            new_title = request.POST.get('title')
            new_description = request.POST.get('description')
            new_hidden = request.POST.get('hidden')
            file.folder = Folder.objects.get(pk=new_folder)
            file.title = new_title
            file.description = new_description
            file.hidden = True if new_hidden == 'on' else False
            file.save()
            messages.add_message(request, messages.SUCCESS, f'Файл успешно изменен!')
            return get_data(request, **kwargs)
        context = {
            'title': 'Изменить файл',
            'speciality_id': kwargs['speciality_id'],
            'teacher_id': kwargs['teacher_id'],
            'file': File.objects.get(pk=kwargs['file_id']),
            'folder_id': kwargs['folder_id'],
            'folders': Folder.objects.filter(teacher=kwargs['teacher_id'],
                                             speciality=kwargs['speciality_id'])
        }
        return render(request, 'storage/edit_file.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, 'У Вас нет доступа к данному разделу')
        return render(request, 'storage/index.html', context=get_context_folder(request, **kwargs))


def add_file(request, **kwargs):
    if not request.user.is_anonymous and \
            int(request.user.privilege) > 1 and \
            kwargs['teacher_id'] == request.user.pk:
        form = FileForm()
        if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, f'Файл успешно загружен!')
                return get_data(request, **kwargs)
            else:
                messages.add_message(request, messages.ERROR, f'Ошибка загрузки файла!')
        context = {
            'title': 'Добавление файла',
            'speciality_id': kwargs['speciality_id'],
            'teacher_id': kwargs['teacher_id'],
            'folders': Folder.objects.filter(teacher=kwargs['teacher_id'],
                                             speciality=kwargs['speciality_id']),
            'form': form
        }
        return render(request, 'storage/add_file.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, 'У Вас нет доступа к данному разделу')
        return get_data(request, **kwargs)

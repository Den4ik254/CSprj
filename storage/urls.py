from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import index, get_data
from .views import create_folder, delete_folder, rename_folder
from .views import delete_file, hide_file, add_file, edit_file

urlpatterns = [
    path('', index, name='index'),  # вызовов обработчика домашней страницы
    path('spec/<int:speciality_id>', get_data, name='spec'),  # вызов обработчика дисциалины
    # вызов обработчика преподавателя
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>', get_data, name='teacher'),

    # Folders
    # вызов обработчика создания папки
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/create-folder', create_folder, name='create_folder'),

    # вызов обработчика папки
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>', get_data, name='folder'),

    # вызов обработчика удаления папки
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>/delete',
         delete_folder,
         name='delete_folder'),

    # вызов обработчика переименования папки
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>/rename',
         rename_folder,
         name='rename_folder'),

    # Files
    # вызов обработчика добавления файла
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/add-file', add_file, name='add_file'),

    # вызов обработчика фалйа
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>/file/<int:file_id>',
         get_data,
         name='file'),

    # вызов обработчика удания файла
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>/file/<int:file_id>/delete',
         delete_file,
         name='delete_file'),

    # вызов обработчика скрытия файла
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>/file/<int:file_id>/hide',
         hide_file,
         name='hide_file'),

    # вызов обработчика изменения файла
    path('spec/<int:speciality_id>/teacher/<int:teacher_id>/folder/<int:folder_id>/file/<int:file_id>/edit',
         edit_file,
         name='edit_file'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

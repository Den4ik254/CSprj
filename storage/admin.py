from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Speciality, Folder, File, User


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_date', 'teacher')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'create_date', 'teacher')
    search_fields = ('title',)
    list_editable = ('teacher',)


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_date', 'folder', 'teacher', 'hidden')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'upload_date', 'folder', 'teacher')
    search_fields = ('title',)
    list_editable = ('teacher', 'folder', 'hidden')


class UserAdminNew(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Основная информация', {'fields': (
            'last_name', 'initials',
            'speciality')
        }),
        ('Права доступа', {
            'fields': ('privilege', 'is_superuser', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id', 'username', 'last_name', 'initials', 'privilege', 'last_login')
    list_display_links = ('id', 'username')
    list_editable = ('last_name', 'initials', 'privilege')


admin.site.register(User, UserAdminNew)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)

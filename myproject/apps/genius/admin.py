from django.contrib import admin
from myproject.apps.genius.models import Task, User


@admin.register(Task)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') # поля для отображения в списке объектов
    list_filter = ('date',) # фильтр по дате создания
    search_fields = ('name',) # поиск по имени
    ordering = ('-date',) # сортировка по дате создания

admin.site.register(User)
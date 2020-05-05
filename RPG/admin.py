from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Monster)


@admin.register(models.RPG)
class RPGAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'story')
    search_fields = ('page_number', 'story')
    ordering = ('page_number', 'story')

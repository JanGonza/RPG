from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Monster)
admin.site.register(models.Items)
admin.site.register(models.Crystal)


@admin.register(models.RPG)
class RPGAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'story')
    search_fields = ('page_number', 'story')
    ordering = ('page_number', 'story')


admin.site.register(models.MonsterStatus)

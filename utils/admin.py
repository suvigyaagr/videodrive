from django.contrib import admin

from utils.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'updated_at')
    search_fields = ('key', 'value')
    list_filter = ('updated_at',)
    ordering = ['key']

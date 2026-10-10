from django.contrib import admin
from .models import ParametresSite


@admin.register(ParametresSite)
class ParametresSiteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'maintenance_active', 'maintenance_fin', 'updated_at']

    def has_add_permission(self, request):
        return not ParametresSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib import admin
from .models import CustomUser, EmployeeProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('role',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_admin():
            return queryset
        elif request.user.is_manager():
            return queryset.filter(role='employee')
        return queryset.none()

    def has_add_permission(self, request):
        if request.user.is_manager():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_manager() and obj and obj.role != 'employee':
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmployeeProfile)

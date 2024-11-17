from django.contrib import admin
from .models import CustomUser, EmployeeProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    list_filter = ['role']
    search_fields = ['username', 'email']

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tasks_completed', 'progress']
    search_fields = ['user__username']

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UploadedFile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    list_display = ['username', 'email', 'role', 'shop_name', 'staff_name', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'shop_name', 'staff_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'shop_name', 'staff_name', 'mobile_number')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'shop_name', 'staff_name', 'mobile_number', 'email')
        }),
    )


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """Admin for UploadedFile model"""
    list_display = ['heading', 'name', 'user', 'file_type', 'file_size', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at', 'created_at']
    search_fields = ['heading', 'name', 'description', 'user__username']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    readonly_fields = ['created_at', 'file_size']
    
    def get_queryset(self, request):
        """Filter based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        return qs.filter(user=request.user)

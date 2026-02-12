from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with additional fields"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    staff_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    plain_password = models.CharField(max_length=255, blank=True, null=True)  # For admin viewing only
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.role})"


class UploadedFile(models.Model):
    """Model for uploaded files"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    DOCUMENT_TYPE_CHOICES = [
        ('expense_bill', 'Expense Bill'),
        ('cheque', 'Cheque'),
        ('purchase_bill', 'Purchase Bill'),
        ('legal_document', 'Legal Document'),
        ('other_bill', 'Other Bill'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    heading = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'uploaded_files'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.heading} - {self.name} (by {self.user.username})"

    def get_file_size_display(self):
        """Return human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    # 🔥 THIS PART DELETES FILE FROM R2 WHEN MODEL IS DELETED
    def delete(self, *args, **kwargs):
        if self.file:
            storage = self.file.storage
            if storage.exists(self.file.name):
                storage.delete(self.file.name)
        super().delete(*args, **kwargs)


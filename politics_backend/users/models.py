from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=100, default='user')
    is_approved = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Remove username requirement
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def approve_user(self, approved_by=None):
        """Approve the user and set approval date"""
        self.is_approved = True
        self.approval_date = timezone.now()
        if approved_by and approved_by.is_superuser:
            self.is_user = True
        self.save()
    
    def can_approve_users(self):
        """Check if user can approve other users (superuser or user)"""
        return self.is_superuser or self.is_user


class PendingInfo(models.Model):
    """Model for pending information submissions"""
    heading = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='pending_info/', blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    
    def __str__(self):
        return f"Pending: {self.heading}"
    
    def approve(self, approved_by):
        """Approve this pending info and create an ActiveInfo record"""
        if not approved_by.can_approve_users():
            raise PermissionError("User does not have permission to approve information")
        
        # Create ActiveInfo record
        ActiveInfo.objects.create(
            heading=self.heading,
            description=self.description,
            image=self.image,
            approved_by=approved_by,
            approved_at=timezone.now(),
            submitted_by=self.submitted_by
        )
        
        # Update status
        self.status = 'approved'
        self.save()
    
    def reject(self, rejected_by):
        """Reject this pending info"""
        if not rejected_by.can_approve_users():
            raise PermissionError("User does not have permission to reject information")
        
        self.status = 'rejected'
        self.save()


class ActiveInfo(models.Model):
    """Model for approved/active information"""
    heading = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='active_info/', blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_submissions')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_info')
    approved_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Active: {self.heading}"

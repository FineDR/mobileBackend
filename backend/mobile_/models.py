from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not fullname:
            raise ValueError("The Fullname field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname)
        user.set_password(password)  # Sets the password securely
        user.save(using=self._db)  # Save user to the database
        return user

    def create_superuser(self, email, fullname, password=None):
        user = self.create_user(email, fullname, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Ensure superuser is active by default
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'  # Use email as the username for authentication
    REQUIRED_FIELDS = ['fullname']  # 'fullname' is required in addition to email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin  # Admin users have all permissions

    def has_module_perms(self, app_label):
        return True  # Admin users have permissions to view all apps



class Message(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated ID
    message = models.TextField()  # Field for the message content
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to the custom User model
        on_delete=models.CASCADE,  # Delete messages when the user is deleted
        related_name='messages'  # Optional: allow reverse access to messages from user
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for message creation

    def __str__(self):
        return f"Message from {self.user.email}: {self.message[:20]}..."  # Display a preview of the message


class TransactionDetails(models.Model):
    amountReceived = models.CharField(max_length=100)
    balanceAfterTransaction = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    transactionDate = models.CharField(max_length=100)
    transactionId = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to User model

    def __str__(self):
        return f"Transaction {self.transactionId} by {self.sender}"
    
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # AutoField for auto-incrementing ID
    category_name = models.CharField(max_length=255)  # Field for category name
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ForeignKey to the custom User model
        on_delete=models.CASCADE  # Delete category if the user is deleted
    )

    def __str__(self):
        return f"{self.category_name} by {self.user.fullname}"  # String representation
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.conf import settings
from django.db import models




class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not fullname:
            raise ValueError("The Fullname field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None):
        user = self.create_user(email, fullname, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'mobile_'  # Ensure this matches your app name

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
    category_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
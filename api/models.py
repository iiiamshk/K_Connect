from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractUser
import uuid, pyotp

# Create your models here.
# email: admin@kconnect.in
# pass: 1234
#pythonanywhere superadmin: 12ErKcoonect$3

class User(AbstractUser):
    
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=15)
    isAdmin = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, null=True, blank=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS= ['name']

    objects= UserManager()

    def save(self, *args, **kwargs):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.email
    

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    icon = models.ImageField(upload_to='group_icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')

    def __str__(self):
        return self.name


class Group_member(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_suspend = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name 
    
class Message(models.Model):
    MSG_TYPE = [
        ('General', 'General'),
        ('Emergency', 'Emergency'),
        ('Holiday', 'Holiday'),
        ('Exam Notice', 'Exam Notice'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    files = models.FileField(upload_to='group_files/', null=True, blank=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    msg_type = models.CharField(max_length=20, choices=MSG_TYPE, default='General')

    def __str__(self):
        return str(self.id)

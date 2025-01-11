from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
# email: admin@kconnect.in
# pass: 1234
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=15)
    isAdmin = models.BooleanField(default=False)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS= ['name']

    objects= UserManager()
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

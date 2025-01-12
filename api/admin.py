from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class user(admin.ModelAdmin):
    list_display = ('email','id', 'name', 'phone', 'isAdmin')

class GroupMemberInline(admin.TabularInline):
    model = Group_member
    extra = 3

class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupMemberInline]
    list_display = ('name', 'id','created_by', 'created_at')

admin.site.register(Group, GroupAdmin)
# admin.site.register(Group_member)
admin.site.register(Message)
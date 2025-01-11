from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'phone',
            'password'
        )
        
    #exclude password in get request
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    


class GroupSerializer(serializers.ModelSerializer):
    # created_by = UserSerializer(read_only=True)
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'description',
            'icon',
        )
    

  
class GroupMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email') 
    user_name = serializers.CharField(source='user.name')
    user_phone = serializers.CharField(source='user.phone')
    class Meta:
        model = Group_member
        fields = (
            'user_email',
            'user_name',
            'user_phone',
            'is_admin',
            'is_suspend',
        )

class GroupDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    members = GroupMemberSerializer(many= True, read_only=True)
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'description',
            'icon',
            'created_by',
            'members'
        )
from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'name',
            'email',
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
    members = serializers.SerializerMethodField()
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
    
    def get_members(self, obj):
        members = obj.members.order_by('-is_admin','user__name')
        return GroupMemberSerializer(members, many=True).data




#messages of a group , including group details and sender details
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = (
            'id',
            'group',
            'sender',            
            'message',
            'sent_time',
            'msg_type',
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('group')
        data['sent_time'] = instance.sent_time.strftime("%d %b %Y %H:%M:%S")
        return data
    
   
class GroupMsg_combinedSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    group_id = serializers.UUIDField(source='id')
    group_name = serializers.CharField(source='name')
    group_icon = serializers.ImageField(source='icon')
    class Meta:
        model = Group
        fields = (
            'group_id',
            'group_name',
            'group_icon',
            'messages'
        )
    
    def get_messages(self, obj):
        messages = obj.messages.order_by('sent_time')
        if not messages:
            return {'msg': 'No Message in this group yet'}
        return MessageSerializer(messages, many=True).data
        

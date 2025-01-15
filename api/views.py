from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import User, Group, Group_member
from api.serializers import *
# Create your views here.

def logoutView(request):
    logout(request)
    return JsonResponse({'msg': 'Logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_login(request):
    if request.user.is_authenticated:
        return Response({'msg': 'Already logged in'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data
    email, password = data.get('email', 'ab@ab.com'),data.get('password', '1234')

    if not email or not password:
        return Response({'msg': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)
    if user:
        login(request, user)
        return Response({'msg': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'msg': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



#list and create user accounts
class user_ListCreate(generics.ListCreateAPIView):
    queryset = User.objects.exclude(isAdmin=True)
    serializer_class = UserSerializer 
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, AllowAny]  
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsAdminUser]

        return super().get_permissions()


#delete user account
class user_Delete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 
    lookup_url_kwarg = "u_id"

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return Response({'Error': 'Cannot delete superuser'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


#view and update profile
class profile_ViewUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    



#list and create groups
class group_ListCreate(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    # def get_permissions(self):
    #     self.permission_classes = [IsAuthenticated]
    #     if self.request.method == 'GET':
    #         self.permission_classes = [AllowAny] 
    #     return super().get_permissions()

    #check if group name already exists
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if Group.objects.filter(name__iexact=name).exists(): 
            return Response({'Error': 'Group name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        #the user creating the group is automatically added as a member
        group = serializer.save(created_by=self.request.user)
        Group_member.objects.create(group=group, user=self.request.user)



#view group details
class group_Detail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "g_id"


#view messages of specific group
class group_Message(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        if not group_id:
            return Response({"error": "group_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        #check if user is a member of the group
        group = get_object_or_404(Group, id=group_id)
        if not group.members.filter(user=request.user).exists():
            return Response({"error": "You are not a member of this group"}, status=status.HTTP_403_FORBIDDEN) 

        serializer = GroupMsg_combinedSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)



class create_Message(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    #set sender to current user 
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
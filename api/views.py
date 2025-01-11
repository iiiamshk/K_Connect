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
    email = data.get('email', 'ab@ab.com')
    password = data.get('password', '1234')

    status_code = status.HTTP_400_BAD_REQUEST

    if not email or not password:
        msg = 'Please provide both email and password'

    user = authenticate(email=email, password=password)
    if user:
        login(request, user)
        msg = 'Login successful'
        status_code = status.HTTP_200_OK
    else:
        msg = 'Invalid credentials'
    response ={
        'msg': msg,
        'status_code': status_code
    }
    return Response(response)


#list and create user accounts
class user_ListCreate(generics.ListCreateAPIView):
    queryset = User.objects.exclude(isAdmin=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 



#view and update profile (eg. password reset)
class profile_ViewUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    


#delete user account
class user_Delete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "u_id"


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
            return Response({'Error': 'Group name already exists'})
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        #the user creating the group is automatically added as a member
        group = serializer.save(created_by=self.request.user)
        Group_member.objects.create(group=group, user=self.request.user)



#view group details
class group_detail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "g_id"

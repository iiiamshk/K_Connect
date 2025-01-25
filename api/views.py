from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import User, Group, Group_member
from api.serializers import *
from . import utils
import pyotp


# Create your views here.

# def logoutView(request):
#     logout(request)
#     return JsonResponse({'msg': 'Logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_login(request):
    if request.user.is_authenticated:
        return Response({'message': 'You are already logged in.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data
    email, password = data.get('email'),data.get('password')

    if not email or not password:
        return Response({'error': 'Both email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)
    if user:
        totp = pyotp.TOTP(user.otp_secret, interval=180)  # otp valid for 3 min(180 sec) 
        otp = totp.now() 

        email_sent = utils.send_otp_mail(otp, user.email)
        if not email_sent:
            return Response({'error': 'Failed to send OTP. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                

        return Response( {"message": "OTP sent successfully.","expires_in": 180}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def verify_otp(request):
    if request.user.is_authenticated:
         return Response({'message': 'You are already logged in.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data
    email, otp = data.get('email', ''), data.get('otp', '')

    if not email or not otp:
        return Response({'error': 'Both email and otp are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        totp = pyotp.TOTP(user.otp_secret, interval= 180) 

        if totp.verify(otp, valid_window = 1):
            
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "OTP verified. Login complete.",
                'authToken': token.key,
                'user_name': user.username,
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "Invalid OTP. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        
    except User.DoesNotExist:
        return Response({"error": "User with the provided email does not exist."}, status=status.HTTP_404_NOT_FOUND)


class logoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('authToken')
        if token:
            try:
                Token.objects.get(key=token).delete()
            except Token.DoesNotExist:
                pass
        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('authToken')
        return response


#list and create user accounts
class user_ListCreate(generics.ListCreateAPIView):
    queryset = User.objects.exclude(isAdmin=True)
    serializer_class = UserSerializer 
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]  
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
            return Response({'error': 'Cannot delete superuser'}, status=status.HTTP_400_BAD_REQUEST)
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

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated] 
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if user.isAdmin:
            return Group.objects.all()
        else:            
            return Group.objects.filter(members__user=user)  
        
        
    def create(self, request, *args, **kwargs):
        #check if group name already exists
        group_name = request.data.get('name')
        if Group.objects.filter(name__iexact=group_name).exists(): 
            return Response({'error': 'Group name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        members = serializer.validated_data.pop('members', [])

        group = serializer.save(created_by=self.request.user)
        Group_member.objects.create(group=group, user=self.request.user, is_admin = True)
        if members:
            utils.add_group_member(group, members)



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



class add_GroupMembers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        
        if not group_id:
            return Response({"error": "group_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        group = get_object_or_404(Group, id=group_id)
        members = request.data.get('members', [])
        if not members:
            return Response({'error': 'No members provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            utils.add_group_member(group, members)
            return Response({'message': 'Members added successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.user_login),
    path('login/verify/', views.verify_otp),

    path('logout/', views.logoutView.as_view()),
    
    path('account/', views.user_ListCreate.as_view()),
    path('account/d/<int:u_id>/', views.user_Delete.as_view()),
    path('profile/', views.profile_ViewUpdate.as_view()),
    
    path('group/', views.group_ListCreate.as_view()), 
    path('group/<uuid:g_id>/', views.group_Detail.as_view()),
    path('group/add-member/', views.add_GroupMembers.as_view()), 

    path('group/messages/', views.group_Message.as_view()),
    path('message/c/', views.create_Message.as_view()),


]

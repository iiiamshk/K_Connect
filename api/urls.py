from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('account/', views.user_ListCreate.as_view(), name='accounts'),
    path('account/d/<int:u_id>/', views.user_Delete.as_view(), name='user_delete'),
    path('profile/', views.profile_ViewUpdate.as_view(), name='myprofile'),
    
    path('group/', views.group_ListCreate.as_view(), name='group'), 
    path('group/<uuid:g_id>/', views.group_Detail.as_view(), name='group_detail'),

    path('group/messages/', views.group_Message.as_view(), name='group_messages'),
    path('message/c/', views.create_Message.as_view(), name='create_message'),

    path('logout/', views.logoutView, name='logout'),

]

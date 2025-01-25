from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('login/', views.login_view, name='login'),
    path('login/verify/', views.login_verify, name='login_verify'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    # path('users/', views.users, name='users'),
    path('group/', views.group_view, name='group'),
    # path('groups/<str:group_id>/', views.group_detail, name='group_detail'),
    # path('groups/<str:group_id>/members/', views.group_members, name='group_members'),
    # path('groups/<str:group_id>/members/<str:user_id>/', views.group_member_detail, name='group_member_detail'),
    # path('groups/<str:group_id>/members/<str:user_id>/remove/', views.remove_group_member, name='remove_group_member'),
    # path('groups/<str:group_id>/members/<str:user_id>/promote/',
]
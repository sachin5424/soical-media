from django.contrib import admin
from django.urls import path,include
from insta import views
app_name='facebook'
urlpatterns = [
    path('home/', views.index,name='home'),
    path('home/<int:pk>/', views.profile_detail,name='profile_detail'),
    path('home/profile_detail_user/<str:user>/', views.profile_detail_user,name='profile_detail_user'),
    path('home/post_User_Post_commt/<int:pk>/', views.Post_commt.as_view(),name='post_User_Post_commt'),
    path('home/frnds_confirm/<str:user>/', views.frnds_confirm,name='frnds_confirm'),
    path('frnd_add/<int:pk>/', views.frnd_add,name='frnd_add'),
    path('frnds_unfrnds/<int:pk>/', views.frnds_unfrnds,name='frnds_unfrnds'),
    path('register_user/', views.register_user,name='register_user'),
    path('', views.user_login,name='user_login'),
]

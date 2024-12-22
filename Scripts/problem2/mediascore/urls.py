from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('home/',views.home, name='home'),
    path('adminHome/',views.adminHome, name='adminHome'),
    path('registration/',views.register, name='register'),
    path('tasks/',views.tasks, name='tasks'),
    path('claimpoint/<int:appid>',views.claimpoint, name='claimpoint'),
    path('add_apps/', views.add_adroidApp, name='add_apps'),
    path('points/', views.points, name="points"),
    path('profile/', views.profile, name="profile"),
    
]
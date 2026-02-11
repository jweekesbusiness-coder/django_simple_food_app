from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    path('register/',view=views.register,name="register"),
    path('login/',view=auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', view=views.logout_view, name='logout'),
    path('profile/',view = views.profile_view, name="profile"),
] 
 
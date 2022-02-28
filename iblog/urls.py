from django.urls import path,include
from . import views

urlpatterns = [
   
    path('', views.index,name='index'),
    path('signin', views.signin,name='signin'),
    path('signout', views.signout,name='signout'),
    path('register', views.register, name='register'),
    path('writeblogs', views.writeblogs, name='writeblogs'),
    path('yourblog', views.yourblog, name='yourblog'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('search', views.search, name="search"),
    path('myblog', views.myblog, name='myblog'),
    path('profile', views.profile, name='profile'),
    path('blogpost/<id>', views.blogpost, name='blogpost'),
    path('deleteblog/<id>', views.deleteblog, name='deleteblog'),
    
] 
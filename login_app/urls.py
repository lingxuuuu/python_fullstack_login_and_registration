from django.urls import path     
from . import views

urlpatterns = [
    #display html
    path('', views.index),
    #this is the route to display after creating a user	
    path('success', views.success),
    #redirects
    #this is the route to create the user and redirect to html
    path('process_register', views.register_user),
    path('login_user', views.login_user),
    path('logout', views.logout)
   ]
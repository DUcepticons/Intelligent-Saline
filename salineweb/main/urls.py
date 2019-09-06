"""salineweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
app_name= 'main'
urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('floor/<int:floor_no>/',views.floor,name='floor'),
    path('floor/<int:floor_no>/room/<int:room_no>/',views.room,name='room'),
    path('ajax/', views.ajaxroomdata, name='ajaxroomdata'),
    path('ajaxhome/', views.ajaxhomeroomdata, name='ajaxhomeroomdata'),
    path('receive/',views.receive,name='receive')
    
]
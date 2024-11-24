"""
URL configuration for treatmentserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('treatment/parameters/set', views.set_treatment_parameters),
    path('treatment/parameters/prev', views.get_prev_treatment),
    path('treatment/parameters/get', views.get_treatment_parameters),
    path('treatment/get_video_call_id', views.get_video_call_id),
    path('treatment/add_video_call_id', views.add_video_call_id),
    path('treatment/remove_video_call_id', views.remove_video_call_id),
    path('treatment/get_all_treatments', views.get_all_treatments),
    path('treatment/get_all_wounds', views.get_all_wounds),
]

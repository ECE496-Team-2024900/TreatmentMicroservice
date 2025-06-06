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
    path('treatment/get_session_info', views.get_session_info),
    path('treatment/parameters/set', views.set_treatment_parameters),
    path('treatment/parameters/prev', views.get_prev_treatment),
    path('treatment/parameters/get', views.get_treatment_parameters),
    path('treatment/get_video_call_id', views.get_video_call_id),
    path('treatment/add_video_call_id', views.add_video_call_id),
    path('treatment/remove_video_call_id', views.remove_video_call_id),
    path('treatment/get_all_treatments', views.get_all_treatments),
    path('treatment/get_all_wounds', views.get_all_wounds),
    path('treatment/get_wound', views.get_wound),
    path('treatment/set_pain_score_and_session_complete', views.set_pain_score_and_session_complete),
    path('treatment/get_all_images_for_wound', views.get_all_images_for_wound),
    path('treatment/add_image', views.add_images),
    path('treatment/timer/<int:treatment_id>/', views.get_treatment_timer, name='get-treatment-timer'),
    path('treatment/get_wounds', views.get_wounds),
    path('treatment/get_treatments', views.get_treatments),
    path('treatment/add_report', views.add_report),
    path('treatment/get_report', views.get_report),
    path('treatment/get_wound_info', views.get_wound_info),
    path('treatment/create_wound', views.create_wound),
    path('treatment/get_patient_wounds', views.get_patient_wounds),
    path('treatment/update_wound_status', views.update_wound_status, name="update_wound_status"),
    path('treatment/add_treatment', views.add_treatment),
    path('treatment/request_reschedule', views.request_reschedule),
    path('treatment/cancel_treatment',views.cancel_treatment)
]

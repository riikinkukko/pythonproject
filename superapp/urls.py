from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from supersite import settings
from . import views
from .models import *

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('register/', doctor_form, name='register'),
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    path('login/', views.doctor_login, name='login'),
    path('about/', about_user_form, name='about'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('pulse_metrics/', views.patient_metrics_pulse, name='pulse_metrics'),
    path('pressure_metrics/', views.patient_metrics_pressures, name='pressure_metrics'),
    path('weight_metrics/', views.patient_metrics_weight, name='weight_metrics'),
    path('doctor_metrics/', views.doctor_metrics, name='doctor_metrics'),
    path('change_form/', views.change_form, name='change_form'),
    path('parameters/', views.parameters, name='parameters'),
    path('temperature_metrics/', views.patient_metrics_temperature, name='temperature_metrics'),
    path('oxygen_blood_metrics/', views.patient_metrics_oxygen_blood, name='oxygen_blood_metrics'),
    path('dairy/', views.dairy_view, name='dairy'),
    path('chat/', views.chat, name='chat'),
    path('codes/', views.codes, name='codes'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
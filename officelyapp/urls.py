from django.urls import path
from officelyapp import views

app_name = 'officelyapp'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    path('app/whatsapp/', views.whatsapp, name='whatsapp'),
    path('app/todo/', views.todo, name='todo'),
    path('app/mail/', views.mail, name='mail'),
    
    path('signature/link/', views.getSignatureLink, name='getSignatureLink'),
    path('signature/link/get/doc', views.getDoc, name='getDoc'),
    path('signature/link/save/template', views.saveTemplate, name='saveTemplate'),
    path('signature/template/', views.getSignatureTemplate, name='getSignatureTemplate'),
    path('signature/enduser/', views.enduserSignature, name='enduserSignature'),

    path('schedule/meeting/link/', views.getMeetingLink, name='getMeetingLink'),
    path('schedule/meeting/template/', views.getMeetingTemplate, name='getMeetingTemplate'),
    path('schedule/meeting/enduser/', views.enduserMeetingLink, name='enduserMeetingLink'),

    path('ocr/new/', views.getNewDoc, name='getNewDoc'),
    path('ocr/enduser/', views.enduserDoc, name='enduserDoc'),

    path('customer/new/', views.newCustomer, name='newCustomer'),
    path('customer/upload/', views.uploadCustomer, name='uploadCustomer'),
    path('customer/get/', views.getCustomer, name='getCustomer'),
    path('customer/api/', views.apiCustomer, name='apiCustomer'),
]
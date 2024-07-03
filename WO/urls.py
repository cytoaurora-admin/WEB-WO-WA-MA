from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_patient, name='add_patient'),

    path('add_patient/', views.add_patient, name='add_patient'),
    path('create_sample_barcode/', views.create_sample_barcode, name='create_sample_barcode'),
    path('create_qrcode_wo/', views.create_qrcode_wo, name='create_qrcode_wo'),
    path('wo_export/', views.wo_export, name='wo_export'),
    path('query_qrcode/', views.query_qrcode, name='query_qrcode'),
    path('query_sample_barcode/', views.query_sample_barcode, name='query_sample_barcode'),
    path('recycle_qrcode/', views.recycle_qrcode, name='recycle_qrcode'),
    path('update_wo_finish_time/', views.update_wo_finish_time, name='update_wo_finish_time'),
    path('update_qrcode/', views.update_qrcode, name='update_qrcode'),
    path('save_qrcode/', views.save_qrcode, name='save_qrcode'),
    path('report_export/', views.report_export, name='report_export'),\

    path('update_option/', views.update_option, name='update_option'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]
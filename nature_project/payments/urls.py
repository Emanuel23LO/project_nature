from . import views
from django.urls import path

urlpatterns = [      
    path('', views.payments, name='payments'),  
    path('payment_status_/<int:payment_id>/', views.change_status_payment, name='payment_status'),          
    path('detail/<int:payment_id>/', views.detail_payment, name='detail_payment'),   
    path('payment_booking/<int:id>/', views.payment_booking, name='payment_booking'),	
    path('payments/generate-pdf/<int:payment_id>/', views.generate_payment_pdf, name='generate_payment_pdf'),
    path('payments/generate-pdf/', views.generate_payment_report, name='generate_payment_report')
    ]


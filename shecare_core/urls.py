from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('screening/', views.screening_view, name='screening'),
    path('report/<str:report_code>/', views.report_detail_view, name='report_detail'),
    path('doctors/', views.doctors_list_view, name='doctors_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail_view, name='doctor_detail'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment_view, name='book_appointment'),
    path('appointment-slip/<str:token_number>/', views.appointment_slip_view, name='appointment_slip'),
    path('diagnostic-tests/', views.diagnostic_tests_view, name='diagnostic_tests'),
    path('lab-voucher/<str:booking_ref>/', views.lab_voucher_view, name='lab_voucher'),
    path('medical-centers/', views.medical_centers_view, name='medical_centers'),
    path('awareness/', views.awareness_hub_view, name='awareness_hub'),
    path('guide/<int:guide_id>/', views.guide_detail_view, name='guide_detail'),
    path('cycle-tracker/', views.cycle_tracker_view, name='cycle_tracker'),
    path('meal-planner/', views.meal_planner_view, name='meal_planner'),
    path('community/', views.community_view, name='community'),
    path('helplines/', views.helplines_view, name='helplines'),
]

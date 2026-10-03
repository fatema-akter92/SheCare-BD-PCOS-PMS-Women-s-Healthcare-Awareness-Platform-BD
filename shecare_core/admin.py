from django.contrib import admin
from .models import (
    Specialty, MedicalCenter, Doctor, DiagnosticTest,
    ScreeningRecord, Appointment, LabBooking, CommunityQuestion, HealthGuide
)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_bn', 'icon')
    search_fields = ('name', 'name_bn')

@admin.register(MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch_name', 'city', 'phone', 'discount_percentage', 'rating')
    list_filter = ('city', 'has_lab', 'has_ultrasound')
    search_fields = ('name', 'branch_name', 'address', 'city')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'hospital_affiliation', 'consultation_fee', 'online_fee', 'rating')
    list_filter = ('specialty', 'is_telemedicine_available')
    search_fields = ('name', 'degrees', 'hospital_affiliation', 'chamber_address')

@admin.register(DiagnosticTest)
class DiagnosticTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'standard_price_bdt', 'discounted_price_bdt', 'is_initial_recommended')
    list_filter = ('category', 'is_initial_recommended')
    search_fields = ('name', 'code', 'purpose')

@admin.register(ScreeningRecord)
class ScreeningRecordAdmin(admin.ModelAdmin):
    list_display = ('report_code', 'patient_name', 'age', 'pcos_risk_level', 'pcos_score', 'pms_severity_level', 'created_at')
    list_filter = ('pcos_risk_level', 'pms_severity_level', 'created_at')
    search_fields = ('report_code', 'patient_name', 'phone')
    readonly_fields = ('report_code', 'created_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('token_number', 'patient_name', 'doctor', 'appointment_type', 'appointment_date', 'time_slot', 'fee', 'status')
    list_filter = ('appointment_type', 'status', 'appointment_date')
    search_fields = ('token_number', 'patient_name', 'patient_phone', 'doctor__name')
    readonly_fields = ('token_number', 'created_at')

@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'patient_name', 'medical_center', 'booking_date', 'final_price', 'status')
    list_filter = ('status', 'booking_date', 'medical_center')
    search_fields = ('booking_reference', 'patient_name', 'patient_phone')
    readonly_fields = ('booking_reference', 'created_at')

@admin.register(CommunityQuestion)
class CommunityQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category', 'is_answered', 'answered_by', 'created_at')
    list_filter = ('category', 'is_answered', 'created_at')
    search_fields = ('title', 'question', 'doctor_answer')

@admin.register(HealthGuide)
class HealthGuideAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'author', 'read_time', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title_en', 'title_bn', 'content_en', 'content_bn')

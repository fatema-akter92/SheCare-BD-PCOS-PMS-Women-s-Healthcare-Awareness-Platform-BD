import uuid
from django.db import models
from django.utils import timezone

class Specialty(models.Model):
    name = models.CharField(max_length=150)
    name_bn = models.CharField(max_length=150, blank=True)
    icon = models.CharField(max_length=50, default="user-md")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name


class MedicalCenter(models.Model):
    CITY_CHOICES = [
        ('Dhaka', 'Dhaka'),
        ('Chittagong', 'Chittagong'),
        ('Sylhet', 'Sylhet'),
        ('Rajshahi', 'Rajshahi'),
        ('Khulna', 'Khulna'),
        ('Cumilla', 'Cumilla'),
    ]

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='Dhaka')
    branch_name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    hotline = models.CharField(max_length=50, default="10616")
    image_url = models.URLField(max_length=500, blank=True)
    discount_percentage = models.PositiveIntegerField(default=20, help_text="Discount for SheCare awareness members")
    has_lab = models.BooleanField(default=True)
    has_ultrasound = models.BooleanField(default=True)
    rating = models.FloatField(default=4.8)
    total_reviews = models.PositiveIntegerField(default=120)

    def __str__(self):
        return f"{self.name} ({self.branch_name}, {self.city})"


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    name_bn = models.CharField(max_length=200, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='doctors')
    degrees = models.CharField(max_length=300)
    hospital_affiliation = models.CharField(max_length=250)
    primary_center = models.ForeignKey(MedicalCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    chamber_address = models.TextField()
    visiting_hours = models.CharField(max_length=200)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1200.00)
    online_fee = models.DecimalField(max_digits=10, decimal_places=2, default=800.00)
    experience_years = models.PositiveIntegerField(default=10)
    rating = models.FloatField(default=4.9)
    review_count = models.PositiveIntegerField(default=85)
    photo_url = models.URLField(max_length=500, blank=True)
    bio = models.TextField()
    bio_bn = models.TextField(blank=True)
    available_days = models.CharField(max_length=150, default="Sat, Sun, Mon, Tue, Wed, Thu")
    is_telemedicine_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.specialty.name}"


class DiagnosticTest(models.Model):
    CATEGORY_CHOICES = [
        ('ultrasound', 'Ultrasonography (USG)'),
        ('hormone', 'Hormonal Profile'),
        ('metabolic', 'Metabolic & Insulin Markers'),
        ('thyroid_vitamins', 'Thyroid & Essential Micronutrients'),
    ]

    name = models.CharField(max_length=250)
    name_bn = models.CharField(max_length=250, blank=True)
    code = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    purpose = models.TextField()
    purpose_bn = models.TextField(blank=True)
    normal_range = models.CharField(max_length=200, blank=True)
    preparation_instructions = models.TextField()
    preparation_bn = models.TextField(blank=True)
    standard_price_bdt = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price_bdt = models.DecimalField(max_digits=10, decimal_places=2)
    is_initial_recommended = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class ScreeningRecord(models.Model):
    RISK_LEVEL_CHOICES = [
        ('Low', 'Low Risk / স্বাভাবিক মাত্রা'),
        ('Moderate', 'Moderate Risk / মাঝারি ঝুঁকি'),
        ('High', 'High Risk / উচ্চ সতর্কতা'),
    ]

    PMS_SEVERITY_CHOICES = [
        ('Mild', 'Mild PMS / মৃদু লক্ষণ'),
        ('Moderate', 'Moderate PMS / মাঝারি লক্ষণ'),
        ('Severe_PMDD', 'Severe PMDD / তীব্র প্রিমেনস্ট্রুয়াল ডিসফোরিক ডিসঅর্ডার'),
    ]

    report_code = models.CharField(max_length=50, unique=True, editable=False)
    patient_name = models.CharField(max_length=150, default="Anonymous SheCare Patient")
    age = models.PositiveIntegerField(default=22)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    
    # Menstrual & Clinical Parameters
    cycle_length = models.PositiveIntegerField(default=28)
    cycle_regularity = models.CharField(max_length=50, default='irregular_mild')
    hirsutism_score = models.PositiveIntegerField(default=1) # 0-3
    cystic_acne = models.BooleanField(default=False)
    hair_thinning = models.BooleanField(default=False)
    weight_difficulty = models.BooleanField(default=False)
    dark_patches_neck = models.BooleanField(default=False) # Acanthosis Nigricans
    pelvic_pain = models.BooleanField(default=False)
    
    # PMS/PMDD Parameters
    pms_mood_swings = models.PositiveIntegerField(default=1) # 0-3
    pms_cramps_severity = models.PositiveIntegerField(default=1) # 0-3
    pms_bloating_fatigue = models.BooleanField(default=False)
    
    # Computed Scores
    pcos_score = models.PositiveIntegerField(default=0)
    pcos_risk_level = models.CharField(max_length=30, choices=RISK_LEVEL_CHOICES, default='Low')
    pms_score = models.PositiveIntegerField(default=0)
    pms_severity_level = models.CharField(max_length=30, choices=PMS_SEVERITY_CHOICES, default='Mild')
    
    clinical_summary = models.TextField(blank=True)
    recommended_tests_summary = models.TextField(blank=True)
    lifestyle_guidance = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.report_code:
            self.report_code = f"SHC-{timezone.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report_code} - {self.patient_name} (PCOS: {self.pcos_risk_level}, PMS: {self.pms_severity_level})"


class Appointment(models.Model):
    TYPE_CHOICES = [
        ('offline_chamber', 'Offline Clinic Chamber / অফলাইন চেম্বার'),
        ('online_telemedicine', 'Online Video Consultation / টেলিমেডিসিন'),
    ]

    PAYMENT_CHOICES = [
        ('unpaid_at_chamber', 'Pay Cash/Card at Medical Center / চেম্বারে পেমেন্ট'),
        ('bkash', 'bKash / বিকাশ'),
        ('nagad', 'Nagad / নগদ'),
        ('paid_online', 'Online Card / অনলাইন কার্ড'),
    ]

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed / নিশ্চিত'),
        ('completed', 'Completed / সম্পন্ন'),
        ('cancelled', 'Cancelled / বাতিল'),
    ]

    token_number = models.CharField(max_length=50, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=150)
    patient_age = models.PositiveIntegerField(default=22)
    patient_phone = models.CharField(max_length=30)
    patient_email = models.EmailField(blank=True)
    appointment_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='offline_chamber')
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    symptoms_description = models.TextField(blank=True)
    screening_record = models.ForeignKey(ScreeningRecord, on_delete=models.SET_NULL, null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='unpaid_at_chamber')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token_number:
            self.token_number = f"APT-{timezone.now().strftime('%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.token_number} - {self.patient_name} with {self.doctor.name}"


class LabBooking(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled / নির্ধারিত'),
        ('sample_collected', 'Sample Collected / স্যাম্পল সংগৃহীত'),
        ('report_ready', 'Report Ready / রিপোর্ট প্রস্তুত'),
    ]

    booking_reference = models.CharField(max_length=50, unique=True, editable=False)
    patient_name = models.CharField(max_length=150)
    patient_phone = models.CharField(max_length=30)
    patient_age = models.PositiveIntegerField(default=22)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    test_package_name = models.CharField(max_length=200)
    selected_tests_summary = models.TextField(blank=True)
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50, default="09:00 AM - 11:00 AM (Fasting Sample)")
    voucher_code = models.CharField(max_length=50, blank=True, default="SHECARE20")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"LAB-{timezone.now().strftime('%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.patient_name} ({self.medical_center.name})"


class CommunityQuestion(models.Model):
    CATEGORY_CHOICES = [
        ('pcos_symptoms', 'PCOS লক্ষণ ও পিরিয়ড অনিয়ম'),
        ('pms_pmdd', 'PMS ও তীব্র মেজাজ খিটখিটে ভাব'),
        ('diet_nutrition', 'দেশি পুষ্টি ও ডায়েট রুটিন'),
        ('fertility_marriage', 'বিয়ে ও ভবিষ্যৎ মাতৃত্ব নিয়ে দুশ্চিন্তা'),
        ('medications', 'ওষুধ ও টেস্ট সম্পর্কিত নির্দেশিকা'),
        ('mental_health', 'মানসিক চাপ ও হরমোন ভারসাম্য'),
    ]

    author_name = models.CharField(max_length=150, default="Anonymous Sister")
    is_anonymous = models.BooleanField(default=True)
    age = models.PositiveIntegerField(default=21)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='pcos_symptoms')
    title = models.CharField(max_length=250)
    question = models.TextField()
    doctor_answer = models.TextField(blank=True)
    answered_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    is_answered = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=15)
    likes_count = models.PositiveIntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"


class HealthGuide(models.Model):
    CATEGORY_CHOICES = [
        ('diet', 'Desi PCOS & PMS Diet / দেশি খাবার ও ডায়েট'),
        ('exercise', 'Exercise & Cortisol / ব্যায়াম ও হরমোন'),
        ('medical_cure', 'Clinical Management / চিকিৎসা ও যত্ন'),
        ('mental_health', 'Emotional Wellness & PMDD / মানসিক স্বস্তি'),
        ('myths_facts', 'Myths vs Facts / ভুল ধারণা বনাম সত্য'),
    ]

    title_en = models.CharField(max_length=250)
    title_bn = models.CharField(max_length=250)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary_en = models.TextField()
    summary_bn = models.TextField()
    content_en = models.TextField()
    content_bn = models.TextField()
    image_url = models.URLField(max_length=500)
    author = models.CharField(max_length=150, default="SheCare Medical Board, Bangladesh")
    read_time = models.CharField(max_length=50, default="4 min read")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title_en} ({self.category})"

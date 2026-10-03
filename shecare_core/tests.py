from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from shecare_core.models import (
    Specialty, MedicalCenter, Doctor, DiagnosticTest,
    ScreeningRecord, Appointment, LabBooking, CommunityQuestion, HealthGuide
)

class SheCarePlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.specialty = Specialty.objects.create(
            name="Gynecology & Obstetrics",
            name_bn="স্ত্রী ও প্রসূতিরোগ",
            icon="stethoscope"
        )
        self.center = MedicalCenter.objects.create(
            name="Popular Diagnostic Center",
            branch_name="Dhanmondi Branch",
            city="Dhaka",
            address="Road 2, Dhanmondi, Dhaka",
            phone="09613787801",
            hotline="10616",
            discount_percentage=20
        )
        self.doctor = Doctor.objects.create(
            name="Prof. Dr. Farhana Dewan",
            name_bn="অধ্যাপক ডাঃ ফারহানা দেওয়ান",
            specialty=self.specialty,
            degrees="MBBS, FCPS",
            hospital_affiliation="DMCH",
            primary_center=self.center,
            chamber_address="Room 304, Popular Diagnostic",
            visiting_hours="5:30 PM - 9:00 PM",
            consultation_fee=1500.00,
            online_fee=1000.00
        )
        self.test = DiagnosticTest.objects.create(
            name="USG of Pelvis (PCOS Protocol)",
            name_bn="তলপেটের আল্ট্রাসনোগ্রাম",
            code="USG-PELV",
            category="ultrasound",
            purpose="Evaluates ovarian follicles and volume",
            preparation_instructions="Full bladder required",
            standard_price_bdt=1800.00,
            discounted_price_bdt=1440.00,
            is_initial_recommended=True
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SheCare")

    def test_screening_submission_high_risk(self):
        payload = {
            'patient_name': 'Sumaiya Akter',
            'age': '22',
            'phone': '01711223344',
            'cycle_length': '45',
            'cycle_regularity': 'irregular_severe',
            'hirsutism_score': '2',
            'cystic_acne': 'on',
            'hair_thinning': 'on',
            'weight_difficulty': 'on',
            'pms_mood_swings': '2',
            'pms_cramps_severity': '2',
            'pms_bloating_fatigue': 'on',
        }
        response = self.client.post(reverse('screening'), payload)
        self.assertEqual(response.status_code, 302)
        
        record = ScreeningRecord.objects.filter(patient_name='Sumaiya Akter').first()
        self.assertIsNotNone(record)
        self.assertTrue(record.pcos_score >= 60)
        self.assertEqual(record.pcos_risk_level, 'High')
        self.assertTrue(record.report_code.startswith('SHC-'))

    def test_report_detail_page(self):
        record = ScreeningRecord.objects.create(
            patient_name='Test Patient',
            age=20,
            cycle_length=35,
            pcos_score=75,
            pcos_risk_level='High',
            pms_score=60,
            pms_severity_level='Moderate'
        )
        response = self.client.get(reverse('report_detail', args=[record.report_code]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, record.report_code)
        self.assertContains(response, "USG-PELV")

    def test_doctor_listing_and_filter(self):
        response = self.client.get(reverse('doctors_list') + f'?specialty={self.specialty.id}&city=Dhaka')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor.name)

    def test_appointment_booking(self):
        payload = {
            'patient_name': 'Ayesha Siddika',
            'patient_age': '24',
            'patient_phone': '01812345678',
            'appointment_type': 'offline_chamber',
            'medical_center': str(self.center.id),
            'appointment_date': date.today().strftime('%Y-%m-%d'),
            'time_slot': '06:30 PM',
            'payment_method': 'unpaid_at_chamber',
        }
        response = self.client.post(reverse('book_appointment', args=[self.doctor.id]), payload)
        self.assertEqual(response.status_code, 302)
        
        apt = Appointment.objects.filter(patient_name='Ayesha Siddika').first()
        self.assertIsNotNone(apt)
        self.assertTrue(apt.token_number.startswith('APT-'))
        self.assertEqual(apt.fee, self.doctor.consultation_fee)

    def test_cycle_tracker_calculation(self):
        last_period = (date.today() - timedelta(days=9)).strftime('%Y-%m-%d')
        response_en = self.client.get(reverse('cycle_tracker') + f'?last_period={last_period}&cycle_length=28&lang=en')
        self.assertEqual(response_en.status_code, 200)
        self.assertContains(response_en, "Flax Seeds")

        response_bn = self.client.get(reverse('cycle_tracker') + f'?last_period={last_period}&cycle_length=28&lang=bn')
        self.assertEqual(response_bn.status_code, 200)
        self.assertContains(response_bn, "ফলিকুলার")

    def test_meal_planner_page(self):
        response = self.client.get(reverse('meal_planner'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "গ্লাইসেমিক")

    def test_helplines_page(self):
        response = self.client.get(reverse('helplines'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "16263")
        self.assertContains(response, "109")
        self.assertContains(response, "999")

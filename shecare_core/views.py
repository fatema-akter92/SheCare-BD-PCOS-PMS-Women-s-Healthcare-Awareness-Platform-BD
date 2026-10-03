import json
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import (
    Specialty, MedicalCenter, Doctor, DiagnosticTest,
    ScreeningRecord, Appointment, LabBooking, CommunityQuestion, HealthGuide
)

def get_current_lang(request):
    """Retrieve language preference from session or query param, default 'bn' for Bangladesh focus."""
    lang = request.GET.get('lang')
    if lang in ['bn', 'en']:
        request.session['lang'] = lang
        return lang
    return request.session.get('lang', 'bn')


def home_view(request):
    lang = get_current_lang(request)
    doctors = Doctor.objects.select_related('specialty', 'primary_center').all()[:4]
    medical_centers = MedicalCenter.objects.all()[:4]
    tests = DiagnosticTest.objects.filter(is_initial_recommended=True)[:4]
    guides = HealthGuide.objects.all()[:3]
    recent_questions = CommunityQuestion.objects.filter(is_answered=True)[:3]
    specialties = Specialty.objects.all()

    context = {
        'lang': lang,
        'doctors': doctors,
        'medical_centers': medical_centers,
        'tests': tests,
        'guides': guides,
        'recent_questions': recent_questions,
        'specialties': specialties,
    }
    return render(request, 'shecare/home.html', context)


def screening_view(request):
    lang = get_current_lang(request)
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', 'Anonymous SheCare Patient').strip() or 'Anonymous SheCare Patient'
        age = int(request.POST.get('age', 22) or 22)
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        
        cycle_length = int(request.POST.get('cycle_length', 28) or 28)
        cycle_regularity = request.POST.get('cycle_regularity', 'regular')
        
        hirsutism_score = int(request.POST.get('hirsutism_score', 0) or 0)
        cystic_acne = request.POST.get('cystic_acne') == 'on'
        hair_thinning = request.POST.get('hair_thinning') == 'on'
        weight_difficulty = request.POST.get('weight_difficulty') == 'on'
        dark_patches_neck = request.POST.get('dark_patches_neck') == 'on'
        pelvic_pain = request.POST.get('pelvic_pain') == 'on'
        
        pms_mood_swings = int(request.POST.get('pms_mood_swings', 0) or 0)
        pms_cramps_severity = int(request.POST.get('pms_cramps_severity', 0) or 0)
        pms_bloating_fatigue = request.POST.get('pms_bloating_fatigue') == 'on'

        # Compute PCOS Risk Score (0 - 100)
        pcos_points = 0
        if cycle_regularity == 'irregular_severe' or cycle_length > 38:
            pcos_points += 30
        elif cycle_regularity == 'irregular_mild' or cycle_length > 35:
            pcos_points += 20
        elif cycle_regularity == 'absent':
            pcos_points += 35
        
        pcos_points += (hirsutism_score * 10)
        if cystic_acne: pcos_points += 10
        if hair_thinning: pcos_points += 10
        if weight_difficulty: pcos_points += 10
        if dark_patches_neck: pcos_points += 15 # strong insulin marker
        if pelvic_pain: pcos_points += 5

        pcos_score = min(pcos_points, 100)
        if pcos_score >= 60:
            pcos_risk_level = 'High'
        elif pcos_score >= 35:
            pcos_risk_level = 'Moderate'
        else:
            pcos_risk_level = 'Low'

        # Compute PMS/PMDD Severity Score (0 - 100)
        pms_points = 0
        pms_points += (pms_mood_swings * 20)
        pms_points += (pms_cramps_severity * 15)
        if pms_bloating_fatigue: pms_points += 20
        if pelvic_pain: pms_points += 10

        pms_score = min(pms_points, 100)
        if pms_score >= 65:
            pms_severity_level = 'Severe_PMDD'
        elif pms_score >= 35:
            pms_severity_level = 'Moderate'
        else:
            pms_severity_level = 'Mild'

        # Clinical summaries
        if pcos_risk_level == 'High':
            clinical_summary = (
                "Clinical signs strongly align with Rotterdam Diagnostic Criteria for Polycystic Ovary Syndrome (PCOS). "
                "Significant markers of chronic oligo/anovulation and clinical hyperandrogenism observed. "
                "Immediate consultation with a reproductive gynecologist or endocrinologist and pelvic ultrasound advised."
            )
        elif pcos_risk_level == 'Moderate':
            clinical_summary = (
                "Mild to moderate hormonal imbalance indicators detected. Possible early or lean PCOS phenotype. "
                "Diagnostic screening recommended along with dietary modification to enhance insulin sensitivity."
            )
        else:
            clinical_summary = (
                "Hormonal risk indicators appear currently within expected clinical ranges. "
                "Maintain healthy sleep, balanced nutrition, and track cycles monthly."
            )

        recommended_tests = (
            "1. USG of Lower Abdomen (PCOS morphology & antral follicle count)\n"
            "2. Serum Total Testosterone & Free Androgen Index\n"
            "3. Serum LH & FSH Ratio (Day 2 or 3 of menstrual bleeding)\n"
            "4. Fasting Serum Insulin & Blood Glucose (HOMA-IR calculation)\n"
            "5. Serum TSH & Free T4 (to rule out secondary hypothyroidism)"
        )

        lifestyle_guidance = (
            "• Switch polished white rice to Bangladeshi Lal Chal (Red Unpolished Rice).\n"
            "• Daily morning Methi (Fenugreek) soaked water.\n"
            "• Follow Seed Cycling: Flax + Pumpkin seeds in Follicular Phase; Sesame + Sunflower in Luteal Phase.\n"
            "• 8,000 brisk steps daily & 20 minutes restorative yoga to reduce cortisol.\n"
            "• Minimize bakery items, dalda/oil paratha, and high-sugar milk tea."
        )

        screening = ScreeningRecord.objects.create(
            patient_name=patient_name,
            age=age,
            phone=phone,
            email=email,
            cycle_length=cycle_length,
            cycle_regularity=cycle_regularity,
            hirsutism_score=hirsutism_score,
            cystic_acne=cystic_acne,
            hair_thinning=hair_thinning,
            weight_difficulty=weight_difficulty,
            dark_patches_neck=dark_patches_neck,
            pelvic_pain=pelvic_pain,
            pms_mood_swings=pms_mood_swings,
            pms_cramps_severity=pms_cramps_severity,
            pms_bloating_fatigue=pms_bloating_fatigue,
            pcos_score=pcos_score,
            pcos_risk_level=pcos_risk_level,
            pms_score=pms_score,
            pms_severity_level=pms_severity_level,
            clinical_summary=clinical_summary,
            recommended_tests_summary=recommended_tests,
            lifestyle_guidance=lifestyle_guidance,
        )

        return redirect('report_detail', report_code=screening.report_code)

    return render(request, 'shecare/screening.html', {'lang': lang})


def report_detail_view(request, report_code):
    lang = get_current_lang(request)
    screening = get_object_or_404(ScreeningRecord, report_code=report_code)
    recommended_doctors = Doctor.objects.all()[:3]
    initial_tests = DiagnosticTest.objects.filter(is_initial_recommended=True)
    partner_centers = MedicalCenter.objects.all()[:3]

    context = {
        'lang': lang,
        'report': screening,
        'doctors': recommended_doctors,
        'tests': initial_tests,
        'centers': partner_centers,
    }
    return render(request, 'shecare/report_detail.html', context)


def doctors_list_view(request):
    lang = get_current_lang(request)
    specialties = Specialty.objects.all()
    cities = MedicalCenter.CITY_CHOICES

    selected_specialty = request.GET.get('specialty', '')
    selected_city = request.GET.get('city', '')
    telemedicine_only = request.GET.get('telemedicine', '')

    doctors = Doctor.objects.select_related('specialty', 'primary_center').all()

    if selected_specialty:
        doctors = doctors.filter(specialty_id=selected_specialty)
    if selected_city:
        doctors = doctors.filter(primary_center__city=selected_city)
    if telemedicine_only == '1':
        doctors = doctors.filter(is_telemedicine_available=True)

    context = {
        'lang': lang,
        'doctors': doctors,
        'specialties': specialties,
        'cities': cities,
        'selected_specialty': selected_specialty,
        'selected_city': selected_city,
        'telemedicine_only': telemedicine_only,
    }
    return render(request, 'shecare/doctors_list.html', context)


def doctor_detail_view(request, doctor_id):
    lang = get_current_lang(request)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    related_doctors = Doctor.objects.filter(specialty=doctor.specialty).exclude(id=doctor.id)[:3]
    return render(request, 'shecare/doctor_detail.html', {
        'lang': lang,
        'doctor': doctor,
        'related_doctors': related_doctors,
    })


def book_appointment_view(request, doctor_id):
    lang = get_current_lang(request)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    medical_centers = MedicalCenter.objects.all()
    screening_code = request.GET.get('report', '')
    screening_record = None
    if screening_code:
        screening_record = ScreeningRecord.objects.filter(report_code=screening_code).first()

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', '').strip()
        patient_age = int(request.POST.get('patient_age', 22) or 22)
        patient_phone = request.POST.get('patient_phone', '').strip()
        patient_email = request.POST.get('patient_email', '').strip()
        appointment_type = request.POST.get('appointment_type', 'offline_chamber')
        medical_center_id = request.POST.get('medical_center')
        appointment_date = request.POST.get('appointment_date')
        time_slot = request.POST.get('time_slot', '06:00 PM')
        symptoms_description = request.POST.get('symptoms_description', '').strip()
        payment_method = request.POST.get('payment_method', 'unpaid_at_chamber')

        medical_center = None
        if appointment_type == 'offline_chamber':
            if medical_center_id:
                medical_center = MedicalCenter.objects.filter(id=medical_center_id).first()
            else:
                medical_center = doctor.primary_center
            fee = doctor.consultation_fee
        else:
            fee = doctor.online_fee

        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            patient_age=patient_age,
            patient_phone=patient_phone,
            patient_email=patient_email,
            appointment_type=appointment_type,
            medical_center=medical_center,
            appointment_date=appointment_date,
            time_slot=time_slot,
            symptoms_description=symptoms_description,
            screening_record=screening_record,
            fee=fee,
            payment_method=payment_method,
            status='confirmed',
        )

        messages.success(request, f"Appointment successfully scheduled! Token: {appointment.token_number}")
        return redirect('appointment_slip', token_number=appointment.token_number)

    today_str = timezone.now().strftime('%Y-%m-%d')
    max_date_str = (timezone.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    return render(request, 'shecare/book_appointment.html', {
        'lang': lang,
        'doctor': doctor,
        'medical_centers': medical_centers,
        'screening_record': screening_record,
        'today_str': today_str,
        'max_date_str': max_date_str,
    })


def appointment_slip_view(request, token_number):
    lang = get_current_lang(request)
    appointment = get_object_or_404(Appointment, token_number=token_number)
    return render(request, 'shecare/appointment_slip.html', {
        'lang': lang,
        'appointment': appointment,
    })


def diagnostic_tests_view(request):
    lang = get_current_lang(request)
    tests = DiagnosticTest.objects.all()
    medical_centers = MedicalCenter.objects.all()
    categories = DiagnosticTest.CATEGORY_CHOICES

    selected_category = request.GET.get('category', '')
    if selected_category:
        tests = tests.filter(category=selected_category)

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', '').strip()
        patient_phone = request.POST.get('patient_phone', '').strip()
        patient_age = int(request.POST.get('patient_age', 22) or 22)
        medical_center_id = request.POST.get('medical_center')
        package_name = request.POST.get('package_name', 'Essential Initial PCOS Panel')
        selected_tests_summary = request.POST.get('selected_tests_summary', 'USG Pelvis, Testosterone, LH/FSH, Fasting Insulin, TSH')
        booking_date = request.POST.get('booking_date')
        time_slot = request.POST.get('time_slot', '09:00 AM - 11:00 AM (Fasting Sample)')
        voucher_code = request.POST.get('voucher_code', 'SHECARE20').strip().upper()

        center = get_object_or_404(MedicalCenter, id=medical_center_id)
        
        # Calculate standard and discounted amounts
        raw_total = sum(t.standard_price_bdt for t in DiagnosticTest.objects.filter(is_initial_recommended=True))
        discount_percent = 20 if voucher_code == 'SHECARE20' else center.discount_percentage
        discount_amt = (raw_total * discount_percent) / 100
        final_amt = raw_total - discount_amt

        lab_booking = LabBooking.objects.create(
            patient_name=patient_name,
            patient_phone=patient_phone,
            patient_age=patient_age,
            medical_center=center,
            test_package_name=package_name,
            selected_tests_summary=selected_tests_summary,
            booking_date=booking_date,
            time_slot=time_slot,
            voucher_code=voucher_code,
            total_price=raw_total,
            discount_amount=discount_amt,
            final_price=final_amt,
            status='scheduled',
        )

        messages.success(request, f"Lab appointment booked! Voucher Reference: {lab_booking.booking_reference}")
        return redirect('lab_voucher', booking_ref=lab_booking.booking_reference)

    today_str = timezone.now().strftime('%Y-%m-%d')
    return render(request, 'shecare/diagnostic_tests.html', {
        'lang': lang,
        'tests': tests,
        'medical_centers': medical_centers,
        'categories': categories,
        'selected_category': selected_category,
        'today_str': today_str,
    })


def lab_voucher_view(request, booking_ref):
    lang = get_current_lang(request)
    lab_booking = get_object_or_404(LabBooking, booking_reference=booking_ref)
    return render(request, 'shecare/lab_voucher.html', {
        'lang': lang,
        'booking': lab_booking,
    })


def awareness_hub_view(request):
    lang = get_current_lang(request)
    guides = HealthGuide.objects.all().order_by('-is_featured', '-created_at')
    category = request.GET.get('category', '')
    if category:
        guides = guides.filter(category=category)
    return render(request, 'shecare/awareness_hub.html', {
        'lang': lang,
        'guides': guides,
        'categories': HealthGuide.CATEGORY_CHOICES,
        'selected_category': category,
    })


def guide_detail_view(request, guide_id):
    lang = get_current_lang(request)
    guide = get_object_or_404(HealthGuide, id=guide_id)
    related_guides = HealthGuide.objects.exclude(id=guide.id)[:3]
    return render(request, 'shecare/guide_detail.html', {
        'lang': lang,
        'guide': guide,
        'related_guides': related_guides,
    })


def cycle_tracker_view(request):
    """Unique Feature 1: Desi Hormone Phase & Cycle Tracker with daily Bangladeshi lifestyle directives."""
    lang = get_current_lang(request)
    context = {'lang': lang}

    last_period_date_str = request.GET.get('last_period')
    cycle_length_str = request.GET.get('cycle_length', '28')

    if last_period_date_str:
        try:
            last_period = datetime.strptime(last_period_date_str, '%Y-%m-%d').date()
            cycle_length = int(cycle_length_str or 28)
            today = timezone.now().date()
            
            days_since = (today - last_period).days
            if days_since < 0:
                days_since = 0

            current_cycle_day = (days_since % cycle_length) + 1
            next_period = last_period + timedelta(days=cycle_length)
            while next_period <= today:
                next_period += timedelta(days=cycle_length)
            
            days_until_next = (next_period - today).days

            # Determine Hormone Phase
            if current_cycle_day <= 5:
                phase_name = "Menstrual Phase"
                phase_name_bn = "মাসিক পর্ব (১ম - ৫ম দিন)"
                hormone_status = "Estrogen & Progesterone are at baseline low levels. Uterine lining shedding."
                hormone_status_bn = "ইস্ট্রোজেন ও প্রোজেস্টেরন হরমোন সর্বনিম্ন স্তরে থাকে। জরায়ুর লাইনিং ঝরে পড়ছে।"
                diet_advice = "Eat warm, iron-rich Desi foods: Lal chal, Kochu shak, Rui macher patla jhol, and warm Ginger (Ada) tea. Replenish lost minerals."
                diet_advice_bn = "গরম ও আয়রন সমৃদ্ধ দেশি খাবার খান: লাল চাল, কচু শাক, রুই মাছের পাতলা ঝোল ও আদা চা। প্রচুর বিশ্রাম নিন।"
                exercise_advice = "Restorative rest, gentle walking, light breathing exercises. Avoid heavy weightlifting or high intensity sprints."
                exercise_advice_bn = "বিশ্রাম ও হালকা হাঁটাচলা। অতিরিক্ত ভারী কাজ বা তীব্র ব্যায়াম এড়িয়ে চলুন।"
                seed_cycling = "Flax Seeds (তিসি) + Pumpkin Seeds (মিষ্টি কুমড়ার বীজ) - 1 tablespoon each."
                phase_color = "rose"

            elif current_cycle_day <= 13:
                phase_name = "Follicular Phase"
                phase_name_bn = "ফলিকুলার পর্ব (৬ষ্ঠ - ১৩তম দিন)"
                hormone_status = "FSH stimulates egg follicles; Estrogen rises steadily. Energy and mental clarity peaking."
                hormone_status_bn = "ডিম্বাশয়ে ফলিকল পরিপক্ব হচ্ছে; ইস্ট্রোজেন হরমোন দ্রুত বৃদ্ধি পাচ্ছে। শক্তি ও চনমনে ভাব বৃদ্ধি পায়।"
                diet_advice = "Incorporate fermented foods, sprout chola (অঙ্কুরিত ছোলা), fresh green vegetables, lemon water, and adequate lean protein."
                diet_advice_bn = "অঙ্কুরিত ছোলা, দেশি সালাদ, লেবুর শরবত ও সুষম প্রোটিন। শরীর সহজে পুষ্টি গ্রহণ করে।"
                exercise_advice = "Optimal time for strength training, aerobic exercises, dance, or progressive brisk walks."
                exercise_advice_bn = "শক্তি বাড়ানোর আদর্শ সময়। দ্রুত হাঁটা, হালকা ওজন নিয়ে ব্যায়াম বা যোগব্যায়াম করুন।"
                seed_cycling = "Phase 1: Flax Seeds (তিসি) + Pumpkin Seeds (মিষ্টি কুমড়ার বীজ) - 1 tbsp each daily."
                phase_color = "sky"

            elif current_cycle_day <= 16:
                phase_name = "Ovulatory Phase"
                phase_name_bn = "ওভুলেশন বা ডিম্বস্ফোটন পর্ব (১৪তম - ১৬তম দিন)"
                hormone_status = "LH surge triggers release of mature egg. Peak estrogen and testosterone levels."
                hormone_status_bn = "এলএইচ (LH) হরমোনের প্রভাবে পরিপক্ব ডিম্বাণু নির্গত হয়। হরমোন ও শারীরিক সক্ষমতা শীর্ষে থাকে।"
                diet_advice = "Fiber-rich cruciferous vegetables (bandhakopi, phulkopi), antioxidant-rich fruits (pepe, amra, guava), and high hydration."
                diet_advice_bn = "প্রচুর ফাইবারযুক্ত সবজি (বাঁধাকপি, পেঁপে, আমড়া, পেয়ারা) এবং পর্যাপ্ত পানি পান করুন।"
                exercise_advice = "Peak physical endurance. Great for cardio, energetic workouts, or sports."
                exercise_advice_bn = "শরীরে সর্বোচ্চ স্ট্যামিনা থাকে। কার্ডিও বা দ্রুত হাঁটা সবচেয়ে ভালো ফল দেবে।"
                seed_cycling = "Transitioning to Phase 2: Sesame Seeds + Sunflower Seeds."
                phase_color = "emerald"

            else:
                phase_name = "Luteal Phase (PMS Window)"
                phase_name_bn = "লুটিয়াল পর্ব ও পিএমএস সময়কাল (১৭তম - ২৮তম দিন)"
                hormone_status = "Progesterone peaks to support potential pregnancy, then drops sharply triggering PMS/PMDD mood swings."
                hormone_status_bn = "প্রোজেস্টেরন হরমোন বৃদ্ধি পেয়ে হঠাৎ কমে যায়, যা থেকে খিটখিটে মেজাজ, পেট ফাঁপা ও তীব্র মিষ্টি খাওয়ার ইচ্ছা তৈরি হয়।"
                diet_advice = "Crucial PMS care: Magnesium-rich snacks (roasted pumpkin seeds, kathbadam, dark chocolate). Strict restriction on bakery sugar, extra salt, and excessive milk tea."
                diet_advice_bn = "পিএমএস নিয়ন্ত্রণের সবচেয়ে গুরুত্বপূর্ণ সময়: কাঠবাদাম, মিষ্টি কুমড়ার বীজ ও ডার্ক চকলেট খান। চিনি, দুধ চা ও অতিরিক্ত লবণ বাদ দিন।"
                exercise_advice = "Shift to cortisol-lowering workouts: Yin yoga, slow evening walking in open air, deep diaphragmatic breathing."
                exercise_advice_bn = "স্ট্রেস হরমোন কর্টিসোল কমাতে খোলা বাতাসে শান্তভাবে হাঁটুন এবং যোগব্যায়াম করুন।"
                seed_cycling = "Phase 2: Sesame Seeds (তিল) + Sunflower Seeds (সূর্যমুখী বীজ) - 1 tablespoon each."
                phase_color = "amber"

            context.update({
                'calculated': True,
                'last_period': last_period_date_str,
                'cycle_length': cycle_length,
                'current_cycle_day': current_cycle_day,
                'next_period': next_period,
                'days_until_next': days_until_next,
                'phase_name': phase_name,
                'phase_name_bn': phase_name_bn,
                'hormone_status': hormone_status,
                'hormone_status_bn': hormone_status_bn,
                'diet_advice': diet_advice,
                'diet_advice_bn': diet_advice_bn,
                'exercise_advice': exercise_advice,
                'exercise_advice_bn': exercise_advice_bn,
                'seed_cycling': seed_cycling,
                'phase_color': phase_color,
            })
        except Exception as e:
            pass

    return render(request, 'shecare/cycle_tracker.html', context)


def meal_planner_view(request):
    """Unique Feature 2: Desi PCOS/PMS Meal Builder & Glycemic Index (GI) Calculator."""
    lang = get_current_lang(request)
    return render(request, 'shecare/meal_planner.html', {'lang': lang})


def community_view(request):
    """Unique Feature 3: SheHelps Safe-Space Q&A Forum."""
    lang = get_current_lang(request)
    questions = CommunityQuestion.objects.all().order_by('-created_at')
    category = request.GET.get('category', '')
    if category:
        questions = questions.filter(category=category)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        question_text = request.POST.get('question', '').strip()
        cat = request.POST.get('category', 'pcos_symptoms')
        author_name = request.POST.get('author_name', 'Anonymous Sister').strip() or 'Anonymous Sister'
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        age = int(request.POST.get('age', 21) or 21)

        if title and question_text:
            CommunityQuestion.objects.create(
                title=title,
                question=question_text,
                category=cat,
                author_name="Anonymous Sister" if is_anonymous else author_name,
                is_anonymous=is_anonymous,
                age=age,
                doctor_answer="",
                is_answered=False,
            )
            messages.success(request, "Your confidential question has been submitted safely to our medical board! We will review and publish verified doctor advice.")
            return redirect('community')

    return render(request, 'shecare/community.html', {
        'lang': lang,
        'questions': questions,
        'categories': CommunityQuestion.CATEGORY_CHOICES,
        'selected_category': category,
    })


def helplines_view(request):
    """Unique Feature 4: Emergency & Telehealth Helplines Hub (Bangladesh)."""
    lang = get_current_lang(request)
    return render(request, 'shecare/helplines.html', {'lang': lang})


def medical_centers_view(request):
    lang = get_current_lang(request)
    city = request.GET.get('city', '')
    centers = MedicalCenter.objects.all()
    if city:
        centers = centers.filter(city=city)
    return render(request, 'shecare/medical_centers.html', {
        'lang': lang,
        'centers': centers,
        'cities': MedicalCenter.CITY_CHOICES,
        'selected_city': city,
    })

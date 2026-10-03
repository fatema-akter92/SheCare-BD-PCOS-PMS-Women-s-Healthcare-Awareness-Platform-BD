import os
from django.core.management.base import BaseCommand
from shecare_core.models import (
    Specialty, MedicalCenter, Doctor, DiagnosticTest,
    CommunityQuestion, HealthGuide
)

class Command(BaseCommand):
    help = "Seeds database with comprehensive medical data for Bangladesh PCOS/PMS platform"

    def handle(self, *args, **options):
        self.stdout.write("Seeding specialties...")
        gynae, _ = Specialty.objects.get_or_create(
            name="Gynecology & Obstetrics",
            defaults={
                "name_bn": "স্ত্রী ও প্রসূতিরোগ বিশেষজ্ঞ",
                "icon": "stethoscope",
                "description": "Specialized in menstrual irregularities, ovarian cysts, PCOS, and reproductive health."
            }
        )
        endo, _ = Specialty.objects.get_or_create(
            name="Endocrinology & Hormone",
            defaults={
                "name_bn": "হরমোন ও ডায়াবেটিস বিশেষজ্ঞ",
                "icon": "activity",
                "description": "Focuses on insulin resistance, androgen excess, thyroid dysfunction, and adrenal balance."
            }
        )
        nutrition, _ = Specialty.objects.get_or_create(
            name="Clinical Nutrition & Dietetics",
            defaults={
                "name_bn": "ক্লিনিক্যাল পুষ্টিবিদ ও ডায়েট বিশেষজ্ঞ",
                "icon": "apple",
                "description": "Evidence-based Bangladeshi meal plans to lower glycemic index and reverse PCOS symptoms."
            }
        )
        mental_health, _ = Specialty.objects.get_or_create(
            name="Mental Health & PMDD Counseling",
            defaults={
                "name_bn": "মানসিক স্বাস্থ্য ও পিএমডিডি কাউন্সেলর",
                "icon": "heart",
                "description": "Compassionate clinical therapy for premenstrual dysphoric disorder, anxiety, and body dysmorphia."
            }
        )

        self.stdout.write("Seeding medical centers across Bangladesh...")
        popular_dhanmondi, _ = MedicalCenter.objects.get_or_create(
            name="Popular Diagnostic Center",
            branch_name="Dhanmondi Branch (Unit 1 & 2)",
            city="Dhaka",
            defaults={
                "address": "House #16, Road #2, Dhanmondi R/A, Dhaka-1205",
                "phone": "+880 9613 787801",
                "hotline": "10616",
                "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 25,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.8,
                "total_reviews": 320
            }
        )

        square_hospital, _ = MedicalCenter.objects.get_or_create(
            name="Square Hospital Ltd.",
            branch_name="Panthapath Main Campus",
            city="Dhaka",
            defaults={
                "address": "18/F, Bir Uttam Qazi Nuruzzaman Sarak, West Panthapath, Dhaka-1205",
                "phone": "+880 2 8159457",
                "hotline": "10616",
                "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 15,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.9,
                "total_reviews": 540
            }
        )

        ibn_sina, _ = MedicalCenter.objects.get_or_create(
            name="Ibn Sina Diagnostic & Consultation Center",
            branch_name="Dhanmondi Branch",
            city="Dhaka",
            defaults={
                "address": "House 48, Road 9/A, Dhanmondi, Dhaka-1209",
                "phone": "+880 9610 010615",
                "hotline": "10615",
                "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 20,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.7,
                "total_reviews": 280
            }
        )

        evercare_dhaka, _ = MedicalCenter.objects.get_or_create(
            name="Evercare Hospital Dhaka",
            branch_name="Bashundhara R/A",
            city="Dhaka",
            defaults={
                "address": "Plot: 81, Block: E, Bashundhara R/A, Dhaka-1229",
                "phone": "+880 2 8431661",
                "hotline": "10678",
                "image_url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 15,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.9,
                "total_reviews": 410
            }
        )

        epic_ctg, _ = MedicalCenter.objects.get_or_create(
            name="Epic Health Care",
            branch_name="Prabartak Circle",
            city="Chittagong",
            defaults={
                "address": "19 K.B. Fazlul Kader Road, Prabartak Circle, Panchlaish, Chattogram",
                "phone": "+880 31 657361",
                "hotline": "09614 656565",
                "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 20,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.8,
                "total_reviews": 190
            }
        )

        mount_adora_sylhet, _ = MedicalCenter.objects.get_or_create(
            name="Mount Adora Hospital",
            branch_name="Subidbazar Branch",
            city="Sylhet",
            defaults={
                "address": "Nayasarak Road, Mirboxtula / Subidbazar, Sylhet-3100",
                "phone": "+880 1798 788888",
                "hotline": "10609",
                "image_url": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 20,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.7,
                "total_reviews": 165
            }
        )

        popular_rajshahi, _ = MedicalCenter.objects.get_or_create(
            name="Popular Diagnostic Center",
            branch_name="Lakshmipur Branch",
            city="Rajshahi",
            defaults={
                "address": "Medical Mor, Lakshmipur, Rajshahi-6000",
                "phone": "+880 9613 787811",
                "hotline": "10616",
                "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=800&q=80",
                "discount_percentage": 20,
                "has_lab": True,
                "has_ultrasound": True,
                "rating": 4.6,
                "total_reviews": 110
            }
        )

        self.stdout.write("Seeding specialist doctors...")
        Doctor.objects.get_or_create(
            name="Prof. Dr. Farhana Dewan",
            defaults={
                "name_bn": "অধ্যাপক ডাঃ ফারহানা দেওয়ান",
                "specialty": gynae,
                "degrees": "MBBS, FCPS (Gynae & Obs), Fellow (Reproductive Health)",
                "hospital_affiliation": "Former Head of Dept, Dhaka Medical College & Hospital (DMCH)",
                "primary_center": popular_dhanmondi,
                "chamber_address": "Room 304, Popular Diagnostic Center, Unit-1, Road 2, Dhanmondi, Dhaka",
                "visiting_hours": "5:30 PM - 9:00 PM (Sat, Sun, Tue, Thu)",
                "consultation_fee": 1500.00,
                "online_fee": 1000.00,
                "experience_years": 24,
                "rating": 4.9,
                "review_count": 210,
                "photo_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80",
                "bio": "National expert in adolescent gynecology, polycystic ovary syndrome, cycle regulation, and hormonal equilibrium with over two decades of distinguished clinical service.",
                "bio_bn": "কৈশোর ও তরুণীদের অনিয়মিত পিরিয়ড, ওভারিয়ান সিস্ট ও হরমোনের অসামঞ্জস্যতা চিকিৎসায় দুই দশকেরও বেশি অভিজ্ঞতাসম্পন্ন দেশের শীর্ষস্থানীয় গাইনি বিশেষজ্ঞ।",
                "available_days": "Sat, Sun, Tue, Thu",
                "is_telemedicine_available": True
            }
        )

        Doctor.objects.update_or_create(
            name="Dr. Nusrat Jahan",
            defaults={
                "name_bn": "ডাঃ নুসরাত জাহান",
                "specialty": gynae,
                "degrees": "MBBS, FCPS (Obs & Gynae), MS, Fellow (Reproductive Endocrinology)",
                "hospital_affiliation": "Bangabandhu Sheikh Mujib Medical University (BSMMU)",
                "primary_center": ibn_sina,
                "chamber_address": "Chamber #402, Ibn Sina Diagnostic Center, Road 9/A, Dhanmondi, Dhaka",
                "visiting_hours": "6:00 PM - 9:30 PM (Sun - Wed)",
                "consultation_fee": 1200.00,
                "online_fee": 800.00,
                "experience_years": 14,
                "rating": 4.9,
                "review_count": 145,
                "photo_url":"https://images.unsplash.com/photo-1527613426441-4da17471b66d?auto=format&fit=crop&w=900&q=80",
                "bio": "Specialized in PCOS phenotype identification, hirsutism reversal, ovulation induction, and lifestyle protocol design for young women and students.",
                "bio_bn": "তরুণী ও ছাত্রীদের পিসিওএস, মুখের অবাঞ্ছিত লোম, ব্রণ ও পিরিয়ডের তীব্র ব্যথার আধুনিক বৈজ্ঞানিক ও সহানুভূতিশীল চিকিৎসায় পারদর্শী।",
                "available_days": "Sun, Mon, Tue, Wed",
                "is_telemedicine_available": True
            }
        )

        Doctor.objects.get_or_create(
            name="Prof. Dr. Shahjada Selim",
            defaults={
                "name_bn": "অধ্যাপক ডাঃ শাহজাদা সেলিম",
                "specialty": endo,
                "degrees": "MBBS, MD (Endocrinology & Metabolism), FACE (USA), FACP",
                "hospital_affiliation": "Department of Endocrinology, BSMMU (PG Hospital), Dhaka",
                "primary_center": square_hospital,
                "chamber_address": "Level 4, OPD Wing, Square Hospital, West Panthapath, Dhaka",
                "visiting_hours": "4:00 PM - 8:30 PM (Sat, Mon, Wed)",
                "consultation_fee": 1600.00,
                "online_fee": 1200.00,
                "experience_years": 18,
                "rating": 4.9,
                "review_count": 310,
                "photo_url": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=600&q=80",
                "bio": "Leading hormone and metabolism scientist in Bangladesh, specializing in PCOS insulin resistance (HOMA-IR), thyroid autoantibodies, and metabolic syndrome.",
                "bio_bn": "পিসিওএস এর মূল কারণ ইনসুলিন রেজিস্ট্যান্স, ওজন বৃদ্ধি, থাইরয়েড ও হরমোন ঘাটতি চিহ্নিত করে দীর্ঘমেয়াদী সমাধানের জাতীয় বিশেষজ্ঞ।",
                "available_days": "Sat, Mon, Wed",
                "is_telemedicine_available": True
            }
        )

        Doctor.objects.get_or_create(
            name="Tamanna Chowdhury",
            defaults={
                "name_bn": "তামান্না চৌধুরী",
                "specialty": nutrition,
                "degrees": "M.Sc (Food & Nutrition, DU), Post Grad Diploma in Clinical Nutrition (India)",
                "hospital_affiliation": "Principal Dietitian, Evercare Hospital Dhaka",
                "primary_center": evercare_dhaka,
                "chamber_address": "Nutrition Clinic, Level 2, Evercare Hospital Dhaka, Bashundhara R/A",
                "visiting_hours": "10:00 AM - 4:00 PM (Sat - Thu)",
                "consultation_fee": 1000.00,
                "online_fee": 700.00,
                "experience_years": 16,
                "rating": 4.8,
                "review_count": 180,
                "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80",
                "bio": "Pioneer of Desi Bangladeshi anti-inflammatory diet, seed cycling protocols, and customized meal planning to reverse insulin spikes without starvation.",
                "bio_bn": "লাল চাল, দেশি শাকসবজি, সিড সাইক্লিং ও পুষ্টিকর খাবারের মাধ্যমে পিসিওএস এবং পিএমএস নিয়ন্ত্রণে দেশের শীর্ষস্থানীয় পুষ্টিবিদ।",
                "available_days": "Sat, Sun, Mon, Tue, Wed, Thu",
                "is_telemedicine_available": True
            }
        )

        Doctor.objects.get_or_create(
            name="Dr. Rubina Akhter",
            defaults={
                "name_bn": "ডাঃ রুবিনা আক্তার",
                "specialty": gynae,
                "degrees": "MBBS, FCPS (Obs & Gynae), Training in Laparoscopic Surgery",
                "hospital_affiliation": "Chittagong Medical College & Hospital (CMCH)",
                "primary_center": epic_ctg,
                "chamber_address": "Epic Health Care, Level 3, Prabartak Circle, Chattogram",
                "visiting_hours": "5:00 PM - 8:30 PM (Sat - Wed)",
                "consultation_fee": 1100.00,
                "online_fee": 800.00,
                "experience_years": 12,
                "rating": 4.8,
                "review_count": 95,
                "photo_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?auto=format&fit=crop&w=600&q=80",
                "bio": "Dedicated gynecologist serving Greater Chittagong, focusing on early detection of ovarian cysts, teenage menstrual dysmenorrhea, and premarital counseling.",
                "bio_bn": "চট্টগ্রাম অঞ্চলের তরুণী ও নারীদের ওভারিয়ান সিস্ট, অতিরিক্ত রক্তক্ষরণ ও মাসিকের ব্যথার জন্য আন্তরিক বিশেষজ্ঞ সেবা।",
                "available_days": "Sat, Sun, Mon, Tue, Wed",
                "is_telemedicine_available": True
            }
        )

        Doctor.objects.get_or_create(
            name="Farzana Kabir (Clinical Psychologist)",
            defaults={
                "name_bn": "ফারজানা কবীর",
                "specialty": mental_health,
                "degrees": "B.Sc & M.Sc (Clinical Psychology, DU), Certified CBT Therapist",
                "hospital_affiliation": "National Institute of Mental Health (NIMH) / SheCare Mental Health Wing",
                "primary_center": popular_dhanmondi,
                "chamber_address": "Consultation Suite 5, Popular Diagnostic Center, Dhanmondi",
                "visiting_hours": "4:00 PM - 8:00 PM (Sat, Mon, Wed)",
                "consultation_fee": 1200.00,
                "online_fee": 900.00,
                "experience_years": 9,
                "rating": 4.9,
                "review_count": 78,
                "photo_url": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=600&q=80",
                "bio": "Specialized in Premenstrual Dysphoric Disorder (PMDD), cyclical depression, anxiety, body image struggles, and stress reduction therapy.",
                "bio_bn": "পিরিয়ডের আগের ভয়ানক খিটখিটে মেজাজ, কান্না ভাব, অতিরিক্ত অস্থিরতা ও পিএমডিডি (PMDD) চিকিৎসায় বিশেষায়িত কাউন্সেলিং।",
                "available_days": "Sat, Mon, Wed",
                "is_telemedicine_available": True
            }
        )

        self.stdout.write("Seeding essential initial diagnostic tests...")
        DiagnosticTest.objects.get_or_create(
            code="USG-PELV",
            defaults={
                "name": "USG of Lower Abdomen / Pelvic Organs (PCOS Protocol)",
                "name_bn": "তলপেটের আল্ট্রাসনোগ্রাম (পিসিওএস প্রোটোকল)",
                "category": "ultrasound",
                "purpose": "Evaluates ovarian volume (>10 cm³), peripheral 'necklace pattern' distribution of 12+ immature follicles, and endometrial thickness.",
                "purpose_bn": "ডিম্বাশয়ের আয়তন বৃদ্ধি এবং পরিধি বরাবর ছোট ছোট সিস্ট বা ফলিকলের উপস্থিতি এবং জরায়ুর লাইনিং পরীক্ষা করা।",
                "normal_range": "Normal ovarian volume < 10 cm³, < 12 small follicles per ovary",
                "preparation_instructions": "Drink 1 to 1.5 liters of clean water 1 hour prior to appointment. Do NOT pass urine (full urinary bladder is essential for clear pelvic acoustic window).",
                "preparation_bn": "টেস্টের ১ ঘণ্টা আগে ১ থেকে দেড় লিটার পানি পান করুন। প্রস্রাব আটকে রাখতে হবে যাতে ব্লাডার পূর্ণ থাকে।",
                "standard_price_bdt": 1800.00,
                "discounted_price_bdt": 1350.00,
                "is_initial_recommended": True
            }
        )

        DiagnosticTest.objects.get_or_create(
            code="HOR-TESTO",
            defaults={
                "name": "Serum Total & Free Testosterone",
                "name_bn": "সিরাম টেস্টোস্টেরন (পুরুষ হরমোন মাত্রা)",
                "category": "hormone",
                "purpose": "Identifies biochemical hyperandrogenism responsible for facial hair (hirsutism), jawline cystic acne, and male-pattern scalp hair thinning.",
                "purpose_bn": "রক্তে অতিরিক্ত এন্ড্রোজেন বা টেস্টোস্টেরন চিহ্নিত করে যা অবাঞ্ছিত লোম, ব্রণ ও চুল পড়ার জন্য দায়ী।",
                "normal_range": "Total: 15 - 70 ng/dL (Female reference range)",
                "preparation_instructions": "Morning blood sample collection preferred (8:00 AM - 10:00 AM) when hormone levels are peak.",
                "preparation_bn": "সকালের দিকে (সকাল ৮টা থেকে ১০টা) রক্তের স্যাম্পল দেয়া সবচেয়ে নির্ভুল ফলাফলের জন্য উত্তম।",
                "standard_price_bdt": 1600.00,
                "discounted_price_bdt": 1280.00,
                "is_initial_recommended": True
            }
        )

        DiagnosticTest.objects.get_or_create(
            code="HOR-LHFSH",
            defaults={
                "name": "Serum LH & FSH Ratio (Day 2 or 3 of Menstrual Cycle)",
                "name_bn": "সিরাম এলএইচ (LH) ও এফএসএইচ (FSH) অনুপাত",
                "category": "hormone",
                "purpose": "Evaluates the Luteinizing Hormone to Follicle-Stimulating Hormone ratio. In PCOS, LH:FSH is frequently 2:1 or 3:1 (normal is ~1:1), causing stalled ovulation.",
                "purpose_bn": "ডিম্বস্ফোটন বা ওভুলেশন বাধাগ্রস্ত হচ্ছে কিনা তা জানতে রক্তে এই দুটি পিটুইটারি হরমোনের অনুপাত দেখা হয়।",
                "normal_range": "LH:FSH ratio approximately 1:1. Ratio > 2:1 indicates anovulatory PCOS state.",
                "preparation_instructions": "CRITICAL: Must be drawn on Day 2 or Day 3 of menstrual flow. If periods are absent for months, consult doctor before sampling.",
                "preparation_bn": "অত্যন্ত গুরুত্বপূর্ণ: মাসিকের রক্তপাতের ২য় বা ৩য় দিনে সকালের স্যাম্পল দিতে হবে।",
                "standard_price_bdt": 2200.00,
                "discounted_price_bdt": 1760.00,
                "is_initial_recommended": True
            }
        )

        DiagnosticTest.objects.get_or_create(
            code="MET-HOMA",
            defaults={
                "name": "Fasting Serum Insulin & Fasting Blood Sugar (HOMA-IR)",
                "name_bn": "ফাস্টিং ইনসুলিন ও সুগার (ইনসুলিন রেজিস্ট্যান্স পরীক্ষা)",
                "category": "metabolic",
                "purpose": "Detects hidden cellular insulin resistance, which drives the ovaries to overproduce male hormones and prevents weight loss.",
                "purpose_bn": "শরীর ইনসুলিন হরমোন ঠিকমতো ব্যবহার করতে পারছে কিনা তা পরীক্ষা করে। পিসিওএস-এ এটি প্রায় ৭০% ক্ষেত্রে দায়ী থাকে।",
                "normal_range": "Fasting Insulin: < 10 µIU/mL. HOMA-IR Score < 1.9 (Optimal)",
                "preparation_instructions": "Strict 10 to 12 hours overnight fasting required. Water is permitted, but avoid tea, coffee, and all morning food.",
                "preparation_bn": "১০ থেকে ১২ ঘণ্টা খালি পেটে থাকতে হবে। শুধু সাদা পানি পান করা যাবে। সকালে চা বা নাস্তা খাওয়া যাবে না।",
                "standard_price_bdt": 1500.00,
                "discounted_price_bdt": 1200.00,
                "is_initial_recommended": True
            }
        )

        DiagnosticTest.objects.get_or_create(
            code="THY-TSH",
            defaults={
                "name": "Serum Thyroid Stimulating Hormone (TSH) & Free T4",
                "name_bn": "থাইরয়েড প্রোফাইল (টিএসএইচ ও ফ্রি টি৪)",
                "category": "thyroid_vitamins",
                "purpose": "Rules out Hypothyroidism, which mimics all signs of PCOS including menstrual irregularities, weight gain, fatigue, and depression.",
                "purpose_bn": "থাইরয়েডের ঘাটতি রয়েছে কিনা যাচাই করা, কারণ হাইপোথাইরয়েডিজমের লক্ষণ পিসিওএস-এর সাথে হুবহু মিলে যায়।",
                "normal_range": "TSH: 0.4 - 4.0 µIU/mL (Ideally 1.0 - 2.5 for optimal fertility & regular cycles)",
                "preparation_instructions": "Fasting not strictly mandatory but recommended early morning sample before taking thyroid tablets if on medication.",
                "preparation_bn": "সকালে স্যাম্পল দেয়া ভালো। থাইরয়েডের কোনো ওষুধ চললে স্যাম্পল দেয়ার পর ওষুধ সেবন করুন।",
                "standard_price_bdt": 1200.00,
                "discounted_price_bdt": 960.00,
                "is_initial_recommended": True
            }
        )

        DiagnosticTest.objects.get_or_create(
            code="VIT-D3",
            defaults={
                "name": "Serum 25-Hydroxy Vitamin D3",
                "name_bn": "সিরাম ভিটামিন ডি৩ পরীক্ষা",
                "category": "thyroid_vitamins",
                "purpose": "Over 80% of Bangladeshi women with PCOS have severe Vitamin D deficiency, worsening insulin resistance, menstrual cramps, and severe PMS.",
                "purpose_bn": "বাংলাদেশি তরুণীদের ৮০% এর শরীরে ভিটামিন ডি কম থাকে, যা পিসিওএস এর তীব্রতা ও মানসিক বিষণ্ণতা বহুগুণ বাড়িয়ে দেয়।",
                "normal_range": "Deficient: < 20 ng/mL, Optimal: 30 - 70 ng/mL",
                "preparation_instructions": "No specific fasting required. Routine venous blood draw.",
                "preparation_bn": "খালি পেটে থাকার প্রয়োজন নেই। যেকোনো সময় স্যাম্পল দেয়া যায়।",
                "standard_price_bdt": 2400.00,
                "discounted_price_bdt": 1920.00,
                "is_initial_recommended": True
            }
        )

        self.stdout.write("Seeding health guides & awareness articles...")
        HealthGuide.objects.get_or_create(
            title_en="Desi PCOS Nutrition: The Ultimate Bangladeshi Hormone-Balancing Meal Guide",
            defaults={
                "title_bn": "দেশি খাবারে পিসিওএস নিয়ন্ত্রণ: হরমোন ব্যালেন্সের সহজ খাদ্যতালিকা",
                "category": "diet",
                "summary_en": "Learn how to replace refined polished white rice with Lal Chal, incorporate methi water, seed cycling, and avoid blood sugar spikes using affordable Bangladeshi ingredients.",
                "summary_bn": "সাদা ভাতের বদলে লাল চাল, মেথি ভেজানো পানি, দেশি শাকসবজি ও সিড সাইক্লিং-এর মাধ্যমে যেভাবে স্বাভাবিক করবেন আপনার হরমোন।",
                "content_en": """
### The Core Strategy: Taming Insulin Resistance with Desi Food
In Bangladesh, our traditional meals revolve heavily around polished white rice, sugary snacks (cha with milk and condensed sugar), and deep-fried roadside treats (singara, puri, samucha). For a woman with PCOS or severe PMS, these refined carbs trigger severe insulin spikes, prompting ovaries to produce excess testosterone.

#### 1. The Smart Bangladeshi Carbohydrate Swaps:
* **Swap White Miniket Rice with Dheki-chhata / Lal Chal (Red Unpolished Rice):** Rich in complex fiber and B-vitamins, red rice digests slowly, preventing sudden insulin surges.
* **Whole Wheat Atta Ruti with Mixed Vegetables (Shobji):** Instead of white flour (maida) paratha fried in dalda.
* **Oats Khichuri or Daliya:** Cooked with lentils and abundant spinach or bottle gourd (lau).

#### 2. Local Bangladeshi Superfoods for PCOS:
* **Methi (Fenugreek) Water:** Soak 1 teaspoon of fenugreek seeds in a glass of warm water overnight; drink every morning. Proven by clinical trials to improve insulin sensitivity and ovarian health.
* **Cinnamon (Darchini) Infusion:** Ceylon cinnamon reduces fasting glucose and assists in menstrual cycle regularity.
* **Local Freshwater Fish (Rui, Katla, Shole, Ilish):** Excellent sources of anti-inflammatory Omega-3 fatty acids. Avoid deep-frying; prefer light curries (macher jhol) with turmeric and ginger.
* **Greens & Shak:** Palong shak, Kochu shak (rich in plant iron to replenish menstrual losses), Pui shak, and Korola (bitter gourd to regulate glucose).

#### 3. Seed Cycling Protocol:
* **Days 1 to 14 (Menstrual & Follicular Phase):** 1 tablespoon ground Organic Flax Seeds (Tishi) + 1 tablespoon raw Pumpkin Seeds (Misty kumrar bichi) daily. Boosts estrogen clearance and supports follicle maturation.
* **Days 15 to 28 (Luteal Phase until period):** 1 tablespoon Sesame Seeds (Til) + 1 tablespoon Sunflower Seeds (Surjamukhir bichi) daily. Supports healthy progesterone to reduce PMS depression and cramping.
                """,
                "content_bn": """
### দেশি পুষ্টির মূল কৌশল: ইনসুলিন রেজিস্ট্যান্স ও হরমোন সমতা
আমাদের দেশে অতিরিক্ত সাদা চালের ভাত, চিনিযুক্ত চা, এবং বিকেলে শিঙাড়া-পুরির মতো ভাজাপোড়া খাওয়ার অভ্যাসের কারণে রক্তে হঠাৎ ইনসুলিনের মাত্রা বেড়ে যায়। এটি ডিম্বাশয়কে অতিরিক্ত পুরুষ হরমোন তৈরি করতে বাধ্য করে, যা থেকে পিসিওএস হয়।

#### ১. খাবারের স্বাস্থ্যকর দেশি বিকল্প:
* **মিনিকেট বা নাজিরশাইল চালের বদলে লাল চাল:** লাল চালে প্রচুর ফাইবার থাকে যা রক্তে ধীরে ধীরে গ্লুকোজ ছড়ায়।
* **ময়দার পরোটার বদলে আটার লাল রুটি ও সবজি:** ডালডা বা সয়াবিনে ভাজা পরোটা সম্পূর্ণরূপে পরিহার করুন।
* **শাক ও সবজির প্রাচুর্য:** পালং শাক, কচু শাক (আয়রন সমৃদ্ধ), লাউ, পটল এবং করলার হালকা তরকারি।

#### ২. পিসিওএস নিরাময়ে দেশি পথ্য:
* **মেথি ভেজানো পানি:** রাতে এক চামচ মেথি এক গ্লাস পানিতে ভিজিয়ে রেখে সকালে খালি পেটে খান। ইনসুলিনের কার্যক্ষমতা বাড়াতে এটি বিজ্ঞানসম্মতভাবে অত্যন্ত কার্যকর।
* **দারুচিনির চা:** গরম পানিতে এক টুকরো দারুচিনি ফুটিয়ে খেলে হরমোন ব্যালেন্স হয় এবং পিরিয়ড নিয়মিত হতে সাহায্য করে।
* **তাজা মাছ:** রুই, কাতলা ও ছোট মাছের পাতলা ঝোল খান যা ওমেগা-৩ ফ্যাটি এসিডে সমৃদ্ধ।

#### ৩. সিড সাইক্লিং (বীজ চক্র):
* **১ম দিন থেকে ১৪তম দিন (ফলিকুলার ফেজ):** প্রতিদিন ১ চামচ তিসি বীজ (ফ্ল্যাক্স সিড) গুঁড়া + ১ চামচ মিষ্টি কুমড়ার বীজ।
* **১৫তম দিন থেকে ২৮তম দিন (লুটিয়াল ফেজ):** প্রতিদিন ১ চামচ তিল (সাদা/কালো তিল) + ১ চামচ সূর্যমুখীর বীজ। এটি প্রোজেস্টেরন হরমোন বাড়িয়ে পিএমএস-এর কষ্ট কমায়।
                """,
                "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80",
                "author": "Tamanna Chowdhury, Principal Clinical Dietitian",
                "read_time": "5 min read",
                "is_featured": True
            }
        )

        HealthGuide.objects.get_or_create(
            title_en="Breaking Bangladeshi Taboos: 6 Dangerous Myths About PCOS & Fertility",
            defaults={
                "title_bn": "পিসিওএস ও ভবিষ্যৎ মাতৃত্ব: ৬টি ক্ষতিকর কুসংস্কার ও সঠিক বৈজ্ঞানিক তথ্য",
                "category": "myths_facts",
                "summary_en": "Debunking common misconceptions in Bangladeshi society: from marriage expectations to birth control myths and lean PCOS.",
                "summary_bn": "বিয়ে হলেই কি পিসিওএস ভালো হয়ে যায়? পিসিওএস থাকলে কি কখনো সন্তান হয় না? জেনে নিন দেশের শীর্ষ চিকিৎসকদের সঠিক পরামর্শ।",
                "content_en": """
### Myth 1: "Having PCOS means you can never become a mother."
**FACT:** Absolutely FALSE. PCOS causes irregular ovulation, not permanent infertility. With lifestyle modifications, weight optimization, inositol supplements, or simple ovulation medication, the vast majority of women with PCOS conceive naturally and have healthy pregnancies.

### Myth 2: "Just get married, and all period problems will automatically disappear."
**FACT:** A dangerous and prevalent cultural myth in Bangladesh. Marriage does not alter your endocrine system or cure insulin resistance. Delaying medical assessment until after marriage leads to unnecessary marital distress. Seek specialized medical evaluation as soon as symptoms arise in adolescence.

### Myth 3: "Only overweight or obese girls get PCOS."
**FACT:** False. Approximately 20% to 30% of South Asian women with PCOS have **Lean PCOS** (normal or underweight BMI). They still experience severe cystic acne, excess facial hair, and anovulatory cycles due to high visceral adiposity, stress, and genetics.

### Myth 4: "Taking hormonal pills prescribed by a doctor makes you permanently infertile."
**FACT:** Hormonal medications (like cyclic progesterone or low-dose oral contraceptives) are clinically prescribed to protect your endometrial lining from precancerous hyperplasia caused by months without periods. Once you discontinue them under medical supervision, normal fertility returns.

### Myth 5: "PCOS is caused by drinking cold water or bathing during periods."
**FACT:** Completely untrue. PCOS is a complex neuro-endocrine and metabolic condition rooted in genetic predisposition, insulin receptor sensitivity, and chronic lifestyle stress.

### Myth 6: "You have to do exhausting high-intensity workouts to lose weight."
**FACT:** Over-exercising spikes **Cortisol** (the stress hormone), which worsens adrenal androgen production in PCOS. Gentle, consistent movement—such as 8,000 brisk steps a day, low-impact resistance training, and restorative yoga—yields far superior hormonal recovery.
                """,
                "content_bn": """
### মিথ ১: "পিসিওএস থাকা মানেই সে আর কোনোদিন মা হতে পারবে না।"
**সত্য:** এটি সম্পূর্ণ ভিত্তিহীন। পিসিওএস-এ ডিম্বাণু দেরিতে বা অনিয়মিতভাবে ফোটে, ডিম্বাশয় স্থায়ীভাবে নষ্ট হয়ে যায় না। সঠিক খাদ্যাভ্যাস, ওজন নিয়ন্ত্রণ ও প্রয়োজনীয় চিকিৎসায় ৮০-৯০% নারী স্বাভাবিকভাবে মা হতে পারেন।

### মিথ ২: "বিয়ে দিলে বা বাচ্চা হলেই পিসিওএস আপনা-আপনি সেরে যাবে।"
**সত্য:** আমাদের সমাজে এটি একটি বহুল প্রচলিত ভুল ধারণা। বিয়ে কোনো হরমোনজনিত রোগের চিকিৎসা নয়। লক্ষণ দেখা দেয়ার সাথে সাথে তরুণী বয়সেই চিকিৎসকের শরণাপন্ন হওয়া জরুরি।

### মিথ ৩: "শুধুমাত্র মোটা বা ওজন বেশি মেয়েদেরই পিসিওএস হয়।"
**সত্য:** ভুল। আমাদের দেশে ২০-৩০% ক্ষেত্রে শুকনো মেয়েদেরও 'লিন পিসিওএস' (Lean PCOS) থাকে। ওজন স্বাভাবিক হলেও তাদের মুখে অবাঞ্ছিত লোম, ব্রণ এবং পিরিয়ডের মারাত্মক অনিয়ম হতে পারে।

### মিথ ৪: "ডাক্তারের দেয়া হরমোন পিল খেলে সারা জীবনের জন্য সন্তান ধারণ ক্ষমতা নষ্ট হয়।"
**সত্য:** চিকিৎসকের পরামর্শে নির্দিষ্ট মেয়াদের হরমোন ওষুধ জরায়ুর ভেতরের অংশকে সুরক্ষিত রাখে এবং পিরিয়ড স্বাভাবিক করে। ওষুধ বন্ধ করার পর স্বাভাবিক প্রজনন ক্ষমতা ফিরে আসে।

### মিথ ৫: "মাসিকের সময় গোসল করা বা ঠান্ডা পানি খাওয়ার কারণে সিস্ট হয়।"
**সত্য:** এটি আদিম কুসংস্কার। গোসল বা ঠান্ডা পানির সাথে ওভারিয়ান সিস্টের কোনো সম্পর্ক নেই।

### মিথ ৬: "পিসিওএস কমাতে প্রতিদিন ঘণ্টার পর ঘণ্টা তীব্র ব্যায়াম করতে হবে।"
**সত্য:** অতিরিক্ত তীব্র ব্যায়ামে স্ট্রেস হরমোন (কর্টিসোল) বেড়ে সমস্যা আরও খারাপ হতে পারে। এর বদলে প্রতিদিন আধা ঘণ্টা দ্রুত হাঁটা, হালকা স্ট্রেচিং বা যোগব্যায়াম অনেক বেশি ফলপ্রসূ।
                """,
                "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
                "author": "SheCare Clinical Advisory Board, Dhaka",
                "read_time": "6 min read",
                "is_featured": True
            }
        )

        HealthGuide.objects.get_or_create(
            title_en="Understanding PMS vs. PMDD: When Period Mood Swings Require Medical Care",
            defaults={
                "title_bn": "পিএমএস বনাম পিএমডিডি: মাসিকের আগের অতিরিক্ত রাগ, কান্না ও বিষণ্ণতার প্রতিকার",
                "category": "mental_health",
                "summary_en": "Distinguishing normal premenstrual symptoms from severe Premenstrual Dysphoric Disorder (PMDD) and somatic pain management.",
                "summary_bn": "মাসিক শুরুর ৭-১০ দিন আগে হঠাৎ তীব্র খিটখিটে মেজাজ, অতিরিক্ত বিষণ্ণতা এবং পেটের অসহ্য ব্যথার বৈজ্ঞানিক সমাধান।",
                "content_en": """
### The Biological Shift Before Menstruation
About 7 to 10 days before your period begins (the Late Luteal Phase), progesterone levels surge and then plummet drastically. In women sensitive to neurosteroid shifts, this triggers an acute drop in **Serotonin** (the brain's happiness and calm neurotransmitter).

#### PMS vs. PMDD: Key Differences
* **PMS (Premenstrual Syndrome):** Affects over 75% of women. Symptoms include mild bloating, breast tenderness, food cravings, and manageable moodiness that disappears when bleeding starts.
* **PMDD (Premenstrual Dysphoric Disorder):** A severe, disabling psychiatric and endocrine condition affecting 3% to 8% of women. Symptoms include extreme anger, suicidal thoughts, crying spells without reason, panic attacks, and severe fatigue that disrupts university or job life.

#### Practical Steps to Overcome PMDD in Bangladesh:
1. **Magnesium & Vitamin B6:** Boost neurotransmitter synthesis. Snack on roasted pumpkin seeds, almonds (kathbadam), and dark chocolate.
2. **Reduce Caffeine & Salt in Late Luteal Phase:** Minimizes fluid retention, breast soreness, and heart palpitations.
3. **Warm Herbal Teas:** Ginger tea (Ada cha) with tulsi or chamomile relieves painful prostaglandin uterine contractions.
4. **Professional Help:** If PMDD impairs your daily relationships or study, an endocrinologist or psychiatrist can prescribe cyclic serotonin support or hormonal therapy.
                """,
                "content_bn": """
### মাসিকের আগের মনস্তাত্ত্বিক ও শারীরিক পরিবর্তন
পিরিয়ড শুরু হওয়ার প্রায় এক সপ্তাহ আগে শরীরে প্রোজেস্টেরন হরমোন হঠাৎ কমে যায়। এর ফলে মস্তিষ্কে 'সেরোটোনিন' নামক ভালো লাগার রাসায়নিক কমে যায়।

#### সাধারণ পিএমএস (PMS) বনাম মারাত্মক পিএমডিডি (PMDD):
* **পিএমএস (PMS):** অধিকাংশ নারীর ক্ষেত্রে দেখা যায়। হালকা পেট ফাঁপা, মিষ্টি খাওয়ার ইচ্ছা, এবং সাময়িক মেজাজ পরিবর্তন যা রক্তপাত শুরু হলেই ভালো হয়ে যায়।
* **পিএমডিডি (PMDD):** এটি একটি তীব্র ও জটিল সমস্যা। এতে তীব্র হতাশা, হঠাৎ অকারণে কান্না, সম্পর্কের টানাপোড়েন, পড়াশোনা বা কাজের তীব্র ক্ষতি এবং নিজেকে শেষ করে দেয়ার মতো মারাত্মক অনুভূতি তৈরি হতে পারে।

#### আরাম ও উপশমের কার্যকরী উপায়:
১. **ম্যাগনেসিয়াম ও ভিটামিন বি৬:** মস্তিষ্কের সেরোটোনিন বাড়ায়। কাঠবাদাম, মিষ্টি কুমড়ার বীজ ও ডার্ক চকলেট উপকারী।
২. **লবণ ও ক্যাফেইন কমানো:** পিরিয়ডের আগের সপ্তাহে কফি ও অতিরিক্ত লবণযুক্ত খাবার এড়িয়ে চলুন।
৩. **আদা ও তুলসীর গরম চা:** জরায়ুর পেশির টান ও ব্যথা কমাতে অত্যন্ত কার্যকরী।
৪. **চিকিৎসকের সহায়তা:** তীব্র পিএমডিডি থাকলে সংকোচ না করে দ্রুত বিশেষজ্ঞ মানসিক স্বাস্থ্য বা গাইনি চিকিৎসকের পরামর্শ নিন।
                """,
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
                "author": "Farzana Kabir, Clinical Psychologist",
                "read_time": "4 min read",
                "is_featured": False
            }
        )

        self.stdout.write("Seeding community Q&A...")
        CommunityQuestion.objects.get_or_create(
            title="আমার বয়স ১৯, পিরিয়ড ৩ মাস ধরে বন্ধ এবং মুখে ছোট ছোট লোম উঠছে। এটা কি পিসিওএস?",
            defaults={
                "author_name": "একটি বোন, ধানমন্ডি",
                "is_anonymous": True,
                "age": 19,
                "category": "pcos_symptoms",
                "question": "আমি অনার্সে পড়ছি। গত ১ বছর ধরে আমার পিরিয়ড অনিয়মিত, কখনো ২ মাস বা ৩ মাস পর হয়। ইদানীং থুতনিতে এবং গালে ছেলেদের মতো শক্ত লোম উঠছে এবং কোনোভাবেই ওজন কমাতে পারছি না। আমি খুব দুশ্চিন্তায় আছি। আমার এখন কী করা উচিত?",
                "doctor_answer": "আপনার বর্ণিত লক্ষণগুলো—দীর্ঘদিন পিরিয়ড না হওয়া, মুখে অবাঞ্ছিত শক্ত লোম (Hirsutism) এবং ওজন কমার সমস্যা—পলিসিস্টিক ওভারি সিন্ড্রোম (PCOS)-এর প্রধান রটারডাম ক্রাইটেরিয়ার সাথে মিলে যাচ্ছে। আপনি একদম ভয় পাবেন না। প্রথম পদক্ষেপ হিসেবে একজন গাইনি বা হরমোন বিশেষজ্ঞের পরামর্শ নিন এবং একটি তলপেটের আল্ট্রাসনোগ্রাম (USG of Lower Abdomen) ও ফাস্টিং ইনসুলিন পরীক্ষা করিয়ে নিন। খাদ্যাভ্যাস থেকে মিষ্টি, ফাস্টফুড বাদ দিন এবং প্রতিদিন ৩০ মিনিট হাঁটা শুরু করুন। প্রাথমিক অবস্থায় চিকিৎসা শুরু করলে সম্পূর্ণ স্বাভাবিক জীবনে থাকা সম্ভব।",
                "is_answered": True,
                "views_count": 340,
                "likes_count": 48
            }
        )

        CommunityQuestion.objects.get_or_create(
            title="পিরিয়ডের ৭ দিন আগে আমার মেজাজ অতিরিক্ত খারাপ হয় ও কান্না আসে। এটা কি স্বাভাবিক?",
            defaults={
                "author_name": "তানজিলা, চট্টগ্রাম",
                "is_anonymous": True,
                "age": 23,
                "category": "pms_pmdd",
                "question": "পিরিয়ড শুরু হওয়ার প্রায় এক সপ্তাহ আগে আমার ভেতরে তীব্র রাগ, অশান্তি এবং সামান্য কথায় চিৎকার বা কান্না করার মতো পরিস্থিতি হয়। পরিবারের লোকজন ভাবে আমি ইচ্ছা করে নাটক করছি। রক্তপাত শুরু হলে আবার সব ঠিক হয়ে যায়। আমি কি কোনো রোগে ভুগছি?",
                "doctor_answer": "তানজিলা, আপনি মোটেও কোনো নাটক করছেন না। আপনি যে শারীরিক ও মানসিক পরিবর্তনের মধ্য দিয়ে যাচ্ছেন তাকে চিকিৎসা বিজ্ঞানে PMDD (Premenstrual Dysphoric Disorder) বলা হয়। এটি কোনো মানসিক দুর্বলতা নয়, বরং মাসিকের আগের হরমোনের তীব্র পরিবর্তনের কারণে মস্তিষ্কের সেরোটোনিন রিসেপ্টরের সংবেদনশীলতা। এ সময় প্রচুর পানি পান করুন, কফি ও অতিরিক্ত লবণ পরিহার করুন, এবং মিষ্টি কুমড়ার বীজ বা বাদাম খান। প্রয়োজনে আমাদের বিশেষজ্ঞ মানসিক স্বাস্থ্য কাউন্সিলরদের সাথে কথা বলতে পারেন। পরিবারকেও এ বিষয়ে চিকিৎসকের পরামর্শ বুঝিয়ে বলুন।",
                "is_answered": True,
                "views_count": 520,
                "likes_count": 89
            }
        )

        CommunityQuestion.objects.get_or_create(
            title="পিসিওএস থাকলে কি মিনিকেট বা নাজিরশাইল ভাত খাওয়া একদম বন্ধ করতে হবে?",
            defaults={
                "author_name": "সাদিয়া, সিলেট",
                "is_anonymous": True,
                "age": 21,
                "category": "diet_nutrition",
                "question": "আমি সিলেট থাকি। ডাক্তার আপা বলেছেন ভাত কম খেতে। কিন্তু ভাতের বদলে রুটি খেলে পেট ভরে না। আমি দেশি খাবারের মধ্যে কীভাবে ডায়েট ম্যানেজ করব?",
                "doctor_answer": "সাদিয়া, আপনাকে ভাত একদম ছেড়ে দিতে হবে না। মূল কৌশল হলো রিফাইন্ড বা পালিশ করা সাদা ভাতের বদলে লাল চাল (Dheki-chhata Lal Chal) খাওয়া। লাল চালের গ্লাইসেমিক ইনডেক্স অনেক কম থাকে। খাবারের প্লেটের অর্ধেকটা রাখুন শাক ও দেশি সবজি (যেমন লাউ, পটল, পেঁপে), চার ভাগের এক ভাগ লাল চালের ভাত এবং বাকি চার ভাগের এক ভাগ প্রোটিন (রুই বা কাতলা মাছ, সিদ্ধ ডিম বা ডাল)। ভাত খাওয়ার আগে সবজি ও প্রোটিন খেলে রক্তে সুগার বা ইনসুলিন দ্রুত বৃদ্ধি পায় না।",
                "is_answered": True,
                "views_count": 270,
                "likes_count": 34
            }
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with authentic Bangladeshi medical data!"))

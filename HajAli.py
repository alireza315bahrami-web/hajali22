import random
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== تنظیمات ====================
TOKEN = "8810239565:AAFtU28AaBDYzVZW-qy8_rOW2yIqCnWDWhM"
ADMIN_ID = 7443695973
YOUR_CHANNEL = "https://t.me/sharafoshamse315"
CHANNEL_ID = "@sharafoshamse315"
CLIP_HASHTAG = "#شرفـ‌الشمس"
# =================================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==================== احادیث (۳۰ عدد) ====================
AHADITH = [
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلْعِلْمُ وِراثَةٌ كَریمَةٌ»\n🔹 دانش میراثی گرانبهاست.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَلْكَمَالُ التَّفَقُّهُ فِي الدِّينِ وَ الصَّبْرُ»\n🔹 کمال در فهم دین و صبر است.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«اَلْمُؤْمِنُ مِرْآةُ الْمُؤْمِنِ»\n🔹 مؤمن آینه مؤمن است.\n📖 بحارالأنوار\n🕌 @HajAliBot",
    "📚 *امام باقر (ع):*\n«مَنْ سَاءَ خُلُقُهُ عَذَّبَ نَفْسَهُ»\n🔹 بداخلاق خودش را عذاب می‌دهد.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«الصَّبْرُ مِنَ الاْيمانِ كَالرَّأْسِ»\n🔹 صبر مانند سر برای بدن است.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام حسن عسکری (ع):*\n«خَصْلَتانِ: اَلاْیمانُ وَ نَفْعُ الاِْخْوانِ»\n🔹 ایمان و سود رساندن.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَحَبُّ اِخْوَانِي مَنْ اَهْدَى عُيُوبِي»\n🔹 بهترین برادر.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«مَنْ اَصْلَحَ سَريرَتَهُ اَصْلَحَ اللّهُ عَلانِيَتَهُ»\n🔹 اصلاح درون.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *علامه طباطبایی:*\n«اسلام دین فطرت است.»\n📖 المیزان\n🕌 @HajAliBot",
    "📚 *امام کاظم (ع):*\n«اَفْضَلُ الْعِبادَةِ اِنْتِظارُ الْفَرَجِ»\n🔹 انتظار فرج.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام رضا (ع):*\n«مَنْ لَمْ يَشْكُرِ الْمُنْعِمَ لَمْ يَشْكُرِ اللّهَ»\n🔹 تشکر از مخلوق.\n📖 عیون\n🕌 @HajAliBot",
    "📚 *امام جواد (ع):*\n«اَلتَّواضُعُ زينَةُ الْحَسَبِ»\n🔹 تواضع زینت است.\n📖 کشف الغمه\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«طَلَبُ الْعِلْمِ فَريضَةٌ»\n🔹 طلب علم واجب است.\n📖 بحار\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلْفَقْرُ فِى الْوَطَنِ غُرْبَةٌ»\n🔹 فقر در وطن غربت است.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام حسین (ع):*\n«اَلنّاسُ عَبيرُ الدُّنْيا»\n🔹 مردم بندگان دنیایند.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام سجاد (ع):*\n«اَللّهُمَّ اِنّي اَعوذُ بِكَ مِنْ عِلْمٍ لا يَنْفَعُ»\n🔹 پناه از علم بی‌فایده.\n📖 صحیفه سجادیه\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَلصَّوْمُ لِي وَ اَنَا اَجْزي بِهِ»\n🔹 روزه برای من است.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امام باقر (ع):*\n«اَلْاِسْلامُ يَعْلو وَ لا يُعْلى»\n🔹 اسلام برتر است.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلصَّديقُ عِنْدَ الضّيقِ»\n🔹 دوست وقت تنگى.\n📖 غررالحکم\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«اَلدّالُّ عَلَى الْخَيْرِ كَفاعِلِهِ»\n🔹 راهنماى خير مانند انجام‌دهنده است.\n📖 بحار\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَلرَّاحِمونَ يَرْحَمُهُمُ الرَّحْمنُ»\n🔹 رحم‌کنندگان.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلصَّبْرُ صَبْرانِ»\n🔹 صبر بر مصيبت و صبر بر معصيت.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام حسن (ع):*\n«اَلْقَريبُ مَنْ قَرَّبَتْهُ الْمَوَدَّةُ»\n🔹 نزدیک آن است که مودت نزدیکش کند.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام رضا (ع):*\n«اَلْعَقْلُ حِفْظُ التَّجارِبِ»\n🔹 عقل حفظ تجربه‌هاست.\n📖 عیون\n🕌 @HajAliBot",
    "📚 *امام هادی (ع):*\n«اَلنّاسُ فِي الدُّنْيا بِالاَْمْوالِ»\n🔹 مردم در دنیا با اموال.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام عسکری (ع):*\n«اَلْغَضَبُ مِفْتاحُ كُلِّ شَرٍّ»\n🔹 خشم كليد هر بدى است.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام زمان (عج):*\n«اِنّي اَمانٌ لاَِِهْلِ الاَْرْضِ»\n🔹 من امان براى زمينم.\n📖 كمال‌الدين\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«اَللِّسانُ ميزانُ الاِْنْسانِ»\n🔹 زبان ميزان انسان است.\n📖 غررالحکم\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَلْعَمَلُ بِغَيْرِ عِلْمٍ كَالسَّيْرِ فِي غَيْرِ طَريقٍ»\n🔹 عمل بدون علم.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَ عَلَّمَهُ»\n🔹 بهترين شما.\n📖 بحار\n🕌 @HajAliBot"
]

# ==================== صلوات (۱۵ عدد) ====================
SALAVAT = [
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّدٍ وَ آلِ مُحَمَّدٍ وَ عَجِّلْ فَرَجَهُمْ*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اَللّهُمَّ عَجِّل لِوَلیِّکَ الفَرَج*\n🤲 برای ظهور\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ كُنْ لِوَلِيِّكَ الحُجَّةِ*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *السَّلامُ عَلَی المَهْدِیِّ*\n🤲 سلام بر امام عصر\n🕌 @HajAliBot",
    "🌹 *صَلَّی اللّهُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n🤲 سلام بر حسین\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی فاطِمَةَ وَ اَبيها*\n🤲 صلوات بر زهرا\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی الرِّضا*\n🤲 صلوات بر امام رضا\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ اهْدِ قُلوبَنا*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ بارِکْ لَنا*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ اغْفِرْ لَنا*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّد وَ آلِهِ وَ سَلِّمْ*\n🤲 صلوات كامل\n🕌 @HajAliBot",
    "🌹 *صَلَواتُ اللّهِ وَ مَلائِكَتِهِ عَلی مُحَمَّد*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلی جَميعِ الاَْنْبِياءِ*\n🤲 صلوات بر انبيا\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ عَجِّلْ فَرَجَ آلِ مُحَمَّد*\n🤲 فرج آل محمد\n🕌 @HajAliBot",
    "🌹 *يا صاحِبَ الزَّمانِ اَدْرِكْنا*\n🤲 يا صاحب الزمان\n🕌 @HajAliBot"
]

# ==================== اشعار (۲۰ عدد) ====================
POEMS = [
    "🎭 *حافظ:* «یوسف گمگشته باز آید به کنعان غم مخور»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «هر کسی کو دور ماند از اصل خویش»\n🕌 @HajAliBot",
    "🎭 *شهریار:* «علی ای همای رحمت تو چه آیتی خدا را»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «بنی آدم اعضای یکدیگرند»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «در اندرون من خسته دل ندانم کیست»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «هر که را اسرار حق آموختند»\n🕌 @HajAliBot",
    "🎭 *صائب:* «به راه عشق نتوان پی به سر منزل مقصود»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «دوش دیدم که ملائک در میخانه زدند»\n🕌 @HajAliBot",
    "🎭 *فردوسی:* «توانا بود هر که دانا بود»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «درخت دوستی بنشان که کام دل به بار آرد»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «رسید مژده که آمد بهار و سبزه دمید»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «نیست در بازار عالم خوشتر از سودای عشق»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «بیا که قصر امل سخت سست بنیاد است»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «اگر خواهی که نفروشد دلت از مهر جانان را»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «در ازل پرتو حسنت ز تجلی دم زد»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «بشنو از نی چون حکایت می‌کند»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «من آن مرغ سخن‌دانم که در خاکم رود صورت»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «اگر آن ترک شیرازی به دست آرد دل ما را»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «ای خدا این وصل را هجران مکن»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «مژده ای دل که دگر باد صبا باز آمد»\n🕌 @HajAliBot"
]

# ==================== نصایح قرآنی (۲۰ عدد) ====================
NASIHAT = [
    "📖 «اِنَّ اللّهَ مَعَ الصّابِرینَ»\n🔹 خدا با صابران است.\n📖 بقره ۱۵۳\n🕌 @HajAliBot",
    "📖 «وَ مَنْ يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\n🔹 توکل کن.\n📖 طلاق ۳\n🕌 @HajAliBot",
    "📖 «اِنَّ مَعَ الْعُسْرِ يُسْراً»\n🔹 آسانی بعد سختی.\n📖 شرح ۶\n🕌 @HajAliBot",
    "📖 «فَاذْكُرُونِي أَذْكُرْكُمْ»\n🔹 یادم کن.\n📖 بقره ۱۵۲\n🕌 @HajAliBot",
    "📖 «وَ قُولُوا لِلنّاسِ حُسْناً»\n🔹 سخن نیک.\n📖 بقره ۸۳\n🕌 @HajAliBot",
    "📖 «اِنَّ اللّهَ يُحِبُّ الْمُحْسِنينَ»\n🔹 خدا نیکوکاران را دوست دارد.\n📖 بقره ۱۹۵\n🕌 @HajAliBot",
    "📖 «وَ اَحْسِنْ كَما اَحْسَنَ اللّهُ اِلَيْكَ»\n🔹 نیکی کن.\n📖 قصص ۷۷\n🕌 @HajAliBot",
    "📖 «اِدْفَعْ بِالَّتي هِيَ اَحْسَنُ»\n🔹 بدی را با خوبی.\n📖 مؤمنون ۹۶\n🕌 @HajAliBot",
    "📖 «اِنَّ الصَّلاةَ تَنْهى عَنِ الْفَحْشاءِ»\n🔹 نماز.\n📖 عنکبوت ۴۵\n🕌 @HajAliBot",
    "📖 «وَ لا تَيْأَسُوا مِنْ رَوْحِ اللّهِ»\n🔹 ناامید نشو.\n📖 یوسف ۸۷\n🕌 @HajAliBot",
    "📖 «وَ مَنْ اَحْياها فَكَاَنَّما اَحْيَا النّاسَ»\n🔹 زنده کردن یک نفر.\n📖 مائده ۳۲\n🕌 @HajAliBot",
    "📖 «اِنْ اَحْسَنْتُمْ اَحْسَنْتُمْ لاَِنْفُسِكُمْ»\n🔹 نیکی به خود.\n📖 اسراء ۷\n🕌 @HajAliBot",
    "📖 «يَرْفَعِ اللّهُ الَّذينَ آمَنوا»\n🔹 خدا بالا می‌برد.\n📖 مجادله ۱۱\n🕌 @HajAliBot",
    "📖 «اِذا قيلَ لَكُمْ تَفَسَّحوا فَافْسَحوا»\n🔹 جا باز کنید.\n📖 مجادله ۱۱\n🕌 @HajAliBot",
    "📖 «وَ جَزاءُ سَيِّئَةٍ سَيِّئَةٌ مِثْلُها»\n🔹 جزای بدی.\n📖 شوری ۴۰\n🕌 @HajAliBot",
    "📖 «وَ اَقِمِ الصَّلاةَ طَرَفَیِ النَّهارِ»\n🔹 اقامه نماز.\n📖 هود ۱۱۴\n🕌 @HajAliBot",
    "📖 «وَ لَذِكْرُ اللّهِ اَكْبَرُ»\n🔹 یاد خدا بزرگتر است.\n📖 عنکبوت ۴۵\n🕌 @HajAliBot",
    "📖 «اُدْعُ اِلى سَبيلِ رَبِّكَ بِالْحِكْمَةِ»\n🔹 با حکمت دعوت کن.\n📖 نحل ۱۲۵\n🕌 @HajAliBot",
    "📖 «اِنَّ اَكْرَمَكُمْ عِنْدَ اللّهِ اَتْقاكُمْ»\n🔹 گرامی‌ترین با تقواترین.\n📖 حجرات ۱۳\n🕌 @HajAliBot",
    "📖 «فَبَشِّرْ عِبادِ الَّذينَ يَسْتَمِعُونَ الْقَوْلَ»\n🔹 بشارت بندگان.\n📖 زمر ۱۷\n🕌 @HajAliBot"
]

# ==================== ذکر روز ====================
AZKAR_ROOZ = {
    0: "📿 *شنبه:* یا رَبَّ الْعالَمین (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    1: "📿 *یکشنبه:* یا ذَاالْجَلالِ وَالاِْکْرام (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    2: "📿 *دوشنبه:* یا قاضِیَ الْحاجات (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    3: "📿 *سه‌شنبه:* یا اَرْحَمَ الرّاحِمین (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    4: "📿 *چهارشنبه:* یا حَیُّ یا قَیّوم (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    5: "📿 *پنج‌شنبه:* لا اِلهَ اِلاَّ اللّهُ (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    6: "📿 *جمعه:* اللّهُمَّ صَلِّ عَلی مُحَمَّد (۱۰۰ مرتبه)\n🕌 @HajAliBot"
}

# ==================== تبلیغ کانال ====================
CHANNEL_AD = f"📢 *کانال شرف‌الشمس:*\n{YOUR_CHANNEL}\n🔹 احادیث | کلیپ | مطالب مذهبی\n🕌 @HajAliBot"

# ==================== شاخص‌ها ====================
hi = si = pi = ni = 0
salavat_counter = {}

# ==================== جستجوی کلیپ ====================
async def get_random_clip(context):
    try:
        messages = []
        async for msg in context.bot.get_chat_history(CHANNEL_ID, limit=100):
            text = msg.text or msg.caption or ""
            if CLIP_HASHTAG in text:
                messages.append(msg)
        if messages:
            return random.choice(messages)
    except:
        pass
    return None

# ==================== تشخیص عدد برای صلوات ====================
def extract_salavat_number(text):
    """اگه کاربر فقط یه عدد ۱ تا ۹۹ بفرسته، به عنوان تعداد صلوات ثبت کنه"""
    text = text.strip()
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 99:
            return num
    return None

# ==================== دستورات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"🏴 *اَلسَّلامُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n\n"
        f"✨ *خوش آمدید {u.first_name} عزیز*\n"
        f"🤖 من *حاج علی* هستم\n\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"📚 *خدمات:*\n"
        f"🔸 /hadis ـ حدیث با ترجمه\n"
        f"🔹 /salavat ـ ذکر صلوات\n"
        f"🔸 /poem ـ شعر تک بیتی\n"
        f"🔹 /nasihat ـ نصیحت قرآنی\n"
        f"🔸 /zekr ـ ذکر روز\n"
        f"🔹 /clip ـ کلیپ مذهبی\n"
        f"🔸 /channel ـ کانال ما\n\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"📿 *صلوات شمار:* /salavatcount\n"
        f"💡 *نکته:* عدد ۱ تا ۹۹ بفرستید\n"
        f"تا همون تعداد صلوات ثبت بشه!\n\n"
        f"🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def help_command(update, context):
    await update.message.reply_text("📚 /hadis /salavat /poem /nasihat /zekr /clip /channel /salavatcount", parse_mode='Markdown')

async def hadis(update, context): global hi; t = AHADITH[hi % len(AHADITH)]; hi += 1; await update.message.reply_text(t, parse_mode='Markdown')

async def salavat(update: Update, context):
    global si
    user_id = update.effective_user.id
    salavat_counter[user_id] = salavat_counter.get(user_id, 0) + 1
    count = salavat_counter[user_id]
    t = SALAVAT[si % len(SALAVAT)]; si += 1
    await update.message.reply_text(f"{t}\n\n📿 *صلوات‌های شما:* {count}", parse_mode='Markdown')

async def salavat_count(update: Update, context):
    user_id = update.effective_user.id
    count = salavat_counter.get(user_id, 0)
    await update.message.reply_text(
        f"📿 *{update.effective_user.first_name} عزیز*\n\n"
        f"🌹 صلوات‌های شما: *{count}*\n\n"
        f"🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def poem(update, context): global pi; t = POEMS[pi % len(POEMS)]; pi += 1; await update.message.reply_text(t, parse_mode='Markdown')
async def nasihat(update, context): global ni; t = NASIHAT[ni % len(NASIHAT)]; ni += 1; await update.message.reply_text(t, parse_mode='Markdown')

async def zekr(update, context):
    await update.message.reply_text(AZKAR_ROOZ[datetime.now().weekday()], parse_mode='Markdown')

async def clip(update: Update, context):
    await update.message.reply_text("🔍 در حال جستجوی کلیپ...")
    msg = await get_random_clip(context)
    if msg:
        try: await msg.forward(update.effective_chat.id)
        except: await update.message.reply_text("❌ خطا در ارسال")
    else:
        await update.message.reply_text("📹 کلیپی پیدا نشد.\n🕌 @HajAliBot")

async def channel(update, context):
    await update.message.reply_text(CHANNEL_AD, parse_mode='Markdown')

async def welcome_new(update, context):
    for m in update.message.new_chat_members:
        await update.message.reply_text(f"🏴 سلام {m.first_name}\n{random.choice(POEMS)}", parse_mode='Markdown')

# ==================== پیام گروه و پیوی ====================
async def group_msg(update: Update, context):
    t = update.message.text.lower()
    global hi, si, pi, ni
    user_id = update.effective_user.id
    
    # اول چک کن عدد خالص فرستاده (برای صلوات)
    num = extract_salavat_number(update.message.text)
    if num:
        salavat_counter[user_id] = salavat_counter.get(user_id, 0) + num
        count = salavat_counter[user_id]
        await update.message.reply_text(
            f"🌹 *{num} صلوات بر محمد و آل محمد*\n\n"
            f"📿 *کل صلوات‌های شما:* {count}\n"
            f"🕌 @HajAliBot",
            parse_mode='Markdown'
        )
        return
    
    if "صلوات" in t:
        salavat_counter[user_id] = salavat_counter.get(user_id, 0) + 1
        count = salavat_counter[user_id]
        r = SALAVAT[si % len(SALAVAT)]; si += 1
        await update.message.reply_text(f"{r}\n\n📿 صلوات: {count}", parse_mode='Markdown')
    elif "حدیث" in t:
        r = AHADITH[hi % len(AHADITH)]; hi += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "شعر" in t:
        r = POEMS[pi % len(POEMS)]; pi += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "نصیحت" in t or "آیه" in t:
        r = NASIHAT[ni % len(NASIHAT)]; ni += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "کلیپ" in t or "فیلم" in t or "ویدیو" in t:
        await update.message.reply_text("🔍 در حال جستجو...")
        msg = await get_random_clip(context)
        if msg:
            try: await msg.forward(update.effective_chat.id); return
            except: pass
        await update.message.reply_text("📹 کلیپی پیدا نشد.\n🕌 @HajAliBot")
    elif "امام زمان" in t or "مهدی" in t:
        await update.message.reply_text("🌹 اللَّهُمَّ عَجِّلْ لِوَلِیِّکَ الْفَرَج\n🕌 @HajAliBot", parse_mode='Markdown')
    elif "سلام" in t and len(t) < 10:
        await update.message.reply_text("🏴 علیکم السلام\n🕌 @HajAliBot", parse_mode='Markdown')

# ==================== ارسال خودکار ====================
async def auto_hadis(context): global hi; await context.bot.send_message(ADMIN_ID, AHADITH[hi % len(AHADITH)], parse_mode='Markdown'); hi += 1
async def auto_salavat(context): global si; await context.bot.send_message(ADMIN_ID, SALAVAT[si % len(SALAVAT)], parse_mode='Markdown'); si += 1
async def auto_poem(context): global pi; await context.bot.send_message(ADMIN_ID, POEMS[pi % len(POEMS)], parse_mode='Markdown'); pi += 1
async def auto_nasihat(context): global ni; await context.bot.send_message(ADMIN_ID, NASIHAT[ni % len(NASIHAT)], parse_mode='Markdown'); ni += 1
async def auto_zekr(context): await context.bot.send_message(ADMIN_ID, AZKAR_ROOZ[datetime.now().weekday()], parse_mode='Markdown')
async def auto_channel(context): await context.bot.send_message(ADMIN_ID, CHANNEL_AD, parse_mode='Markdown')

# ==================== اجرا ====================
def main():
    app = Application.builder().token(TOKEN).build()
    for cmd, func in [("start", start), ("help", help_command), ("hadis", hadis), ("salavat", salavat),
                       ("poem", poem), ("nasihat", nasihat), ("zekr", zekr), ("clip", clip),
                       ("channel", channel), ("salavatcount", salavat_count)]:
        app.add_handler(CommandHandler(cmd, func))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, group_msg))
    jq = app.job_queue
    jq.run_repeating(auto_hadis, interval=3600, first=10)
    jq.run_repeating(auto_salavat, interval=1200, first=30)
    jq.run_repeating(auto_poem, interval=3600, first=60)
    jq.run_repeating(auto_nasihat, interval=3600, first=120)
    jq.run_repeating(auto_zekr, interval=7200, first=180)
    jq.run_repeating(auto_channel, interval=18000, first=300)
    print("🏴 حاج علی روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()

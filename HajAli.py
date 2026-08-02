import random
import logging
from datetime import datetime 
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== تنظیمات ====================
TOKEN = "8810239565:AAFtU28AaBDYzVZW-qy8_rOW2yIqCnWDWhM"
ADMIN_ID = 7443695973
YOUR_CHANNEL = "https://t.me/sharafoshamse315"
# =================================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== احادیث (۵۰ عدد) ====================
AHADITH = [
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلْعِلْمُ وِراثَةٌ كَریمَةٌ»\n🔹 دانش میراثی گرانبهاست.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَلْكَمَالُ التَّفَقُّهُ فِي الدِّينِ وَ الصَّبْرُ»\n🔹 کمال در فهم دین و صبر است.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«اَلْمُؤْمِنُ مِرْآةُ الْمُؤْمِنِ»\n🔹 مؤمن آینه مؤمن است.\n📖 بحارالأنوار\n🕌 @HajAliBot",
    "📚 *امام باقر (ع):*\n«مَنْ سَاءَ خُلُقُهُ عَذَّبَ نَفْسَهُ»\n🔹 بداخلاق خودش را عذاب می‌دهد.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«الصَّبْرُ مِنَ الاْيمانِ كَالرَّأْسِ مِنَ الْجَسَدِ»\n🔹 صبر مانند سر برای بدن است.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام حسن عسکری (ع):*\n«خَصْلَتانِ: اَلاْیمانُ بِاللّهِ وَ نَفْعُ الاِْخْوانِ»\n🔹 ایمان به خدا و سود رساندن به برادران.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اِنَّ اَحَبَّ اِخْوَانِي مَنْ اَهْدَى اِلَيَّ عُيُوبِي»\n🔹 بهترین برادر کسی است که عیب‌هایم را هدیه کند.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«مَنْ اَصْلَحَ سَريرَتَهُ اَصْلَحَ اللّهُ عَلانِيَتَهُ»\n🔹 هر که درونش را اصلاح کند خدا ظاهرش را اصلاح کند.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *علامه طباطبایی:*\n«اسلام دین فطرت است.»\n📖 المیزان\n🕌 @HajAliBot",
    "📚 *علامه طباطبایی:*\n«حقیقت عبادت اظهار بندگی به درگاه الهی است.»\n📖 المیزان\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«خالِطُوا النّاسَ بِاَلْسِنَتِكُمْ وَ زايِلُوهُمْ بِقُلُوبِكُمْ»\n🔹 با زبان همراه باشيد و با قلب جدا.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلْفَقْرُ فِى الْوَطَنِ غُرْبَةٌ»\n🔹 فقر در وطن غربت است.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام کاظم (ع):*\n«اَفْضَلُ الْعِبادَةِ بَعْدَ الْمَعْرِفَةِ اِنْتِظارُ الْفَرَجِ»\n🔹 برترین عبادت بعد از معرفت انتظار فرج است.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام رضا (ع):*\n«مَنْ لَمْ يَشْكُرِ الْمُنْعِمَ مِنَ الْمَخْلوقينَ لَمْ يَشْكُرِ اللّهَ»\n🔹 هر که از مخلوق تشکر نکند از خدا تشکر نکرده.\n📖 عیون اخبار الرضا\n🕌 @HajAliBot",
    "📚 *امام جواد (ع):*\n«اَلتَّواضُعُ زينَةُ الْحَسَبِ»\n🔹 تواضع زینت حسب است.\n📖 کشف الغمه\n🕌 @HajAliBot"
]

# ==================== صلوات (۱۰ عدد) ====================
SALAVAT = [
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّدٍ وَ آلِ مُحَمَّدٍ وَ عَجِّلْ فَرَجَهُمْ*\n🤲 صلوات برای امام زمان (عج)\n🕌 @HajAliBot",
    "🌹 *اَللّهُمَّ عَجِّل لِوَلیِّکَ الفَرَج*\n🤲 برای ظهور دعا کنیم\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ كُنْ لِوَلِيِّكَ الحُجَّةِ بنِ الحَسَن*\n🤲 صلوات برای فرج\n🕌 @HajAliBot",
    "🌹 *السَّلامُ عَلَی المَهْدِیِّ*\n🤲 سلام بر امام عصر\n🕌 @HajAliBot",
    "🌹 *صَلَّی اللّهُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n🤲 سلام بر سیدالشهدا\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی فاطِمَةَ وَ اَبیها وَ بَعْلِها وَ بَنیها*\n🤲 صلوات بر حضرت زهرا\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی عَلِیِّ بْنِ موسَی الرِّضا*\n🤲 صلوات بر امام رضا\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّد وَ آلِ مُحَمَّد وَ اهْدِ قُلوبَنا*\n🤲 صلوات برای هدایت قلب\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّد وَ آلِ مُحَمَّد وَ بارِکْ لَنا*\n🤲 صلوات برای برکت\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّد وَ آلِ مُحَمَّد وَ اغْفِرْ لَنا*\n🤲 صلوات برای آمرزش\n🕌 @HajAliBot"
]

# ==================== اشعار (۱۵ عدد) ====================
POEMS = [
    "🎭 *حافظ:*\n«یوسف گمگشته باز آید به کنعان غم مخور»\n🕌 @HajAliBot",
    "🎭 *مولانا:*\n«هر کسی کو دور ماند از اصل خویش / باز جوید روزگار وصل خویش»\n🕌 @HajAliBot",
    "🎭 *شهریار:*\n«علی ای همای رحمت تو چه آیتی خدا را»\n🕌 @HajAliBot",
    "🎭 *سعدی:*\n«بنی آدم اعضای یکدیگرند»\n🕌 @HajAliBot",
    "🎭 *حافظ:*\n«در اندرون من خسته دل ندانم کیست»\n🕌 @HajAliBot",
    "🎭 *مولانا:*\n«هر که را اسرار حق آموختند / مهر کردند و دهانش دوختند»\n🕌 @HajAliBot",
    "🎭 *صائب:*\n«به راه عشق نتوان پی به سر منزل مقصود»\n🕌 @HajAliBot",
    "🎭 *حافظ:*\n«دوش دیدم که ملائک در میخانه زدند»\n🕌 @HajAliBot",
    "🎭 *فردوسی:*\n«توانا بود هر که دانا بود»\n🕌 @HajAliBot",
    "🎭 *سعدی:*\n«درخت دوستی بنشان که کام دل به بار آرد»\n🕌 @HajAliBot",
    "🎭 *حافظ:*\n«رسید مژده که آمد بهار و سبزه دمید»\n🕌 @HajAliBot",
    "🎭 *مولانا:*\n«نیست در بازار عالم خوشتر از سودای عشق»\n🕌 @HajAliBot",
    "🎭 *حافظ:*\n«بیا که قصر امل سخت سست بنیاد است»\n🕌 @HajAliBot",
    "🎭 *سعدی:*\n«اگر خواهی که نفروشد دلت از مهر جانان را»\n🕌 @HajAliBot",
    "🎭 *حافظ:*\n«در ازل پرتو حسنت ز تجلی دم زد»\n🕌 @HajAliBot"
]

# ==================== نصایح (۱۵ عدد) ====================
NASIHAT = [
    "📖 *نصیحت:*\n«اِنَّ اللّهَ مَعَ الصّابِرینَ»\n🔹 خدا با صابران است.\n📖 بقره ۱۵۳\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«وَ مَنْ يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\n🔹 توکل کن، خدا کافی است.\n📖 طلاق ۳\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«اِنَّ مَعَ الْعُسْرِ يُسْراً»\n🔹 با سختی آسانی است.\n📖 شرح ۶\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«فَاذْكُرُونِي أَذْكُرْكُمْ»\n🔹 مرا یاد کنید تا یادتان کنم.\n📖 بقره ۱۵۲\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«وَ قُولُوا لِلنّاسِ حُسْناً»\n🔹 به مردم سخن نیک بگویید.\n📖 بقره ۸۳\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«اِنَّ اللّهَ يُحِبُّ الْمُحْسِنينَ»\n🔹 خدا نیکوکاران را دوست دارد.\n📖 بقره ۱۹۵\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«وَ اَحْسِنْ كَما اَحْسَنَ اللّهُ اِلَيْكَ»\n🔹 نیکی کن چنان که خدا به تو نیکی کرد.\n📖 قصص ۷۷\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«اِدْفَعْ بِالَّتي هِيَ اَحْسَنُ»\n🔹 بدی را با خوبی دفع کن.\n📖 مؤمنون ۹۶\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«اِنَّ الصَّلاةَ تَنْهى عَنِ الْفَحْشاءِ»\n🔹 نماز از زشتی باز می‌دارد.\n📖 عنکبوت ۴۵\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«وَ لا تَيْأَسُوا مِنْ رَوْحِ اللّهِ»\n🔹 از رحمت خدا ناامید نشوید.\n📖 یوسف ۸۷\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«وَ مَنْ اَحْياها فَكَاَنَّما اَحْيَا النّاسَ جَميعاً»\n🔹 هر که نفسی را زنده کند گویا همه را زنده کرده.\n📖 مائده ۳۲\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«اِنْ اَحْسَنْتُمْ اَحْسَنْتُمْ لاَِنْفُسِكُمْ»\n🔹 اگر نیکی کنید به خود کرده‌اید.\n📖 اسراء ۷\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«اِذا قيلَ لَكُمْ تَفَسَّحوا فَافْسَحوا»\n🔹 وقتی گفتند جا باز کنید، باز کنید.\n📖 مجادله ۱۱\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«يَرْفَعِ اللّهُ الَّذينَ آمَنوا مِنْكُمْ»\n🔹 خدا مؤمنان را بالا می‌برد.\n📖 مجادله ۱۱\n🕌 @HajAliBot",
    "📖 *نصیحت:*\n«وَ جَزاءُ سَيِّئَةٍ سَيِّئَةٌ مِثْلُها»\n🔹 جزای بدی مثل آن است.\n📖 شوری ۴۰\n🕌 @HajAliBot"
]

# ==================== ذکر روز ====================
AZKAR_ROOZ = {
    0: "📿 *شنبه:* یا رَبَّ الْعالَمین (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    1: "📿 *یکشنبه:* یا ذَاالْجَلالِ وَالاِْکْرام (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    2: "📿 *دوشنبه:* یا قاضِیَ الْحاجات (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    3: "📿 *سه‌شنبه:* یا اَرْحَمَ الرّاحِمین (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    4: "📿 *چهارشنبه:* یا حَیُّ یا قَیّوم (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    5: "📿 *پنج‌شنبه:* لا اِلهَ اِلاَّ اللّهُ (۱۰۰ مرتبه)\n🕌 @HajAliBot",
    6: "📿 *جمعه:* اللّهُمَّ صَلِّ عَلی مُحَمَّد وَ آلِ مُحَمَّد (۱۰۰ مرتبه)\n🕌 @HajAliBot"
}

# ==================== مداحی (۱۰ عدد) ====================
MADAHI = [
    "🎧 *مداحی:* حاج محمود کریمی - امیر بی‌نشان\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج میثم مطیعی - ای اهل حرم\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج حسن خلج - علی مولا\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج سعید حدادیان - یا حسین\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج عبدالرضا هلالی - زهرا\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج محمد طاهری - غریب مادر\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج مهدی رسولی - ارباب\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج محسن عرب‌خالقی - فاطمیه\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج جواد مقدم - محرم\n🕌 @HajAliBot",
    "🎧 *مداحی:* حاج علی کرمی - یا زهرا\n🕌 @HajAliBot"
]

# ==================== کلیپ (۱۰ عدد) ====================
CLIPS = [
    "📹 *کلیپ:* لحظه اذان حرم امام رضا\n🕌 @HajAliBot",
    "📹 *کلیپ:* زیارت اربعین\n🕌 @HajAliBot",
    "📹 *کلیپ:* نماز جماعت در حرم\n🕌 @HajAliBot",
    "📹 *کلیپ:* ذکر مصیبت محرم\n🕌 @HajAliBot",
    "📹 *کلیپ:* روضه خانگی\n🕌 @HajAliBot",
    "📹 *کلیپ:* دعای کمیل\n🕌 @HajAliBot",
    "📹 *کلیپ:* جشن ولادت\n🕌 @HajAliBot",
    "📹 *کلیپ:* سینه‌زنی سنتی\n🕌 @HajAliBot",
    "📹 *کلیپ:* نوحه خوانی\n🕌 @HajAliBot",
    "📹 *کلیپ:* سلام به امام حسین\n🕌 @HajAliBot"
]

# ==================== مناسبت‌ها ====================
MONASEBAT = [
    (1, 10, "🏴 شهادت حضرت زهرا (س) - تسلیت\n🕌 @HajAliBot"),
    (1, 13, "🏴 رحلت حضرت ام‌البنین (س)\n🕌 @HajAliBot"),
    (3, 15, "🎉 ولادت امام حسن مجتبی (ع)\n🕌 @HajAliBot"),
    (4, 20, "🏴 شهادت امام حسین (ع) - عاشورا\n🕌 @HajAliBot"),
    (6, 17, "🎉 ولادت امام رضا (ع)\n🕌 @HajAliBot"),
    (9, 15, "🎉 ولادت امام زمان (عج)\n🕌 @HajAliBot"),
    (10, 20, "🏴 شهادت امام حسن عسکری (ع)\n🕌 @HajAliBot"),
    (11, 5, "🎉 ولادت حضرت زینب (س)\n🕌 @HajAliBot"),
    (12, 9, "🏴 شهادت امام حسن عسکری (ع)\n🕌 @HajAliBot"),
    (12, 17, "🎉 ولادت پیامبر اکرم (ص)\n🕌 @HajAliBot")
]

# ==================== تبلیغ کانال ====================
CHANNEL_AD = f"📢 *کانال ما:*\n{YOUR_CHANNEL}\n🔹 احادیث | مداحی | کلیپ | مطالب مذهبی\n🕌 @HajAliBot"

# ==================== اوقات شرعی ====================
AWQAT = [
    (4, 30, "🕌 اذان صبح\n🕌 @HajAliBot"),
    (12, 0, "🕌 اذان ظهر\n🕌 @HajAliBot"),
    (15, 30, "🕌 اذان عصر\n🕌 @HajAliBot"),
    (18, 0, "🕌 اذان مغرب\n🕌 @HajAliBot"),
    (19, 30, "🕌 اذان عشاء\n🕌 @HajAliBot")
]

# ==================== شاخص ====================
hi = si = pi = ni = 0

# ==================== دستورات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"🏴 *اَلسَّلامُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n\n"
        f"✨ سلام {u.first_name} عزیز\n\n"
        f"🤖 *حاج علی* در خدمت شما\n\n"
        f"/hadis | /salavat | /poem | /nasihat\n"
        f"/zekr | /madahi | /clip | /channel\n\n"
        f"🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 /hadis /salavat /poem /nasihat /zekr /madahi /clip /channel", parse_mode='Markdown')

async def hadis(update, context):
    global hi
    t = AHADITH[hi % len(AHADITH)]; hi += 1
    await update.message.reply_text(t, parse_mode='Markdown')

async def salavat(update, context):
    global si
    t = SALAVAT[si % len(SALAVAT)]; si += 1
    await update.message.reply_text(t, parse_mode='Markdown')

async def poem(update, context):
    global pi
    t = POEMS[pi % len(POEMS)]; pi += 1
    await update.message.reply_text(t, parse_mode='Markdown')

async def nasihat(update, context):
    global ni
    t = NASIHAT[ni % len(NASIHAT)]; ni += 1
    await update.message.reply_text(t, parse_mode='Markdown')

async def zekr(update, context):
    await update.message.reply_text(AZKAR_ROOZ[datetime.now().weekday()], parse_mode='Markdown')

async def madahi(update, context):
    await update.message.reply_text(random.choice(MADAHI), parse_mode='Markdown')

async def clip(update, context):
    await update.message.reply_text(random.choice(CLIPS), parse_mode='Markdown')

async def channel(update, context):
    await update.message.reply_text(CHANNEL_AD, parse_mode='Markdown')

async def welcome_new(update, context):
    for m in update.message.new_chat_members:
        await update.message.reply_text(f"🏴 سلام {m.first_name} عزیز\n{random.choice(POEMS)}", parse_mode='Markdown')

async def group_msg(update, context):
    t = update.message.text.lower()
    global hi, si, pi, ni
    if "صلوات" in t:
        r = SALAVAT[si % len(SALAVAT)]; si += 1
    elif "حدیث" in t:
        r = AHADITH[hi % len(AHADITH)]; hi += 1
    elif "شعر" in t:
        r = POEMS[pi % len(POEMS)]; pi += 1
    elif "نصیحت" in t or "آیه" in t:
        r = NASIHAT[ni % len(NASIHAT)]; ni += 1
    elif "مداحی" in t:
        r = random.choice(MADAHI)
    elif "کلیپ" in t:
        r = random.choice(CLIPS)
    elif "امام زمان" in t or "مهدی" in t:
        r = "🌹 اللَّهُمَّ عَجِّلْ لِوَلِیِّکَ الْفَرَج\n🕌 @HajAliBot"
    elif "سلام" in t and len(t) < 10:
        r = "🏴 علیکم السلام\n🕌 @HajAliBot"
    else: return
    await update.message.reply_text(r, parse_mode='Markdown')

# ==================== ارسال خودکار ====================
async def a_hadis(context):
    global hi
    t = AHADITH[hi % len(AHADITH)]; hi += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ حدیث:\n{t}", parse_mode='Markdown')
    except: pass

async def a_salavat(context):
    global si
    t = SALAVAT[si % len(SALAVAT)]; si += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ صلوات:\n{t}", parse_mode='Markdown')
    except: pass

async def a_poem(context):
    global pi
    t = POEMS[pi % len(POEMS)]; pi += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ شعر:\n{t}", parse_mode='Markdown')
    except: pass

async def a_nasihat(context):
    global ni
    t = NASIHAT[ni % len(NASIHAT)]; ni += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ نصیحت:\n{t}", parse_mode='Markdown')
    except: pass

async def a_zekr(context):
    try: await context.bot.send_message(ADMIN_ID, AZKAR_ROOZ[datetime.now().weekday()], parse_mode='Markdown')
    except: pass

async def a_azan(context):
    n = datetime.now()
    for h, m, msg in AWQAT:
        if n.hour == h and n.minute == m:
            try: await context.bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
            except: pass

async def a_monasebat(context):
    n = datetime.now()
    for m, d, msg in MONASEBAT:
        if n.month == m and n.day == d:
            try: await context.bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
            except: pass

async def a_channel(context):
    try: await context.bot.send_message(ADMIN_ID, CHANNEL_AD, parse_mode='Markdown')
    except: pass

# ==================== اجرا ====================
def main():
    app = Application.builder().token(TOKEN).build()
    
    for cmd, func in [("start", start), ("help", help_command), ("hadis", hadis), ("salavat", salavat),
                       ("poem", poem), ("nasihat", nasihat), ("zekr", zekr), ("madahi", madahi),
                       ("clip", clip), ("channel", channel)]:
        app.add_handler(CommandHandler(cmd, func))
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, group_msg))
    
    jq = app.job_queue
    jq.run_repeating(a_hadis, interval=3600, first=10)
    jq.run_repeating(a_salavat, interval=1200, first=30)
    jq.run_repeating(a_poem, interval=3600, first=60)
    jq.run_repeating(a_nasihat, interval=3600, first=120)
    jq.run_repeating(a_zekr, interval=7200, first=180)
    jq.run_repeating(a_azan, interval=60, first=10)
    jq.run_repeating(a_monasebat, interval=86400, first=10)
    jq.run_repeating(a_channel, interval=18000, first=300)
    
    print("🏴 حاج علی روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()    

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
# =================================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== احادیث ====================
AHADITH = [
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلْعِلْمُ وِراثَةٌ كَریمَةٌ»\n🔹 دانش میراثی گرانبهاست.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اَلْكَمَالُ التَّفَقُّهُ فِي الدِّينِ وَ الصَّبْرُ»\n🔹 کمال در فهم دین و صبر است.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«اَلْمُؤْمِنُ مِرْآةُ الْمُؤْمِنِ»\n🔹 مؤمن آینه مؤمن است.\n📖 بحارالأنوار\n🕌 @HajAliBot",
    "📚 *امام باقر (ع):*\n«مَنْ سَاءَ خُلُقُهُ عَذَّبَ نَفْسَهُ»\n🔹 بداخلاق خودش را عذاب می‌دهد.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«الصَّبْرُ مِنَ الاْيمانِ كَالرَّأْسِ مِنَ الْجَسَدِ»\n🔹 صبر مانند سر برای بدن است.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *امام حسن عسکری (ع):*\n«خَصْلَتانِ: اَلاْیمانُ بِاللّهِ وَ نَفْعُ الاِْخْوانِ»\n🔹 ایمان و سود رساندن.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام صادق (ع):*\n«اِنَّ اَحَبَّ اِخْوَانِي مَنْ اَهْدَى اِلَيَّ عُيُوبِي»\n🔹 بهترین برادر.\n📖 الکافی\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«مَنْ اَصْلَحَ سَريرَتَهُ اَصْلَحَ اللّهُ عَلانِيَتَهُ»\n🔹 اصلاح درون.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *علامه طباطبایی:*\n«اسلام دین فطرت است.»\n📖 المیزان\n🕌 @HajAliBot",
    "📚 *علامه طباطبایی:*\n«حقیقت عبادت اظهار بندگی است.»\n📖 المیزان\n🕌 @HajAliBot",
    "📚 *امام کاظم (ع):*\n«اَفْضَلُ الْعِبادَةِ اِنْتِظارُ الْفَرَجِ»\n🔹 انتظار فرج.\n📖 تحف العقول\n🕌 @HajAliBot",
    "📚 *امام رضا (ع):*\n«مَنْ لَمْ يَشْكُرِ الْمُنْعِمَ لَمْ يَشْكُرِ اللّهَ»\n🔹 تشکر.\n📖 عیون\n🕌 @HajAliBot",
    "📚 *امام جواد (ع):*\n«اَلتَّواضُعُ زينَةُ الْحَسَبِ»\n🔹 تواضع.\n📖 کشف الغمه\n🕌 @HajAliBot",
    "📚 *امیرالمؤمنین علی (ع):*\n«اَلْفَقْرُ فِى الْوَطَنِ غُرْبَةٌ»\n🔹 فقر در وطن.\n📖 نهج‌البلاغه\n🕌 @HajAliBot",
    "📚 *پیامبر اکرم (ص):*\n«طَلَبُ الْعِلْمِ فَريضَةٌ»\n🔹 طلب علم.\n📖 بحار\n🕌 @HajAliBot"
]

# ==================== صلوات ====================
SALAVAT = [
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّدٍ وَ آلِ مُحَمَّدٍ وَ عَجِّلْ فَرَجَهُمْ*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اَللّهُمَّ عَجِّل لِوَلیِّکَ الفَرَج*\n🤲 برای ظهور\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ كُنْ لِوَلِيِّكَ الحُجَّةِ*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *السَّلامُ عَلَی المَهْدِیِّ*\n🤲 سلام بر امام عصر\n🕌 @HajAliBot",
    "🌹 *صَلَّی اللّهُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n🤲 سلام بر حسین\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی فاطِمَةَ*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ صَلِّ عَلَی الرِّضا*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ اهْدِ قُلوبَنا*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ بارِکْ لَنا*\n🤲 صلوات\n🕌 @HajAliBot",
    "🌹 *اللَّهُمَّ اغْفِرْ لَنا*\n🤲 صلوات\n🕌 @HajAliBot"
]

# ==================== اشعار ====================
POEMS = [
    "🎭 *حافظ:* «یوسف گمگشته باز آید»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «هر کسی کو دور ماند»\n🕌 @HajAliBot",
    "🎭 *شهریار:* «علی ای همای رحمت»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «بنی آدم اعضای یکدیگرند»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «در اندرون من خسته دل»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «هر که را اسرار حق آموختند»\n🕌 @HajAliBot",
    "🎭 *صائب:* «به راه عشق نتوان پی»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «دوش دیدم که ملائک»\n🕌 @HajAliBot",
    "🎭 *فردوسی:* «توانا بود هر که دانا بود»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «درخت دوستی بنشان»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «رسید مژده که آمد بهار»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «نیست در بازار عالم»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «بیا که قصر امل»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «اگر خواهی که نفروشد»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «در ازل پرتو حسنت»\n🕌 @HajAliBot"
]

# ==================== نصایح ====================
NASIHAT = [
    "📖 «اِنَّ اللّهَ مَعَ الصّابِرینَ»\n🔹 خدا با صابران است.\n📖 بقره ۱۵۳\n🕌 @HajAliBot",
    "📖 «وَ مَنْ يَتَوَكَّلْ»\n🔹 توکل کن.\n📖 طلاق ۳\n🕌 @HajAliBot",
    "📖 «اِنَّ مَعَ الْعُسْرِ يُسْراً»\n🔹 آسانی بعد سختی.\n📖 شرح ۶\n🕌 @HajAliBot",
    "📖 «فَاذْكُرُونِي أَذْكُرْكُمْ»\n🔹 یادم کن.\n📖 بقره ۱۵۲\n🕌 @HajAliBot",
    "📖 «وَ قُولُوا لِلنّاسِ حُسْناً»\n🔹 سخن نیک.\n📖 بقره ۸۳\n🕌 @HajAliBot",
    "📖 «اِنَّ اللّهَ يُحِبُّ الْمُحْسِنينَ»\n🔹 خدا نیکوکاران را دوست دارد.\n📖 بقره ۱۹۵\n🕌 @HajAliBot",
    "📖 «وَ اَحْسِنْ كَما اَحْسَنَ اللّهُ»\n🔹 نیکی کن.\n📖 قصص ۷۷\n🕌 @HajAliBot",
    "📖 «اِدْفَعْ بِالَّتي هِيَ اَحْسَنُ»\n🔹 بدی را با خوبی.\n📖 مؤمنون ۹۶\n🕌 @HajAliBot",
    "📖 «اِنَّ الصَّلاةَ تَنْهى»\n🔹 نماز.\n📖 عنکبوت ۴۵\n🕌 @HajAliBot",
    "📖 «وَ لا تَيْأَسُوا»\n🔹 ناامید نشو.\n📖 یوسف ۸۷\n🕌 @HajAliBot"
]

# ==================== ذکر روز ====================
AZKAR_ROOZ = {
    0: "📿 *شنبه:* یا رَبَّ الْعالَمین\n🕌 @HajAliBot",
    1: "📿 *یکشنبه:* یا ذَاالْجَلالِ\n🕌 @HajAliBot",
    2: "📿 *دوشنبه:* یا قاضِیَ الْحاجات\n🕌 @HajAliBot",
    3: "📿 *سه‌شنبه:* یا اَرْحَمَ الرّاحِمین\n🕌 @HajAliBot",
    4: "📿 *چهارشنبه:* یا حَیُّ یا قَیّوم\n🕌 @HajAliBot",
    5: "📿 *پنج‌شنبه:* لا اِلهَ اِلاَّ اللّهُ\n🕌 @HajAliBot",
    6: "📿 *جمعه:* اللّهُمَّ صَلِّ عَلی مُحَمَّد\n🕌 @HajAliBot"
}

# ==================== مناسبت‌ها ====================
MONASEBAT = [
    (1, 10, "🏴 شهادت حضرت زهرا (س)\n🕌 @HajAliBot"),
    (3, 15, "🎉 ولادت امام حسن (ع)\n🕌 @HajAliBot"),
    (6, 17, "🎉 ولادت امام رضا (ع)\n🕌 @HajAliBot"),
    (9, 15, "🎉 ولادت امام زمان (عج)\n🕌 @HajAliBot"),
    (12, 17, "🎉 ولادت پیامبر (ص)\n🕌 @HajAliBot")
]

# ==================== تبلیغ کانال ====================
CHANNEL_AD = f"📢 *کانال ما:*\n{YOUR_CHANNEL}\n🔹 احادیث | مداحی | کلیپ\n🕌 @HajAliBot"

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

# ==================== گرفتن فایل از کانال ====================
async def get_random_media(context, media_type="all"):
    """برداشتن تصادفی مداحی یا کلیپ از کانال"""
    try:
        messages = []
        async for msg in context.bot.get_chat_history(CHANNEL_ID, limit=50):
            if media_type == "voice" and (msg.voice or msg.audio):
                messages.append(msg)
            elif media_type == "video" and (msg.video or msg.animation or msg.video_note):
                messages.append(msg)
            elif media_type == "all" and (msg.voice or msg.audio or msg.video or msg.animation or msg.document):
                messages.append(msg)
        if messages:
            return random.choice(messages)
    except:
        pass
    return None

# ==================== دستورات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"🏴 *سلام {u.first_name}*\n\n"
        f"🤖 حاج علی\n"
        f"/hadis | /salavat | /poem | /nasihat\n"
        f"/zekr | /madahi | /clip | /channel\n\n"
        f"🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def help_command(update, context):
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

async def madahi(update: Update, context):
    msg = await get_random_media(context, "voice")
    if msg:
        try:
            await msg.forward(update.effective_chat.id)
            return
        except:
            pass
    await update.message.reply_text("🎧 مداحی پیدا نشد.\n🕌 @HajAliBot")

async def clip(update: Update, context):
    msg = await get_random_media(context, "video")
    if msg:
        try:
            await msg.forward(update.effective_chat.id)
            return
        except:
            pass
    await update.message.reply_text("📹 کلیپی پیدا نشد.\n🕌 @HajAliBot")

async def channel(update, context):
    await update.message.reply_text(CHANNEL_AD, parse_mode='Markdown')

async def welcome_new(update, context):
    for m in update.message.new_chat_members:
        await update.message.reply_text(f"🏴 سلام {m.first_name}\n{random.choice(POEMS)}", parse_mode='Markdown')

async def group_msg(update: Update, context):
    t = update.message.text.lower()
    global hi, si, pi, ni
    
    if "صلوات" in t:
        r = SALAVAT[si % len(SALAVAT)]; si += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "حدیث" in t:
        r = AHADITH[hi % len(AHADITH)]; hi += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "شعر" in t:
        r = POEMS[pi % len(POEMS)]; pi += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "نصیحت" in t or "آیه" in t:
        r = NASIHAT[ni % len(NASIHAT)]; ni += 1
        await update.message.reply_text(r, parse_mode='Markdown')
    elif "مداحی" in t or "صوت" in t or "صدا" in t:
        msg = await get_random_media(context, "voice")
        if msg:
            try:
                await msg.forward(update.effective_chat.id)
                return
            except:
                pass
        await update.message.reply_text("🎧 مداحی پیدا نشد.\n🕌 @HajAliBot")
    elif "کلیپ" in t or "فیلم" in t or "ویدیو" in t:
        msg = await get_random_media(context, "video")
        if msg:
            try:
                await msg.forward(update.effective_chat.id)
                return
            except:
                pass
        await update.message.reply_text("📹 کلیپی پیدا نشد.\n🕌 @HajAliBot")
    elif "امام زمان" in t or "مهدی" in t:
        await update.message.reply_text("🌹 اللَّهُمَّ عَجِّلْ لِوَلِیِّکَ الْفَرَج\n🕌 @HajAliBot", parse_mode='Markdown')
    elif "سلام" in t and len(t) < 10:
        await update.message.reply_text("🏴 علیکم السلام\n🕌 @HajAliBot", parse_mode='Markdown')

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

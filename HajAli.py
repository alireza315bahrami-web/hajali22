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
    "🌹 *صَلَّی اللّهُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n🤲 سلام بر حسین\n🕌 @HajAliBot"
]

# ==================== اشعار ====================
POEMS = [
    "🎭 *حافظ:* «یوسف گمگشته باز آید»\n🕌 @HajAliBot",
    "🎭 *مولانا:* «هر کسی کو دور ماند»\n🕌 @HajAliBot",
    "🎭 *شهریار:* «علی ای همای رحمت»\n🕌 @HajAliBot",
    "🎭 *سعدی:* «بنی آدم اعضای یکدیگرند»\n🕌 @HajAliBot",
    "🎭 *حافظ:* «در اندرون من خسته دل»\n🕌 @HajAliBot"
]

# ==================== نصایح ====================
NASIHAT = [
    "📖 «اِنَّ اللّهَ مَعَ الصّابِرینَ»\n🔹 خدا با صابران است.\n📖 بقره ۱۵۳\n🕌 @HajAliBot",
    "📖 «وَ مَنْ يَتَوَكَّلْ»\n🔹 توکل کن.\n📖 طلاق ۳\n🕌 @HajAliBot",
    "📖 «اِنَّ مَعَ الْعُسْرِ يُسْراً»\n🔹 آسانی بعد سختی.\n📖 شرح ۶\n🕌 @HajAliBot",
    "📖 «فَاذْكُرُونِي أَذْكُرْكُمْ»\n🔹 یادم کن.\n📖 بقره ۱۵۲\n🕌 @HajAliBot",
    "📖 «وَ قُولُوا لِلنّاسِ حُسْناً»\n🔹 سخن نیک.\n📖 بقره ۸۳\n🕌 @HajAliBot"
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

# ==================== تبلیغ کانال ====================
CHANNEL_AD = f"📢 *کانال ما:*\n{YOUR_CHANNEL}\n🔹 احادیث | کلیپ | مطالب مذهبی\n🕌 @HajAliBot"

# ==================== شاخص ====================
hi = si = pi = ni = 0

# ==================== گرفتن کلیپ از کانال ====================
async def get_random_clip(context):
    try:
        messages = []
        async for msg in context.bot.get_chat_history(CHANNEL_ID, limit=100):
            if msg.video or msg.animation or msg.video_note:
                messages.append(msg)
        if messages:
            return random.choice(messages)
    except Exception as e:
        logger.error(f"Error getting clip: {e}")
    return None

# ==================== دستورات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"🏴 *سلام {u.first_name}*\n\n"
        f"🤖 حاج علی\n"
        f"/hadis | /salavat | /poem | /nasihat\n"
        f"/zekr | /clip | /channel\n\n"
        f"🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def help_command(update, context):
    await update.message.reply_text("📚 /hadis /salavat /poem /nasihat /zekr /clip /channel", parse_mode='Markdown')

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

async def clip(update: Update, context):
    await update.message.reply_text("🔍 در حال جستجوی کلیپ...")
    msg = await get_random_clip(context)
    if msg:
        try:
            await msg.forward(update.effective_chat.id)
            return
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در ارسال کلیپ: {e}")
    else:
        await update.message.reply_text("📹 کلیپی در کانال پیدا نشد.\n🕌 @HajAliBot")

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
    elif "کلیپ" in t or "فیلم" in t or "ویدیو" in t:
        await update.message.reply_text("🔍 در حال جستجوی کلیپ...")
        msg = await get_random_clip(context)
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
async def auto_hadis(context):
    global hi
    t = AHADITH[hi % len(AHADITH)]; hi += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ حدیث:\n{t}", parse_mode='Markdown')
    except: pass

async def auto_salavat(context):
    global si
    t = SALAVAT[si % len(SALAVAT)]; si += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ صلوات:\n{t}", parse_mode='Markdown')
    except: pass

async def auto_poem(context):
    global pi
    t = POEMS[pi % len(POEMS)]; pi += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ شعر:\n{t}", parse_mode='Markdown')
    except: pass

async def auto_nasihat(context):
    global ni
    t = NASIHAT[ni % len(NASIHAT)]; ni += 1
    try: await context.bot.send_message(ADMIN_ID, f"⏰ نصیحت:\n{t}", parse_mode='Markdown')
    except: pass

async def auto_zekr(context):
    try: await context.bot.send_message(ADMIN_ID, AZKAR_ROOZ[datetime.now().weekday()], parse_mode='Markdown')
    except: pass

async def auto_channel(context):
    try: await context.bot.send_message(ADMIN_ID, CHANNEL_AD, parse_mode='Markdown')
    except: pass

# ==================== اجرا ====================
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hadis", hadis))
    app.add_handler(CommandHandler("salavat", salavat))
    app.add_handler(CommandHandler("poem", poem))
    app.add_handler(CommandHandler("nasihat", nasihat))
    app.add_handler(CommandHandler("zekr", zekr))
    app.add_handler(CommandHandler("clip", clip))
    app.add_handler(CommandHandler("channel", channel))
    
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

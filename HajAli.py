import random
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== تنظیمات ====================
TOKEN = "8810239565:AAFtU28AaBDYzVZW-qy8_rOW2yIqCnWDWhM"
ADMIN_ID = 7443695973
# =================================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== لیست احادیث ====================
AHADITH = [
    "📚 *امیرالمؤمنین علی (ع):*\n\n«اَلْعِلْمُ وِراثَةٌ كَریمَةٌ، وَ الاَْدَبُ حُلَلٌ مُجَدَّدَةٌ»\n\n🔹 *ترجمه:* دانش میراثی گرانبهاست و ادب لباسی نو و زیباست.\n\n📖 نهج‌البلاغه، حکمت ۵\n\n🕌 @HajAliBot",
    
    "📚 *امیرالمؤمنین علی (ع):*\n\n«اَلصَّبْرُ مِنَ الاْيمانِ كَالرَّأْسِ مِنَ الْجَسَدِ»\n\n🔹 *ترجمه:* صبر نسبت به ایمان، مانند سر نسبت به بدن است.\n\n📖 نهج‌البلاغه، حکمت ۸۲\n\n🕌 @HajAliBot",
    
    "📚 *امام صادق (ع):*\n\n«اَلْكَمَالُ كُلُّ الْكَمَالِ اَلتَّفَقُّهُ فِي الدِّينِ وَ الصَّبْرُ عَلَى النَّائِبَةِ وَ تَقْدِيرُ الْمَعِيشَةِ»\n\n🔹 *ترجمه:* تمام کمال در فهم دین و صبر بر مصیبت و اندازه‌گیری در زندگی است.\n\n📖 الکافی، جلد ۱\n\n🕌 @HajAliBot",
    
    "📚 *امام باقر (ع):*\n\n«مَنْ سَاءَ خُلُقُهُ عَذَّبَ نَفْسَهُ»\n\n🔹 *ترجمه:* هر که بداخلاق باشد، خودش را عذاب می‌دهد.\n\n📖 الکافی، جلد ۲\n\n🕌 @HajAliBot",
    
    "📚 *پیامبر اکرم (ص):*\n\n«اَلْمُؤْمِنُ مِرْآةُ الْمُؤْمِنِ»\n\n🔹 *ترجمه:* مؤمن آینه مؤمن است.\n\n📖 بحارالأنوار، جلد ۷۴\n\n🕌 @HajAliBot",
    
    "📚 *امیرالمؤمنین علی (ع):*\n\n«مَنْ اَصْلَحَ سَريرَتَهُ اَصْلَحَ اللّهُ عَلانِيَتَهُ»\n\n🔹 *ترجمه:* هر که درون خود را اصلاح کند، خداوند ظاهرش را اصلاح می‌کند.\n\n📖 نهج‌البلاغه، حکمت ۴۲۳\n\n🕌 @HajAliBot",
    
    "📚 *امام صادق (ع):*\n\n«اِنَّ اَحَبَّ اِخْوَانِي اِلَيَّ مَنْ اَهْدَى اِلَيَّ عُيُوبِي»\n\n🔹 *ترجمه:* محبوب‌ترین برادرانم نزد من کسی است که عیب‌هایم را به من هدیه کند.\n\n📖 الکافی، جلد ۲\n\n🕌 @HajAliBot",
    
    "📚 *علامه طباطبایی (ره):*\n\n«اسلام دین فطرت است و تمام دستورات آن با فطرت انسانی سازگار می‌باشد.»\n\n📖 تفسیر المیزان، جلد ۱\n\n🕌 @HajAliBot",
    
    "📚 *علامه طباطبایی (ره):*\n\n«حقیقت عبادت، اظهار بندگی و فقر به درگاه الهی است.»\n\n📖 تفسیر المیزان، جلد ۴\n\n🕌 @HajAliBot",
    
    "📚 *امیرالمؤمنین علی (ع):*\n\n«خالِطُوا النّاسَ بِاَلْسِنَتِكُمْ وَ اَجْسادِكُمْ، وَ زايِلُوهُمْ بِقُلُوبِكُمْ وَ اَعْمالِكُمْ»\n\n🔹 *ترجمه:* با مردم با زبان و بدن خود همراه شوید ولی با قلب و اعمالتان از آنان جدا باشید.\n\n📖 نهج‌البلاغه، حکمت ۱۰\n\n🕌 @HajAliBot",
    
    "📚 *امیرالمؤمنین علی (ع):*\n\n«اَلْفَقْرُ فِى الْوَطَنِ غُرْبَةٌ، وَ الْغِنى فِى الْغُرْبَةِ وَطَنٌ»\n\n🔹 *ترجمه:* فقر در وطن غربت است و بی‌نیازی در غربت وطن.\n\n📖 نهج‌البلاغه، حکمت ۵۶\n\n🕌 @HajAliBot",
    
    "📚 *امام حسن عسکری (ع):*\n\n«خَصْلَتانِ لَيْسَ فَوْقَهُما شَیءٌ: اَلاْیمانُ بِاللّهِ وَ نَفْعُ الاِْخْوانِ»\n\n🔹 *ترجمه:* دو خصلت است که بالاتر از آن چیزی نیست: ایمان به خدا و سود رساندن به برادران.\n\n📖 تحف العقول\n\n🕌 @HajAliBot"
]

# ==================== لیست صلوات ====================
SALAVAT = [
    "🌹 *اللَّهُمَّ صَلِّ عَلَی مُحَمَّدٍ وَ آلِ مُحَمَّدٍ وَ عَجِّلْ فَرَجَهُمْ*\n\n🤲 برای سلامتی و تعجیل در ظهور امام زمان (عج) صلوات\n\n🕌 @HajAliBot",
    
    "🌹 *اللَّهُمَّ كُنْ لِوَلِيِّكَ الحُجَّةِ بنِ الحَسَن*\n\n🤲 صلوات برای فرج آقا امام زمان (عج)\n\n🕌 @HajAliBot",
    
    "🌹 *اَللّهُمَّ عَجِّل لِوَلیِّکَ الفَرَج*\n\n🤲 برای ظهور مولایمان دعا کنیم\n\n🕌 @HajAliBot",
    
    "🌹 *السَّلامُ عَلَی المَهْدِیِّ الَّذِی وَعَدَ اللَّهُ بِهِ الأُمَم*\n\n🤲 صلوات برای امام عصر (عج)\n\n🕌 @HajAliBot",
    
    "🌹 *صَلَّی اللّهُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n\n🤲 ذکر مصیبت و سلام بر سیدالشهدا\n\n🕌 @HajAliBot"
]

# ==================== لیست اشعار ====================
POEMS = [
    "🎭 *مولانا:*\n«هر که را اسرار حق آموختند / مهر کردند و دهانش دوختند»\n\n🕌 @HajAliBot",
    
    "🎭 *حافظ:*\n«در اندرون من خسته دل ندانم کیست / که من خموشم و او در فغان و در غوغاست»\n\n🕌 @HajAliBot",
    
    "🎭 *سعدی:*\n«بنی آدم اعضای یکدیگرند / که در آفرینش ز یک گوهرند»\n\n🕌 @HajAliBot",
    
    "🎭 *شهریار:*\n«علی ای همای رحمت تو چه آیتی خدا را / که به ماسوا فکندی همه سایه هما را»\n\n🕌 @HajAliBot",
    
    "🎭 *حافظ:*\n«یوسف گمگشته باز آید به کنعان غم مخور / کلبه احزان شود روزی گلستان غم مخور»\n\n🕌 @HajAliBot",
    
    "🎭 *مولانا:*\n«هر کسی کو دور ماند از اصل خویش / باز جوید روزگار وصل خویش»\n\n🕌 @HajAliBot",
    
    "🎭 *صائب تبریزی:*\n«به راه عشق نتوان پی به سر منزل مقصود / که در هر گام می‌افتد هزاران جان گرامی‌ها»\n\n🕌 @HajAliBot",
    
    "🎭 *حافظ:*\n«دوش دیدم که ملائک در میخانه زدند / گل آدم بسرشتند و به پیمانه زدند»\n\n🕌 @HajAliBot"
]

# ==================== لیست نصایح ====================
NASIHAT = [
    "📖 *نصیحت قرآنی:*\n\n«اِنَّ اللّهَ مَعَ الصّابِرینَ»\n\n🔹 *ترجمه:* خداوند با صابران است.\n\n📖 سوره بقره، آیه ۱۵۳\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«وَ مَنْ يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ»\n\n🔹 *ترجمه:* هر که بر خدا توکل کند، خدا او را کافی است.\n\n📖 سوره طلاق، آیه ۳\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«اِنَّ مَعَ الْعُسْرِ يُسْراً»\n\n🔹 *ترجمه:* همانا با سختی، آسانی است.\n\n📖 سوره شرح، آیه ۶\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«فَاذْكُرُونِي أَذْكُرْكُمْ»\n\n🔹 *ترجمه:* پس مرا یاد کنید تا شما را یاد کنم.\n\n📖 سوره بقره، آیه ۱۵۲\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«وَ قُولُوا لِلنّاسِ حُسْناً»\n\n🔹 *ترجمه:* و به مردم سخن نیک بگویید.\n\n📖 سوره بقره، آیه ۸۳\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«اِنَّ اللّهَ يُحِبُّ الْمُحْسِنينَ»\n\n🔹 *ترجمه:* خداوند نیکوکاران را دوست دارد.\n\n📖 سوره بقره، آیه ۱۹۵\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«وَ اَحْسِنْ كَما اَحْسَنَ اللّهُ اِلَيْكَ»\n\n🔹 *ترجمه:* نیکی کن همان‌گونه که خدا به تو نیکی کرده است.\n\n📖 سوره قصص، آیه ۷۷\n\n🕌 @HajAliBot",
    
    "📖 *نصیحت قرآنی:*\n\n«اِدْفَعْ بِالَّتي هِيَ اَحْسَنُ»\n\n🔹 *ترجمه:* بدی را با آنچه نیکوتر است دفع کن.\n\n📖 سوره مؤمنون، آیه ۹۶\n\n🕌 @HajAliBot"
]

# ==================== خوش‌آمدگویی ====================
WELCOME_POEMS = [
    "🌟 خوش آمدید!\n\n🎭 *مولانا:*\n«هر کسی از ظن خود شد یار من / از درون من نجست اسرار من»\n\n🕌 @HajAliBot",
    
    "🌟 سلام بر شما!\n\n🎭 *حافظ:*\n«رسید مژده که آمد بهار و سبزه دمید / وظیفه گر برسد مصرفش گل است و نبید»\n\n🕌 @HajAliBot",
    
    "🌟 درود بر شما!\n\n🎭 *سعدی:*\n«درخت دوستی بنشان که کام دل به بار آرد / نهال دشمنی برکن که رنج بی‌شمار آرد»\n\n🕌 @HajAliBot"
]

# شاخص‌های چرخش
hadith_index = 0
salavat_index = 0
poem_index = 0
nasihat_index = 0

# ==================== دستورات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🏴 *اَلسَّلامُ عَلَیْکَ یا اَبا عَبْدِ اللّهِ*\n\n"
        f"✨ با عرض سلام و ادب خدمت {user.first_name} عزیز\n\n"
        f"🤖 من *حاج علی* هستم، ربات مذهبی و فرهنگی\n\n"
        f"📿 خدمات من:\n"
        f"🔸 احادیث معتبر با ترجمه\n"
        f"🔸 ذکر صلوات برای امام زمان (عج)\n"
        f"🔸 اشعار عرفانی و اخلاقی\n"
        f"🔸 نصایح قرآنی\n\n"
        f"📚 دستورات:\n"
        f"/start - شروع\n"
        f"/hadis - حدیث با ترجمه\n"
        f"/salavat - صلوات مخصوص\n"
        f"/poem - شعر تک بیتی\n"
        f"/nasihat - نصیحت قرآنی\n"
        f"/help - راهنما\n\n"
        f"🕌 *اللّهُمَّ عَجِّلْ لِوَلِیِّکَ الْفَرَج*\n\n"
        f"🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *راهنمای حاج علی:*\n\n"
        "/start - شروع و خوش‌آمدگویی\n"
        "/hadis - حدیث تصادفی با ترجمه\n"
        "/salavat - صلوات برای امام زمان\n"
        "/poem - شعر تک بیتی\n"
        "/nasihat - نصیحت قرآنی\n\n"
        "🕌 @HajAliBot",
        parse_mode='Markdown'
    )

async def hadis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hadith_index
    hadis_text = AHADITH[hadith_index % len(AHADITH)]
    hadith_index += 1
    await update.message.reply_text(hadis_text, parse_mode='Markdown')

async def salavat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global salavat_index
    salavat_text = SALAVAT[salavat_index % len(SALAVAT)]
    salavat_index += 1
    await update.message.reply_text(salavat_text, parse_mode='Markdown')

async def poem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global poem_index
    poem_text = POEMS[poem_index % len(POEMS)]
    poem_index += 1
    await update.message.reply_text(poem_text, parse_mode='Markdown')

async def nasihat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global nasihat_index
    nasihat_text = NASIHAT[nasihat_index % len(NASIHAT)]
    nasihat_index += 1
    await update.message.reply_text(nasihat_text, parse_mode='Markdown')

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        welcome_text = random.choice(WELCOME_POEMS)
        await update.message.reply_text(
            f"🏴 *سلام و درود بر {member.first_name} عزیز*\n\n{welcome_text}",
            parse_mode='Markdown'
        )

async def group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if "صلوات" in text:
        global salavat_index
        response = SALAVAT[salavat_index % len(SALAVAT)]
        salavat_index += 1
        await update.message.reply_text(response, parse_mode='Markdown')
    elif "حدیث" in text:
        global hadith_index
        response = AHADITH[hadith_index % len(AHADITH)]
        hadith_index += 1
        await update.message.reply_text(response, parse_mode='Markdown')
    elif "شعر" in text:
        global poem_index
        response = POEMS[poem_index % len(POEMS)]
        poem_index += 1
        await update.message.reply_text(response, parse_mode='Markdown')
    elif "نصیحت" in text or "آیه" in text:
        global nasihat_index
        response = NASIHAT[nasihat_index % len(NASIHAT)]
        nasihat_index += 1
        await update.message.reply_text(response, parse_mode='Markdown')
    elif "امام زمان" in text or "مهدی" in text:
        await update.message.reply_text(
            "🌹 *اللَّهُمَّ عَجِّلْ لِوَلِیِّکَ الْفَرَج*\n\n🤲 صلوات برای سلامتی آقا\n\n🕌 @HajAliBot",
            parse_mode='Markdown'
        )
    elif "سلام" in text and len(text) < 10:
        await update.message.reply_text(
            "🏴 *علیکم السلام و رحمة الله و برکاته*\n\n🕌 @HajAliBot",
            parse_mode='Markdown'
        )

# ==================== ارسال خودکار ====================
async def auto_hadis(context: ContextTypes.DEFAULT_TYPE):
    global hadith_index
    hadis_text = AHADITH[hadith_index % len(AHADITH)]
    hadith_index += 1
    try:
        await context.bot.send_message(ADMIN_ID, f"⏰ *حدیث ساعت:*\n\n{hadis_text}", parse_mode='Markdown')
    except:
        pass

async def auto_salavat(context: ContextTypes.DEFAULT_TYPE):
    global salavat_index
    salavat_text = SALAVAT[salavat_index % len(SALAVAT)]
    salavat_index += 1
    try:
        await context.bot.send_message(ADMIN_ID, f"⏰ *وقت صلوات:*\n\n{salavat_text}", parse_mode='Markdown')
    except:
        pass

async def auto_poem(context: ContextTypes.DEFAULT_TYPE):
    global poem_index
    poem_text = POEMS[poem_index % len(POEMS)]
    poem_index += 1
    try:
        await context.bot.send_message(ADMIN_ID, f"⏰ *شعر ساعت:*\n\n{poem_text}", parse_mode='Markdown')
    except:
        pass

async def auto_nasihat(context: ContextTypes.DEFAULT_TYPE):
    global nasihat_index
    nasihat_text = NASIHAT[nasihat_index % len(NASIHAT)]
    nasihat_index += 1
    try:
        await context.bot.send_message(ADMIN_ID, f"⏰ *نصیحت قرآنی:*\n\n{nasihat_text}", parse_mode='Markdown')
    except:
        pass

# ==================== اجرا ====================
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hadis", hadis))
    app.add_handler(CommandHandler("salavat", salavat))
    app.add_handler(CommandHandler("poem", poem))
    app.add_handler(CommandHandler("nasihat", nasihat))
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, group_message))
    
    job_queue = app.job_queue
    job_queue.run_repeating(auto_hadis, interval=3600, first=10)
    job_queue.run_repeating(auto_salavat, interval=1200, first=30)
    job_queue.run_repeating(auto_poem, interval=3600, first=60)
    job_queue.run_repeating(auto_nasihat, interval=3600, first=120)
    
    print("🏴 حاج علی روشن شد!")
    print("📚 در حال خدمت‌رسانی...")
    app.run_polling()

if __name__ == "__main__":
    main()

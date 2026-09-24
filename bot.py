import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# تفعيل سجل الأخطاء
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🛑 آي دي حسابك الأساسي فقط (المتحكم الوحيد والمالك)
OWNER_ID = 1837019378

# متغيرات الحالة والتحكم
bot_is_active = True
group_locked = False

# قائمة الكلمات المحظورة والسب (أداء عالي وسريع)
BAD_WORDS_SET = {
    "قحبة", "منيوك", "متناك", "متناكه", "عاهرة", "شرموطة", "شرموطه",
    "انيك", "كس", "كس امك", "كس اختك", "ابن الحرام", "قواد", "ديوث", "خول", "مخنث", "عرص",
    "سكس", "اباحي", "18+", "porno", "sex", "xx", "مقطع ساخن", "نيك", "جنس", "بورنو",
    "تهكير", "هكر", "اختراق", "ثغرة", "رابط مخترق"
}

SAD_WORDS = ["مضايق", "زعلان", "مقهور", "حزين", "مفجوع", "تعبان", "زهقان", "مخنوق", "أفف", "يارب", "هم"]


# 1. الترحيب بالأعضاء الجدد
async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_is_active:
        return
        
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
        
        fancy_welcome = (
            f"✨ **أهلاً بك يا ألق الحضور [{member.first_name}](tg://user?id={member.id}) في عائلتنا الملكية!** ✨\n\n"
            f"🌟 أنرت مجتمعنا بانضمامك، ونتمنى أن تجد بيننا كل فائدة ومتعة.\n"
            f"🛡 نرجو منك الالتزام بالقوانين العامة للحفاظ على بيئة نقية وراقية للجميع.\n\n"
            f"🌸 نتمنى لك إقامة طيبة وموفقة معنا!"
        )
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=fancy_welcome, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"خطأ في ترحيب الأعضاء: {e}")


# 2. الأوامر والتحكم (مخصصة لك وحدك)
async def bot_commands_and_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_is_active, group_locked
    if not update.message or not update.message.text:
        return
        
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    
    if user_id != OWNER_ID:
        return

    if text == "إيقاف البوت":
        bot_is_active = False
        await update.message.reply_text("🛑 تم إيقاف عمل البوت وباقي الأوامر مؤقتاً يا سلطاني.")
        return
    elif text == "تفعيل البوت":
        bot_is_active = True
        await update.message.reply_text("🟢 تم إعادة تفعيل البوت وعمله بكامل طاقته يا سيدي.")
        return
    elif text == "قفل الدردشة":
        group_locked = True
        await update.message.reply_text("🔒 تم قفل المجموعة بأمر من السلطان.")
        return
    elif text == "فتح الدردشة":
        group_locked = False
        await update.message.reply_text("🔓 تم فتح المجموعة.")
        return


# 3. الردود العامة، الحماية والسرعة القصوى
async def main_security_and_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_is_active, group_locked
    if not update.message or not update.message.text:
        return
        
    if not bot_is_active:
        return

    message_text = update.message.text.strip()
    message_lower = message_text.lower()
    user = update.message.from_user
    chat = update.message.chat
    
    is_owner = (user.id == OWNER_ID)
    
    # 👑 الأوامر والردود الخاصة بك وحدك
    if is_owner:
        if message_text == "دستور":
            await update.message.reply_text("👑 عمت مساءً يا سلطان مملكة التلجرام! الأرض أرضك والأمر أمرك.")
            return
        elif message_text == "هزيم":
            await update.message.reply_text("أهلاً بك بابا")
            return
        elif message_text == "هزيم الرعد":
            await update.message.reply_text("أمرك مطاع يا سيدي ومطوري! أنا رهن إشارتك وبكامل قوتي.")
            return
        elif message_text in ["/help", "الاوامر", "الأوامر"]:
            help_text = (
                "🛠 **قائمة أوامر حماية وإدارة هزيم الرعد الشاملة:**\n\n"
                "👑 **أوامر السلطان:**\n"
                "• إيقاف البوت / تفعيل البوت\n"
                "• قفل الدردشة / فتح الدردشة\n"
                "• دستور / هزيم / هزيم الرعد\n"
            )
            await update.message.reply_text(help_text, parse_mode="Markdown")
            return
        elif message_text in ["/developer", "مطور البوت"]:
            await update.message.reply_text("👑 هذا البوت تم تصميمه وبرمجته خصيصاً ليخدم سيدي ومولاي **السلطاني**.")
            return
        elif message_text in ["/info", "معلومات القروب"]:
            await update.message.reply_text(f"📊 معلومات القروب:\n- اسم القروب: {chat.title}\n- آي دي القروب: `{chat.id}`", parse_mode="Markdown")
            return
        elif message_text in ["رابط القروب", "الرابط"]:
            try:
                invite_link = await chat.export_invite_link()
                await update.message.reply_text(f"🔗 رابط الدعوة الخاص بالمجموعة:\n{invite_link}")
            except Exception:
                await update.message.reply_text("⚠️ عذراً، لا أملك صلاحية جلب الرابط.")
            return

        return

    if group_locked:
        try:
            await update.message.delete()
            return
        except Exception:
            pass

    if "السلام عليكم" in message_text:
        await update.message.reply_text("وعليكم السلام ورحمة الله وبركاته، أهلاً بك يا صديقي.")
        return

    # 🛡 حماية الفتيات والأعضاء من التحرش
    harassment_words = ["يا حلوة", "تعال خاص", "مزة", "تعال واتساب", "رقمك", "بنت شو"]
    for h_word in harassment_words:
        if h_word in message_lower:
            try:
                await update.message.delete()
                warning_harass = await update.message.reply_text(
                    f"⚠️ **تحذير صارم يا {user.first_name}!** إياك والتطاول أو التحرش هنا!"
                )
                context.job_queue.run_once(lambda ctx: warning_harass.delete(), 10)
                return
            except Exception as e:
                logger.error(f"خطأ في حماية الفتيات: {e}")

    # 🧠 التحليل النفسي
    is_sad_or_upset = any(word in message_lower for word in SAD_WORDS)
    if is_sad_or_upset:
        try:
            await update.message.reply_text(f"💙 أهلاً بك يا {user.first_name}.. لاحظت أنك تمر بضيق، اطمئن نحن بجانبك!")
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"🚨 **تنبيه نفسي:** العضو [{user.first_name}] يبدو حزيناً أو مضايقاً."
            )
        except Exception as e:
            logger.error(f"خطأ في المواساة: {e}")

    # 🛑 فحص السب والروابط
    is_violation = False
    violation_reason = ""

    for word in BAD_WORDS_SET:
        if word in message_lower:
            is_violation = True
            violation_reason = "محتوى مخالف أو سب وشتم"
            break

    if not is_violation:
        if "http://" in message_lower or "https://" in message_lower or "t.me/" in message_lower:
            is_violation = True
            violation_reason = "نشر روابط خارجية أو دعوات"

    if is_violation:
        try:
            await update.message.delete()
            await chat.ban_member(user.id)
            warning_msg = await update.message.reply_text(
                f"🚨 **تم رصد مخالفة أمنية وطرد المخالف فوراً!**\n👤 العضو: {user.first_name}\n⚠️ السبب: {violation_reason}"
            )
            context.job_queue.run_once(lambda ctx: warning_msg.delete(), 8)
        except Exception as e:
            logger.error(f"خطأ في الحظر الفوري: {e}")


if __name__ == '__main__':
    TOKEN = "8764154331:AAH2FJi8xF9Oma4uSvXCLx27IqkTbG-JTM0"
    
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
    app.add_handler(CommandHandler(["help", "developer", "info", "id", "lock", "open"], bot_commands_and_control))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_commands_and_control))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), main_security_and_features))

    print("بوت هزيم الرعد يعمل بأقصى سرعة ومبرمج لحساب السلطاني الأساسي فقط...")
    app.run_polling(poll_interval=0.05, close_loop=False)

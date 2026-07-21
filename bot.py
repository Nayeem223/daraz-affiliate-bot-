from telegram import Update, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================
# SETTINGS
# ==========================

BOT_TOKEN = "8384351425:AAFVpUBgvo67ElYOcWgECPJCt5GbIOtOL9Y"

ADMIN_ID = 1451579464

CHANNELS = [
    -1004477389478,
    -1004464116389,
    -1003956235036,
    -1004447285623,
]

# ==========================
# USER DATA
# ==========================

user_data = {}

# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "✅ Daraz Bot Ready!\n\n"
        "/post = Create New Post"
    )


# ==========================
# POST
# ==========================

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["photos"] = []
    context.user_data["waiting_photo"] = True
    context.user_data["waiting_caption"] = False

    await update.message.reply_text(
        "📷 Send all photos.\n\n"
        "After sending all photos send /done"
    )

# ==========================
# RECEIVE PHOTO
# ==========================

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not context.user_data.get("waiting_photo"):
        return

    if not update.message.photo:
        return

    photo_id = update.message.photo[-1].file_id

    context.user_data["photos"].append(photo_id)

    await update.message.reply_text(
        f"✅ Photo {len(context.user_data['photos'])} Added"
    )


# ==========================
# DONE
# ==========================

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.user_data["photos"]) == 0:
        await update.message.reply_text(
            "❌ Please send at least one photo first."
        )
        return

    context.user_data["waiting_photo"] = False
    context.user_data["waiting_caption"] = True

    await update.message.reply_text(
        "📝 Now send ONE caption.\n\n"
        "Example:\n\n"
        "🔥 Product Name\n"
        "💰 Price: 999 Tk\n"
        "🎁 20% OFF\n"
        "🔗 https://daraz...."
    )

# ==========================
# RECEIVE CAPTION
# ==========================

async def receive_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not context.user_data.get("waiting_caption"):
        return

    caption = update.message.text
    photos = context.user_data["photos"]

    media = []

    for i, photo in enumerate(photos):

        if i == 0:
            media.append(
                InputMediaPhoto(
                    media=photo,
                    caption=caption
                )
            )
        else:
            media.append(
                InputMediaPhoto(
                    media=photo
                )
            )

    for channel in CHANNELS:
        await context.bot.send_media_group(
            chat_id=channel,
            media=media
        )

    context.user_data.clear()

    await update.message.reply_text(
        "✅ Album Posted Successfully!"
    )

# ==========================
# MAIN
# ==========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CommandHandler("done", done))

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receive_photo
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_caption
        )
    )

    print("✅ Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()

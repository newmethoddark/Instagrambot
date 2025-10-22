import telebot
import requests
import os
import random
from datetime import datetime

# -------------------------
# Config
# -------------------------
BOT_TOKEN = os.getenv("8344596547:AAH25iHNTnMZSrPi1BJF3auG6r5b-fbq5jE")  # BOT_TOKEN stored in GitHub secret
bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# -------------------------
# Caption + Dynamic Hashtags
# -------------------------
def generate_caption():
    hashtags = [
        "#ReelsDownloader", "#InstagramReels", "#ReelSaver", "#InstaBot",
        "#ReelsHD", "#NoWatermark", "#TrendingReels", "#ViralReels",
        "#ExplorePage", "#InstaVideo", "#DownloadReels", "#ReelsForYou",
        "#InstaDownloader", "#SocialSaver", "#FastDownload", "#Reels2025",
        "#InstaSave", "#ViralVideo", "#ExploreMore", "#InstaTrend"
    ]
    selected_hashtags = " ".join(random.sample(hashtags, 8))
    return (
        "🎬 **Your Instagram Reel is Ready!**\n\n"
        "🔥 *Downloaded successfully without watermark*\n"
        "⚡ *Fast • Secure • Free Forever*\n\n"
        "💾 Save and share your favorite reels instantly!\n\n"
        f"{selected_hashtags}\n\n"
        "🤖 Powered by @YourBotUsername"
    )

# -------------------------
# Commands
# -------------------------
@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.reply_to(
        message,
        "👋 **Welcome to Insta Reels Downloader Bot!**\n\n"
        "📥 Send me any Instagram Reels link to download it.\n\n"
        "Example:\n`https://www.instagram.com/reel/xyz123/`\n\n"
        "⚡ *No watermark • Fast download • 24/7 online*",
        parse_mode="Markdown",
    )

# -------------------------
# Reel Downloader
# -------------------------
@bot.message_handler(func=lambda msg: "instagram.com/reel" in msg.text)
def download_reel(message):
    url = message.text.strip()
    bot.reply_to(message, "⏳ *Downloading your reel... Please wait.*", parse_mode="Markdown")
    try:
        api_url = f"https://ssinstagram.com/api/convert?url={url}"
        response = requests.get(api_url).json()
        if "url" in response and response["url"]:
            video_url = response["url"][0]["url"]
            caption = generate_caption()
            video_path = os.path.join(DOWNLOAD_DIR, f"reel_{datetime.now().timestamp()}.mp4")
            with open(video_path, "wb") as f:
                f.write(requests.get(video_url).content)
            with open(video_path, "rb") as vid:
                bot.send_video(message.chat.id, vid, caption=caption, parse_mode="Markdown")
            os.remove(video_path)
        else:
            bot.reply_to(message, "❌ *Failed to fetch reel. Make sure the link is public.*", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ *Error:* `{e}`", parse_mode="Markdown")

# -------------------------
# Run bot
# -------------------------
print("✅ Insta Reels Downloader Bot is running...")
bot.infinity_polling()

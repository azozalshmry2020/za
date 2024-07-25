import requests
import telebot
import logging

# إعدادات تسجيل الأخطاء
logging.basicConfig(filename='bot_errors.log', level=logging.ERROR)

# توكن البوت
token = '6361320030:AAGv_ZnDMy3hT1ztGR3Spv3lzpqlpYsS-G4'
bot = telebot.TeleBot(token)

# دالة الترحيب
@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    bot.reply_to(message, f"""Welcome Dear [{name}](tg://settings),\nI am a bot that downloads videos from Instagram. Send the link now""", parse_mode="markdown")

# دالة تحميل الفيديوهات من انستغرام
@bot.message_handler(func=lambda message: True)
def vid(message):
    url = message.text
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    try:
        response = requests.get(f'https://www.instagram.com/graphql/query/?query_hash=2b0673e0dc4580674a88d426fe00ea90&variables={{"shortcode":"{url.split("/")[-2]}"}}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'shortcode_media' in data['data']:
                media = data['data']['shortcode_media']
                if 'video_url' in media:
                    video_url = media['video_url']
                    bot.send_video(message.chat.id, video_url)
                    bot.reply_to(message, 'Download completed 🎶')
                else:
                    bot.reply_to(message, 'Error: No video URL found.')
            else:
                bot.reply_to(message, 'Error: Invalid response from API.')
        else:
            bot.reply_to(message, f'Error: {response.status_code}')
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        bot.reply_to(message, f'Error: {str(e)}')

# تشغيل البوت بتقنية polling
bot.infinity_polling(timeout=30, long_polling_timeout=30)

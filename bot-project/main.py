import asyncio
import os
from telethon import TelegramClient, events
import requests
from io import BytesIO
import tempfile
from telethon import TelegramClient, events

from config import API_ID, API_HASH, BOT_TOKEN
from event_handlers import handle_start_message, handle_phone, handle_code_input, handle_password
from client_handler import user_sessions, start_client, login_client
from clock_handler import handle_setclock, handle_clockoff  
from help import handle_help_message
from instadown import download_instagram_post, clean_download_folder
from profile_image_clock import start_imgclock, stop_imgclock 
from anime_information import get_anime_info_and_image
from github_downloader import gitdown_handler
from redown import handle_redown


async def main():
    bot = TelegramClient('bot', API_ID, API_HASH)
    await bot.start(bot_token=BOT_TOKEN)

    @bot.on(events.NewMessage(pattern='/redown (.+)'))
    async def redown_handler(event):
        await handle_redown(event)


    @bot.on(events.NewMessage(pattern='/help'))
    async def on_help(event):
        await handle_help_message(event)

    @bot.on(events.NewMessage(pattern=r'/imgclock'))
    async def on_imgclock(event):
        await start_imgclock(event)

    @bot.on(events.NewMessage(pattern=r'/imgclockoff'))
    async def on_imgclockoff(event):
        await stop_imgclock(event) 


    @bot.on(events.NewMessage(pattern='/setclock'))
    async def on_setclock(event):
        await handle_setclock(event, bot)

    @bot.on(events.NewMessage(pattern='/clockoff'))
    async def on_clockoff(event):
        await handle_clockoff(event, bot)

    @bot.on(events.NewMessage(pattern='/start'))
    async def on_start(event):
        await handle_start_message(event)


 
    @bot.on(events.NewMessage(pattern=r'^/gitdown (.+)'))
    async def on_gitdown(event):
        await gitdown_handler(event)
            
    @bot.on(events.NewMessage(pattern='/instadown (.+)'))
    async def insta_download(event):
        url = event.pattern_match.group(1)
        await event.reply("⏳ Yuklab olinmoqda, iltimos kuting...")
        try:
            download_instagram_post(url)
            video_sent = False
            image_sent = False
            for file in os.listdir('instadown'):
                if file.endswith('.mp4') and not video_sent:
                    await event.reply(file=f'instadown/{file}')
                    video_sent = True
                elif file.endswith('.jpg') and not image_sent and not video_sent:
                    await event.reply(file=f'instadown/{file}')
                    image_sent = True
            clean_download_folder()
        except Exception as e:
            await event.reply(f"❌ Yuklab olishda xatolik: {e}")


    @bot.on(events.NewMessage(pattern='/anime (.*)'))
    async def anime_info(event):
        anime_name = event.pattern_match.group(1)
        anime_details, anime_image = await get_anime_info_and_image(anime_name)

        if anime_image:
            if len(anime_details) > 1024:
                anime_details = anime_details[:1021] + "..."

            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(anime_image.getvalue())
                tmp_file.close()

                await event.client.send_file(
                    event.chat_id, 
                    tmp_file.name, 
                    caption=anime_details, 
                    parse_mode='markdown'
                )
        else:
            await event.reply(anime_details)
            
    @bot.on(events.NewMessage)
    async def on_message(event):
        if event.sender_id in user_sessions:
            user_data = user_sessions[event.sender_id]
            if user_data['awaiting_password']:
                await handle_password(event)
            else:
                await handle_code_input(event)
        else:
            await handle_phone(event)

    @bot.on(events.CallbackQuery)
    async def on_callback_query(event):
        await handle_code_input(event)

    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
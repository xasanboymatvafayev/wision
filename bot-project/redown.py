import re
import os
from client_handler import user_sessions  
from telethon.tl.types import PeerChannel
from telethon.errors import ChannelPrivateError, RpcCallFailError

async def handle_redown(event):
    user_data = user_sessions.get(event.sender_id)
    if not user_data:
        await event.reply("⚠️ Avval tizimga kirishingiz kerak.")
        return

    client = user_data['client']
    user_input = event.pattern_match.group(1).strip()

    try:
        private_match = re.search(r'https?://t\.me/c/(\d+)/(\d+)', user_input)
        public_match = re.search(r'https?://t\.me/([^/]+)/(\d+)', user_input)

        if private_match:
            chat_id = int(private_match.group(1))
            message_id = int(private_match.group(2))
            chat = PeerChannel(chat_id)
        elif public_match:
            chat_username = public_match.group(1)
            message_id = int(public_match.group(2))
            chat = await client.get_entity(chat_username)
        elif user_input.isdigit():
            chat = event.chat_id
            message_id = int(user_input)
        else:
            await event.reply("⚠️ Xato: To‘g‘ri Telegram havolasini yuboring.")
            return

        try:
            message = await client.get_messages(chat, ids=message_id)
        except ChannelPrivateError:
            await event.reply("🚫 Bu shaxsiy kanal. Kirish huquqingiz yo‘q.")
            return

        if not message:
            await event.reply("🚫 Xabar topilmadi. Kanalga a'zo bo‘lishingiz kerak.")
            return

        if message.media:
            file = await client.download_media(message)
            await client.send_file('me', file, caption=f"📥 Yuklandi - ID: {message_id}")
            await event.reply("✅ Xabar 'me' ga yuborildi.")
            os.remove(file)
        else:
            await client.send_message('me', f"ℹ️ Xabar (ID: {message_id}) da media yo‘q.")
            await event.reply("ℹ️ Xabarda media mavjud emas.")

    except RpcCallFailError as rpc_err:
        await event.reply(f"⚠️ Telegram xatosi: {rpc_err}. Keyinroq urinib ko‘ring.")
    except Exception as e:
        await event.reply(f"❌ Xatolik yuz berdi: {str(e)}")

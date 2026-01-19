from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import asyncio
from telethon import events
from client_handler import user_sessions

clock_tasks = {}

async def update_clock(client, interval):
    while True:
        try:
            now = datetime.now().strftime("%H:%M")
            await client(UpdateProfileRequest(last_name=now))
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"Xato: {e}")
            break

async def handle_setclock(event, bot):
    if event.sender_id in clock_tasks:
        await event.reply("⏳ Soat allaqachon yangilanmoqda.")
        return
    
    user_data = user_sessions.get(event.sender_id)
    if not user_data or 'client' not in user_data:
        await event.reply("⚠️ Avval tizimga kirishingiz kerak.")
        return

    client = user_data['client']
    task = asyncio.create_task(update_clock(client, 60)) 
    clock_tasks[event.sender_id] = task
    await event.reply("✅ Soat muvaffaqiyatli yoqildi va har 60 soniyada yangilanadi.")

async def handle_clockoff(event, bot):
    if event.sender_id in clock_tasks:
        clock_tasks[event.sender_id].cancel()
        del clock_tasks[event.sender_id]
        user_data = user_sessions.get(event.sender_id)
        if user_data and 'client' in user_data:
            client = user_data['client']
            await client(UpdateProfileRequest(last_name=""))  
        await event.reply("❌ Soat to'xtatildi va last_name tozalandi.")
    else:
        await event.reply("⚠️ Soat hali ishga tushmagan.")

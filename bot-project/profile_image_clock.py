from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon import events
from PIL import Image, ImageDraw, ImageFont
import time
import asyncio
from client_handler import user_sessions
import io

clock_active = {}

def create_clock_image():

    img = Image.new('RGB', (500, 500), color='black')
    draw = ImageDraw.Draw(img)

    current_time = time.strftime('%H:%M')
    try:
        font = ImageFont.truetype(r'/home/hevorix/Desktop/telegram-project/mc_font.woff', 150)
    except IOError:
        font = ImageFont.load_default()

    text_size = draw.textbbox((0, 0), current_time, font=font)
    text_width, text_height = text_size[2] - text_size[0], text_size[3] - text_size[1]
    text_position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

    draw.text(text_position, current_time, font=font, fill='white')
    img_path = 'profile_clock_only.jpg'
    img.save(img_path)
    return img_path

async def update_profile_image(client):
    while clock_active.get(client.session.filename, False):
        try:
            img_path = create_clock_image()
            await client(DeletePhotosRequest(await client.get_profile_photos('me')))
            await client(UploadProfilePhotoRequest(file=await client.upload_file(img_path)))
            await asyncio.sleep(60)
        except Exception as e:
            print(f"Xatolik: {e}")
            break

async def start_imgclock(event):
    user_data = user_sessions.get(event.sender_id)
    if not user_data or 'client' not in user_data:
        await event.reply("❌ Siz botga ulanmagansiz! Avval login qiling.")
        return

    client = user_data['client']
    if clock_active.get(client.session.filename, False):
        await event.reply("⏳ Soat allaqachon yoqilgan!")
        return

    clock_active[client.session.filename] = True
    await event.reply("✅ Soatli rasm yuklanmoqda!")

    asyncio.create_task(update_profile_image(client))

async def stop_imgclock(event):
    user_data = user_sessions.get(event.sender_id)
    if not user_data or 'client' not in user_data:
        await event.reply("❌ Siz botga ulanmagansiz! Avval login qiling.")
        return

    client = user_data['client']
    clock_active[client.session.filename] = False

    try:
        await client(DeletePhotosRequest(await client.get_profile_photos('me')))
        await event.reply("❌ Soatli rasm o‘chirildi!")
    except Exception as e:
        await event.reply(f"⚠️ Xatolik: {e}")
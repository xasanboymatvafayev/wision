from telethon import events
import requests
import os

async def gitdown_handler(event):
    url = event.pattern_match.group(1)
    if "github.com" not in url:
        await event.reply("❌ Iltimos, to‘g‘ri GitHub repository URL manzilini kiriting.")
        return
    
    repo_name = url.strip("/").split("/")[-1]
    zip_url = f"{url}/archive/refs/heads/main.zip"
    zip_file = f"{repo_name}.zip"

    try:
        await event.reply(f"⏳ `{repo_name}` repository yuklanmoqda...")
        response = requests.get(zip_url)
        if response.status_code == 200:
            with open(zip_file, "wb") as file:
                file.write(response.content)
            await event.reply(file=zip_file, message=f"✅ `{repo_name}` yuklandi!")
            os.remove(zip_file)
        else:
            await event.reply("❌ Repository topilmadi yoki yuklab olishda xatolik yuz berdi.")
    except Exception as e:
        await event.reply(f"❌ Xatolik: {str(e)}")


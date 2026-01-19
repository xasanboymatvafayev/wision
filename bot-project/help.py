from telethon import events

async def handle_help_message(event):
    help_text = (
        """
Telegram botimizdagi barcha functionlar !

Registratsia talab qiluvchi funktsiyalar:
/setclock - Profilingizda soatni ko'rsatishni yoqish
/clockoff - Profil soatini o'chirish
/imgclock - Profil rasmida soatni ko'rsatish
/imgclockoff - Profil rasmidagi soatni o'chirish
/redown [message id] - Restricted content yuklovchi

Registratsia talab qilmaydigan funktsiyalar !
/anime [anime_nomi] - Anime haqida ma'lumot olish
/instadown [instagram post url] - Instagramdan postlarni yuklab beradi
/gitdown [github repository url] - Githubdan repository yuklab beradi

Yordam olish uchun buyruq:
/help - Botimizdagi barcha commandlar 
/start - Botni qayta boshlash
        """
    )

    image_url = "https://files.catbox.moe/ds0cyy.jpg"  # Rasm URL manzili

    await event.client.send_file(
        event.chat_id,
        image_url,
        caption=help_text,
        parse_mode='markdown'
    )

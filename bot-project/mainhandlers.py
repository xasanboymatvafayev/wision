from anime_information import get_anime_info_and_image
from webscreen import take_screenshot

@bot.on(events.NewMessage(pattern='/anime (.*)'))
async def anime_info(event):
        anime_name = event.pattern_match.group(1)
        
        anime_details, anime_image = get_anime_info_and_image(anime_name)
        
        if anime_image:
            if len(anime_details) > 1024:
                anime_details = anime_details[:1021] + "..."

            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(anime_image.getvalue())
                tmp_file.close()

                await event.client.send_file(event.chat_id, tmp_file.name, caption=anime_details, parse_mode='markdown')
        else:
            await event.reply(anime_details)


@bot.on(events.NewMessage(pattern=r'/webscreen (.+)'))
async def webscreen_handler(event):
        try:
            url = event.pattern_match.group(1)
            save_path = "screenshot.png"
            await event.reply("⏳ Skreenshot olinmoqda, biroz kuting...")
            take_screenshot(url, save_path)
            await event.reply(file=save_path)
            os.remove(save_path)

        except Exception as e:
            await event.reply(f"❌ Xatolik yuz berdi: {str(e)}")
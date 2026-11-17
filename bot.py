import os
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s: %(message)s", level=logging.INFO
)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]
CHANNEL = int(os.environ["CHANNEL_ID"])

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


@client.on(events.NewMessage(func=lambda e: e.is_private))
async def save(event):
    try:
        me = await client.get_me()
        if event.chat_id == me.id:
            return  # пропускаем "Избранное"

        chat = await event.get_chat()
        first = getattr(chat, "first_name", None) or ""
        last = getattr(chat, "last_name", None) or ""
        name = f"{first} {last}".strip() or "Неизвестный"
        user = getattr(chat, "username", None)
        username = f" (@{user})" if user else ""

        if event.out:
            header = f"📤 Вы → {name}{username}:\n\n"
        else:
            header = f"📩 {name}{username}:\n\n"

        if event.media:
            await client.send_file(
                CHANNEL, event.media, caption=header + (event.text or "")
            )
        elif event.text:
            await client.send_message(CHANNEL, header + event.text)
    except Exception as e:
        logging.error(f"Ошибка при сохранении: {e}")


client.start()
client.run_until_disconnected()

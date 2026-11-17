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


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def save(event):
    try:
        sender = await event.get_sender()
        first = getattr(sender, "first_name", None) or ""
        last = getattr(sender, "last_name", None) or ""
        name = f"{first} {last}".strip() or "Неизвестный"
        user = getattr(sender, "username", None)
        username = f" (@{user})" if user else ""
        header = f"📩 ЛС от {name}{username}:\n\n"

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

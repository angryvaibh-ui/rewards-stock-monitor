import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = (
    "🤖 Rewards Stock Monitor\n\n"
    "✅ GitHub Actions is connected successfully!\n"
    "📱 Telegram notifications are working."
)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message,
    },
    timeout=20,
)

response.raise_for_status()

print("Telegram test message sent successfully!")

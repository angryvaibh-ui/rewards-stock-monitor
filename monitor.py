import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

PRODUCT_URL = (
    "https://www.flipkart.com/flipkart-digital-gift-card/"
    "p/itme2bb903489d9a?pid=GVOG9AN3NQGJXYSB"
)

STATE_FILE = "status.txt"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def get_previous_status():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            return file.read().strip()

    return "UNKNOWN"


def save_status(status):
    with open(STATE_FILE, "w") as file:
        file.write(status)


print("Checking Flipkart gift card...")

response = requests.get(
    PRODUCT_URL,
    headers=headers,
    timeout=20
)

print("HTTP status:", response.status_code)

response.raise_for_status()

page = response.text.lower()

unavailable_words = [
    "out of stock",
    "currently unavailable",
    "sold out",
]

available_words = [
    "buy now",
    "add to cart",
]

if any(word in page for word in unavailable_words):
    current_status = "OUT_OF_STOCK"

elif any(word in page for word in available_words):
    current_status = "AVAILABLE"

else:
    current_status = "UNKNOWN"


previous_status = get_previous_status()

print("Previous status:", previous_status)
print("Current status:", current_status)


# Alert ONLY when status changes from unavailable/unknown to available.
if (
    current_status == "AVAILABLE"
    and previous_status != "AVAILABLE"
):

    message = (
        "🚨 FLIPKART GIFT CARD AVAILABLE! 🚨\n\n"
        "The Flipkart Digital Gift Card appears to be available.\n\n"
        f"{PRODUCT_URL}"
    )

    telegram_url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    )

    telegram_response = requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=20,
    )

    telegram_response.raise_for_status()

    print("🚨 Telegram availability alert sent!")

elif current_status == "AVAILABLE":
    print("Still available. No new alert.")

elif current_status == "OUT_OF_STOCK":
    print("Gift card is out of stock.")

else:
    print("Could not determine availability.")


save_status(current_status)

print("Status saved successfully.")

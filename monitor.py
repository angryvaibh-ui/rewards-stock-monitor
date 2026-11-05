import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

PRODUCT_URL = (
    "https://www.flipkart.com/flipkart-digital-gift-card/"
    "p/itme2bb903489d9a?pid=GVOG9AN3NQGJXYSB"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}

try:
    response = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=20,
    )

    print("HTTP status:", response.status_code)

    if response.status_code != 200:
        raise RuntimeError(
            f"Flipkart returned HTTP {response.status_code}"
        )

    page = response.text.lower()

    # Basic availability indicators.
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
        status = "OUT_OF_STOCK"

    elif any(word in page for word in available_words):
        status = "AVAILABLE"

    else:
        status = "UNKNOWN"

    print("Detected status:", status)

    if status == "AVAILABLE":
        message = (
            "🚨 FLIPKART GIFT CARD ALERT 🚨\n\n"
            "The Flipkart Digital Gift Card appears to be AVAILABLE!\n\n"
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

        print("Telegram availability alert sent!")

    elif status == "OUT_OF_STOCK":
        print("Gift card appears to be out of stock.")

    else:
        print(
            "Could not reliably determine availability. "
            "No Telegram alert sent."
        )

except Exception as e:
    print("Monitor error:", e)
    raise

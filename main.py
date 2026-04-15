from supabase import create_client
import requests

# 1. Setup Connections
CRM_URL = "https://qubitech.retailcrm.ru/api/v5/orders"
CRM_KEY = "MmIgsuoUY5cshUKDegIMwATBnQVBEGe7"

SUPABASE_URL = "https://maawfesxlfgetjvdybob.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hYXdmZXN4bGZnZXRqdmR5Ym9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNTI5NTUsImV4cCI6MjA5MTcyODk1NX0.a9T7TK2Ys6vHRsFvn2OVEO3N6GLG3htjW7VkjskFKeQ"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TOKEN = "8781031064:AAErWsgxAS1Vhu8AsIfFFmeo2cUq_4jKlbE"
CHAT_ID = 7220684459


def send_telegram_alert(amount, customer_name, order_id):
    """Sends a notification to Telegram."""
    message = (
        f"🔔 *New High-Value Order!*\n\n"
        f"💰 *Amount:* {amount:,.0f} ₸\n"
        f"👤 *Customer:* {customer_name}\n"
        f"📦 *Order ID:* {order_id}\n\n"
        f"🚀 _Check RetailCRM for details_"
    )

    # ✅ FIXED URL: Added 'api.'
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        # Check if the Telegram API actually processed it
        result = response.json()
        if response.status_code == 200 and result.get("ok"):
            print(f"✅ Alert sent for Order #{order_id}")
        else:
            print(f"❌ Telegram Error: {result.get('description')}")
    except Exception as e:
        print(f"⚠️ Connection error: {e}")


# 2. Get Data from RetailCRM
# We add limit=50 to ensure we get all the orders you just uploaded
response = requests.get(f"{CRM_URL}?apiKey={CRM_KEY}&limit=50")
orders = response.json().get('orders', [])


# 3. Process and Upload to Supabase
for o in orders:
    # 1. Prepare data (same as you had)
    custom_fields = o.get('customFields')
    if not isinstance(custom_fields, dict):
        custom_fields = {}

    delivery = o.get('delivery', {})
    address = delivery.get('address', {}) if isinstance(delivery, dict) else {}

    # Get values for logic
    total = float(o.get('totalSumm', 0))
    first_name = o.get('firstName', '')
    last_name = o.get('lastName', '')
    full_name = f"{first_name} {last_name}".strip()
    order_id = o.get('id')

    order_data = {
        "crm_id": order_id,
        "first_name": first_name,
        "last_name": last_name,
        "phone": o.get('phone'),
        "email": o.get('email'),
        "city": address.get('city'),
        "total_sum": total,
        "status": o.get('status'),
        "order_method": o.get('orderMethod'),
        "utm_source": custom_fields.get('utm_source'),
    }

    # 2. Sync to Supabase
    try:
        supabase.table("orders").insert(order_data).execute()
        print(f"✅ Synced Order #{order_id} for {first_name}")
    except Exception as e:
        print(f"❌ Error syncing order {order_id}: {e}")

    # 3. THE MISSING PART: Telegram Notification Trigger
    if total > 50000:
        print(f"🔔 High value found: {total} ₸. Sending Telegram...")
        send_telegram_alert(total, full_name, order_id)



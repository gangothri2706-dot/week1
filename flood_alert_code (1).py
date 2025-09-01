import requests
from datetime import datetime
import time
from flask import Flask
from threading import Thread

# ========================
# CONFIG
# ========================
API_KEY = "your_openweather_api_key"   # <-- Replace with your OpenWeather API key
CITY = "Hyderabad"                     # <-- Your city
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# SMS API setup (Fast2SMS)
SMS_API = "https://www.fast2sms.com/dev/bulkV2"
SMS_API_KEY = "your_fast2sms_api_key"  # <-- Replace with your Fast2SMS API key
PHONE_NUMBER = "9876543210"            # <-- Replace with your phone number

RAINFALL_THRESHOLD = 50  # mm in 3 hours
LOG_FILE = "flood_log.txt"  # log file to track history


# ========================
# FUNCTIONS
# ========================
def write_log(message):
    """Save messages into a log file with timestamp"""
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


def send_sms_alert(message):
    """Send SMS alert using Fast2SMS"""
    payload = {
        'sender_id': 'FSTSMS',
        'message': message,
        'language': 'english',
        'route': 'q',
        'numbers': PHONE_NUMBER
    }
    headers = {
        'authorization': SMS_API_KEY,
        'Content-Type': "application/x-www-form-urlencoded",
    }
    response = requests.post(SMS_API, data=payload, headers=headers)

    log_msg = f"✅ SMS Sent: {response.text}"
    print(log_msg)
    write_log(log_msg)


def check_weather():
    """Fetch weather and check rainfall"""
    try:
        response = requests.get(URL)
        data = response.json()

        if "rain" in data:
            rainfall = data["rain"].get("3h", 0)
            log_msg = f"Rainfall: {rainfall} mm in {CITY} (last 3h)"
            print(log_msg)
            write_log(log_msg)

            if rainfall >= RAINFALL_THRESHOLD:
                alert_msg = f"🚨 Flood Alert! Heavy rain in {CITY}. Rainfall: {rainfall} mm (last 3h)."
                send_sms_alert(alert_msg)
        else:
            no_data_msg = "ℹ️ No rainfall data available."
            print(no_data_msg)
            write_log(no_data_msg)

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        write_log(error_msg)


# ========================
# BACKGROUND LOOP
# ========================
def run_flood_alert():
    while True:
        check_weather()
        time.sleep(300)   # wait 5 minutes before checking again


# ========================
# KEEP ALIVE WEB SERVER
# ========================
app = Flask('')

@app.route('/')
def home():
    return "🚨 Flood Alert System is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)


# ========================
# START BOTH TOGETHER
# ========================
if __name__ == "__main__":
    # Start Flask server (for Replit + UptimeRobot keep-alive)
    t = Thread(target=run)
    t.start()

    # Start flood alert loop
    run_flood_alert()
    
    _______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    output :
    
    Rainfall: 12 mm in Hyderabad (last 3h)
✅ Rainfall safe.
Rainfall: 65 mm in Hyderabad (last 3h)
✅ SMS Sent: {"return": true, "request_id": "abcd1234", "message": ["SMS sent successfully."]}
-___________________________________________________________________________________________________________________________________________________________

ON YOUR PHONE (SMS ALERT)
🔹 3. On Your Phone (SMS Alert)

If rainfall is above threshold (e.g., ≥ 50 mm in 3h), you get a text like:

🚨 Flood Alert! Heavy rain in Hyderabad. Rainfall: 65 mm (last 3h).


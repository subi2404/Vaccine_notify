import requests
from datetime import datetime, timedelta
import time
import pytz
from os import environ

# Constants
time_interval = 20  # (in seconds) Frequency of code execution
PINCODE = "801503"
tele_auth_token = "8458098602:AAH9jIqxrLcUZu98YvdJh7U4QMg0YJ4ZnG0"  # Your Telegram bot token
tel_group_id = "vacNotify"  # Telegram group username or chat ID
IST = pytz.timezone('Asia/Kolkata')
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}

def update_timestamp_send_Request(PINCODE):
    raw_TS = datetime.now(IST) + timedelta(days=1)  # Tomorrow's date
    tomorrow_date = raw_TS.strftime("%d-%m-%Y")
    today_date = datetime.now(IST).strftime("%d-%m-%Y")
    curr_time = datetime.now(IST).strftime("%H:%M:%S")
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={tomorrow_date}"
    response = requests.get(request_link, headers=header)
    raw_JSON = response.json()
    return raw_JSON, today_date, curr_time

def get_availability(age):
    raw_JSON, today_date, curr_time = update_timestamp_send_Request(PINCODE)
    found = False
    for cent in raw_JSON.get('centers', []):
        for sess in cent.get("sessions", []):
            if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
                found = True
                msg = f"""For age {age}+ [Vaccine Available] at {PINCODE} on {sess['date']}
    Center : {cent["name"]}
    Vaccine: {sess["vaccine"]}
    Dose_1: {sess["available_capacity_dose1"]}
    Dose_2: {sess["available_capacity_dose2"]}"""
                send_msg_on_telegram(msg)
                print(f"INFO: [{curr_time}] Vaccine Found for {age}+ at {PINCODE}")

    if not found:
        print(f"INFO: [{today_date}-{curr_time}] Vaccine NOT Found for {age}+ at {PINCODE}")

def send_msg_on_telegram(msg):
    telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id={tel_group_id}&text={msg}"
    tel_resp = requests.get(telegram_api_url)
    if tel_resp.status_code == 200:
        print("Notification has been sent on Telegram")
    else:
        print("Could not send Message", tel_resp.text)

if __name__ == "__main__":
    while True:
        get_availability(45)
        get_availability(18)
        time.sleep(time_interval)

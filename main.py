import time
import requests
from datetime import datetime
import smtplib

MY_EMAIL = "mohamed.cisco.code"
MY_PASSWORD = "mohamed1998+3"

MY_LNG = 34.308826
MY_LAT = 31.354675


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    print(response.status_code)
    response.raise_for_status()
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LNG - 5 <= longitude <= MY_LNG + 5:
        return True


#
# iss_podition = (longitude, latitude)
# print(iss_podition)
def is_night():
    parameter = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0

    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    response.raise_for_status()
    data = response.json()
    # print(data)

    # sunrise = data["results"]["sunrise"]
    # print(sun_lst[1].split(":"))
    # sun_lst = sunrise.split("T")
    # sunset = data["results"]["sunset"]
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":"))
    sunset = int(data["results"]["sunset"].split("T")[1].split(":"))
    print(sunrise)
    print(sunset)
    time_now = datetime.now().hour
    if time_now <= sunrise and time_now >= sunset:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.send_message(
                from_addr=MY_EMAIL,
                to_addrs="mohamedsbaih98@gmail.com",
                msg="Subject: Look Up 👆🏻\n\nThe ISS is above you the sky. "
            )

import time
import schedule
import RPi.GPIO as GPIO
import webbrowser
import os
from datetime import datetime
import holidays
import pyautogui

# Set the URL of the website you want to open
website_url = 'https://vignan-dynamic-college-web-platform.netlify.app'

GPIO.setwarnings(False)
# Set the times to open and close the website (24-hour format)
open_time = "10:39"
close_time = "10:40"

# Set GPIO pin for output
gpio_pin = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)

# Flag to indicate whether supply should be given
supply_active = False

def open_website():
    webbrowser.open(website_url, new=2)  # Open website in a new browser tab
    time.sleep(5)  # Wait for the page to load (adjust this delay as needed)
    pyautogui.press('f11')  # Simulate pressing F11 key to enter fullscreen mode

def close_website():
    os.system("pkill chromium")
    raise Exception("script terminated after closing website")

def supply_to_gpio():
    global supply_active
    supply_active = True

def stop_supply():
    global supply_active
    supply_active = False
    GPIO.output(gpio_pin, GPIO.HIGH)  # Set pin to HIGH

holiday_list = holidays.India()

# Schedule the tasks
schedule.every().day.at(open_time).do(open_website)
schedule.every().day.at(close_time).do(close_website)
schedule.every().day.at(open_time).do(supply_to_gpio)
schedule.every().day.at(close_time).do(stop_supply)

# Main loop
try:
    while True:
        now = datetime.now()
        if now.weekday() < 6 and now not in holiday_list:
            schedule.run_pending()
            if supply_active:
                GPIO.output(gpio_pin, GPIO.LOW)  # Set pin to LOW if supply is active
            elif not supply_active:
                GPIO.output(gpio_pin, GPIO.HIGH)   # Set pin to HIGH if supply is not active
            else:
                pass
        time.sleep(1)  # Check every second
except Exception as e:
    print(e)

# Cleanup GPIO
GPIO.cleanup()

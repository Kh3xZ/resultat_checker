from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import os
import schedule
from playsound3 import playsound

EMAIL = "09656469"
PASSWORD = "s99Qg8yFznqeH6q"
LOGIN_URL = "https://www.didousoft.tn/login"
RESULTAT_URL = "https://www.didousoft.tn/user/iset_page?page=resultats"
ALARM_FILE = "alarm.mp3"
i = 0

def play_alarm():
    try:
        playsound(ALARM_FILE, block=False)
    except Exception as e:
        print("🔇 Alarm skipped:", e)

def check_resultats():
    global i
    i += 1
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    print(f"\n🔄 Checking for new results... (Attempt {i})")
    print("🌐 Launching browser...")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        print("🔐 Logging in...")
        driver.get(LOGIN_URL)
        time.sleep(3)
        driver.find_element(By.NAME, "login").send_keys(EMAIL)
        driver.find_element(By.NAME, "mdp").send_keys(PASSWORD)
        driver.find_element(
            By.XPATH,
            "//input[@type='submit' and @value='VALIDER']"
        ).click()
        time.sleep(15)

        print("📄 Navigating to results page...")
        driver.get(RESULTAT_URL)
        time.sleep(5)

        cards = driver.find_elements(By.CSS_SELECTOR, "h4.text-info")
        current_results = set()

        for card in cards:
            text = card.text
            date = text.split("\n")[0].replace("Délibération du : ", "")
            current_results.add(date)

        if os.path.exists("results.txt"):
            with open("results.txt", "r", encoding="utf-8") as f:
                old_results = set(f.read().splitlines())
        else:
            old_results = set()

        new_results = current_results - old_results

        if new_results:
            for result in new_results:
                print(f"📢 Resultat Habtit Nayyikk !!!")
                play_alarm()
                screenshot_file = f"screenshot_{result.replace('/', '-')}.png"
                driver.save_screenshot(screenshot_file)
                print(f"📸 Screenshot saved: {screenshot_file}")
        else:
            print("😭 No new results found.")

        with open("results.txt", "w", encoding="utf-8") as f:
            for result in current_results:
                f.write(result + "\n")

    finally:
        driver.quit()

print("🚀 Resultat checker started")
print("🕒 Running every 3 minutes...")

check_resultats()
schedule.every(3).minutes.do(check_resultats)

while True:
    schedule.run_pending()
    time.sleep(1)

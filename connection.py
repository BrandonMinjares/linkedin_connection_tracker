
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import schedule

# LinkedIn credentials
# LINKEDIN_EMAIL = ""
# LINKEDIN_PASSWORD = ""
# PROFILE_URL = "https://www.linkedin.com/in/brandonminjares/"

# Path to ChromeDriver
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

# Start Selenium WebDriver
def check_connection_status():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    
    try:
        # Open LinkedIn
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        # Log in
        driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD, Keys.RETURN)
        time.sleep(5)

        # Go to target profile
        driver.get(PROFILE_URL)
        time.sleep(5)
        print("testing")
        # Check if "Pending" or "Connect" button is present
        page_source = driver.page_source
        if "Pending" in page_source:
            print("Request still pending.")
        elif "Message" in page_source:
            print("Connection accepted! 🎉")
        else:
            print("Unknown status. Check manually.")

    finally:
        driver.quit()

# Schedule the script to run daily
check_connection_status()

# Run the scheduler
"""
while True:
    schedule.run_pending()
    time.sleep(60)
"""
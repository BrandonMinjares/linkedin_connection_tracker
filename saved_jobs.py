import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LinkedIn credentials
LINKEDIN_EMAIL = "your_email@example.com"
LINKEDIN_PASSWORD = "your_password"

# Path to ChromeDriver
CHROMEDRIVER_PATH = "/path/to/chromedriver"

def save_job_to_csv(job_details):
    """Append extracted job details to CSV file."""
    with open("linkedin_saved_jobs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(job_details)

def login_to_linkedin(driver):
    """Log in to LinkedIn using credentials."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.ID, "password").submit()
    time.sleep(5)

def extract_saved_jobs(driver):
    """Extract job details from the saved jobs list."""
    driver.get("https://www.linkedin.com/my-items/saved-jobs/?cardType=SAVED")
    time.sleep(5)

    try:
        job_list = driver.find_element(By.CLASS_NAME, "GvXnnMieLesgSiMjvOXypGYCDABjCBejdLw")
        job_list_items = job_list.find_elements(By.TAG_NAME, "li")
        
        for job_item in job_list_items:
            try:
                job_info = job_item.find_element(By.CLASS_NAME, "mb1").text.strip()
                job_lines = [line.strip() for line in job_info.split("\n") if "Verified" not in line and "Actively Recruiting" not in line]
                
                # Click dropdown button to reveal links
                try:
                    dropdown_button = job_item.find_element(By.XPATH, ".//button[contains(@aria-label, 'Click to take more actions on')]")
                    driver.execute_script("arguments[0].click();", dropdown_button)
                    time.sleep(3)  # Wait for dropdown to open
                    
                    # Wait for the Apply link to be visible
                    apply_container = WebDriverWait(job_item, 5).until(
                        EC.presence_of_element_located((By.XPATH, ".//div[starts-with(@id, 'ember')]/a"))
                    )
                    job_posting = apply_container.get_attribute("href")
                    
                    # Ensure only job title, company, and location are stored
                    if len(job_lines) >= 3:
                        job_lines = job_lines[:3] + [job_posting]
                    
                except Exception as e:
                    print("Error extracting job links:", e)
                    job_lines.append("")
                
                if job_lines:
                    save_job_to_csv(job_lines)
                    print(f"Saved job: {job_lines}")
                    
            except Exception as e:
                print("Error extracting job:", e)
                continue
    
    except Exception as e:
        print("Error finding saved jobs section:", e)

if __name__ == "__main__":
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        login_to_linkedin(driver)
        extract_saved_jobs(driver)
    finally:
        driver.quit()

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

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

    # Find the main saved jobs section
    try:
        job_section = driver.find_element(By.CLASS_NAME, "grid__col.grid__col--lg-12.mb6")
        
        # Find all <ul> elements within this section
        ul_elements = job_section.find_elements(By.TAG_NAME, "ul")
        
        if len(ul_elements) < 2:
            print("Could not find the second <ul> element.")
            return
        
        # Get the second <ul> and extract all <li> elements
        job_list_items = ul_elements[1].find_elements(By.TAG_NAME, "li")
        
        for job_item in job_list_items:
            try:
                # Extract text content from the <li>
                job_text = job_item.get_attribute("innerText").strip()
                
                # Remove "Verified" and trim trailing space if needed
                job_lines = [line.strip() for line in job_text.split("\n") if "Verified" not in line]

                # If job title exists and had "Verified" removed, trim trailing space
                if job_lines and job_text.endswith("Verified"):
                    job_lines[0] = job_lines[0].rstrip()

                # Save job details to CSV
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

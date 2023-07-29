import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.implicitly_wait(10)

login_url = "http://localhost:8000/login/?next=/"
driver.get(login_url)

# Find their id, which are id_username and id_password
username_input = driver.find_element(By.ID, "id_username")
password_input = driver.find_element(By.ID, "id_password")

username_input.send_keys("djangoSuperuser")
password_input.send_keys("LEGITPassword1234")

# Find the "Sign In" element
sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
sign_in_button.click()

# ==================== After "Sign In" we do =======================================
target_url = "http://localhost:8000"
driver.get(target_url)

# wait for the web to load
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//strong')))

# original version
table_rows = driver.find_elements(By.XPATH, '//tr')

for row in table_rows[1:]:

    export_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, './/button[@id="export-dropdown"]')))
    export_button.click()

    # export_json = row.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(@href, "format=json")]')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, './/a[contains(@class, "dropdown-item") and contains(@href, "format=json")]')))
    export_json.click()


time.sleep(5)

while True:
    time.sleep(1)
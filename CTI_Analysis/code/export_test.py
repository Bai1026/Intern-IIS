import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException


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

# table_rows = driver.find_elements(By.XPATH, '//tr')

window_height = driver.execute_script("return window.innerHeight")
actions = ActionChains(driver)
count = 0 

while True:
    table_rows = driver.find_elements(By.XPATH, '//tr')
    if count >= len(table_rows):
        break
    
    try:
        row = table_rows[i]
        export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')
        # ...
    except StaleElementReferenceException:
        table_rows = driver.find_elements(By.XPATH, '//tr')
        row = table_rows[i]
        export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')
    
    # 確認該元素已經在視窗內且可以點擊
    WebDriverWait(driver, 10).until(EC.visibility_of(export_button[0]))
    # export_button[0].click()
    try:
        export_button[0].click()
    except ElementClickInterceptedException:
        actions.move_to_element(export_button[0]).perform()
        export_button[0].click()

    export_json = WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, './/a[contains(@class, "dropdown-item") and contains(@href, "format=json")]')))
    export_json.click()

    count += 1
    print(count)

    if count % 6 == 0:
        # 滾動一整個視窗的大小
        driver.execute_script(f"window.scrollBy(0, {window_height});")
        time.sleep(5)

    # row = table_rows[count]
    # export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')


# for i in range(1, len(table_rows)):
#     # row = table_rows[i]

#     # export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')
#     try:
#         row = table_rows[i]
#         export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')
#         # ...
#     except StaleElementReferenceException:
#         table_rows = driver.find_elements(By.XPATH, '//tr')
#         row = table_rows[i]
#         export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')
#         # ...

#     # 確認該元素已經在視窗內且可以點擊
#     WebDriverWait(driver, 10).until(EC.visibility_of(export_button[0]))
#     # export_button[0].click()
#     try:
#         export_button[0].click()
#     except ElementClickInterceptedException:
#         actions.move_to_element(export_button[0]).perform()
#         export_button[0].click()

#     export_json = WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, './/a[contains(@class, "dropdown-item") and contains(@href, "format=json")]')))
#     export_json.click()

#     count += 1
#     print(count)

#     if count % 6 == 0:
#         # 滾動一整個視窗的大小
#         driver.execute_script(f"window.scrollBy(0, {window_height});")
#         time.sleep(5)



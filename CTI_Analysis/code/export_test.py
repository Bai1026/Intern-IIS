import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


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

# ... (之前的代码)

table_rows = driver.find_elements(By.XPATH, '//tr')

for i in range(1, len(table_rows)):
    row = table_rows[i]
    export_button = row.find_elements(By.XPATH, './/button[@id="export-dropdown"]')

    # 如果"Export"按钮不存在，或者发生异常，则跳过该行，继续处理下一行
    if not export_button:
        continue

    # 点击"Export"按钮并处理导出选项
    export_button[0].click()

    # 等待"export_json"链接可点击
    export_json = WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, './/a[contains(@class, "dropdown-item") and contains(@href, "format=json")]')))
    export_json.click()

    # 添加一些延迟以等待导出完成
    time.sleep(5)

# ... (其余的代码)

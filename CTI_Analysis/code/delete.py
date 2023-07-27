from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

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

# 获取所有表格行
table_rows = driver.find_elements(By.XPATH, '//tr')

for i in range(1, len(table_rows)):
    try:
        row = table_rows[i]

        # 检查是否有"Error"按钮
        error_button = row.find_element(By.XPATH, './/button[@class="btn btn-danger" and @disabled=""]')

        # 使用JavaScript点击"Delete"按钮
        delete_button = row.find_element(By.XPATH, './/a[@class="btn btn-danger btn-sm" and starts-with(@onclick, "deleteJob")]')
        driver.execute_script("arguments[0].click();", delete_button)

        # 等待一段时间，以确保操作成功
        time.sleep(1)

        # 刷新页面，重新获取表格的所有行
        driver.refresh()
        table_rows = driver.find_elements(By.XPATH, '//tr')

    except NoSuchElementException:
        # 如果找不到"error_button"元素，跳过该行的处理，继续处理下一行
        driver.quit()
        # continue

# 关闭浏览器
# driver.quit()
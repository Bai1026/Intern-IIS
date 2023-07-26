import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# open on Chrome
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

# folder_path = "/Users/zoungming/Desktop/Intern-IIS/CTI_Analysis/code/upload_file"
folder_path = "/Users/zoungming/Desktop/Intern-IIS/CTI_Analysis/code_data/pdfs"

# go through the folder that contains all the files(CTI report) we want to upload
for file_name in os.listdir(folder_path):
    # Since folder_path + file_name = file_path
    file_path = os.path.join(folder_path, file_name)
    
    # to identify element, which is input element and the type is "file" or the id is "id-upload"
    upload_file = driver.find_element(By.XPATH, "//input[@id='id-upload']")
    upload_file.send_keys(file_path)
       
    # wait 1 sec to ensure that the file has been uploaded
    time.sleep(0.5)

while(True):
    time.sleep(1)

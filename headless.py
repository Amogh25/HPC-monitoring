from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
user="yyy"
pw ="xxx"
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
driver.maximize_window()

driver.get("https://github.com/login")
time.sleep(5)
driver.find_element(by=By.ID,value="login_field").send_keys(user)
time.sleep(1)
driver.find_element(by=By.ID,value="password").send_keys(pw)
time.sleep(1)
driver.find_element(By.XPATH,r'//*[@id="login"]/div[4]/form/div/input[11]').click()
time.sleep(10)
driver.close()
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class TestJSON():
  def setup_method(self):
    options=webdriver.ChromeOptions()
    options.add_argument("headless")
    path = "/home/sasha/projects/Selenium/json"
    prefs = {"download.default_directory" : path }
    options.add_experimental_option("prefs",prefs)
    self.driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=options)
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()

  def json_fetch(self):
    dashboard_code="GYYoBhsVk"
    dashboard_name = "kafka-overview"
    self.driver.get("http://localhost:3000/d/"+dashboard_code+"/"+dashboard_name+"?orgId=1")
    time.sleep(8)
    self.driver.execute_script("window.scrollTo(0,0)")
    element = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/main/div[3]/header/nav/div[1]/nav/div/div[2]/div')
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.XPATH, "/html/body/div/div[1]/main/div[3]/header/nav/div[1]/nav/div/div[2]/div/button").click()
    element = self.driver.find_element(By.XPATH, "/html/body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div[3]/a").click()
    time.sleep(2)
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/button").click()
    time.sleep(2)

  def test_login(self,url1):
    usr="admin"
    pw="Rockwood0542@"
    self.driver.get(url1)
    self.driver.set_window_size(1292, 638)
    self.driver.execute_script("window.scrollTo(0,0)")
    self.driver.find_element(By.NAME, "user").send_keys(usr)
    self.driver.find_element(By.ID, "current-password").click()
    self.driver.find_element(By.ID, "current-password").send_keys(pw)
    self.driver.find_element(By.XPATH, "/html/body/div/div[1]/main/div[3]/div/div[2]/div/div/form/button").click()
    time.sleep(5)
    
if __name__=="__main__":

  test1 = TestJSON()
  url1="http://localhost:3000/login"
  test1.setup_method()
  test1.test_login(url1)
  print("Login Successful")
  print("Fetching file")
  test1.json_fetch()
  print("File download complete")
  test1.teardown_method()
import time
import json
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestJsonfetch():
  def setup_method(self):
    options=webdriver.ChromeOptions()
    ##options.add_argument("headless")
    self.driver = webdriver.Chrome('home/amogh/Downloads/chromedriver')
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()
  
  def test_jsonfetch(self):
    user="admin"
    password="admin"
    self.driver.get("http://localhost:3000/d/rYdddlPWk/node-exporter-full?orgId=1/login")
    self.driver.find_element(By.NAME, "user").send_keys(user)
    self.driver.find_element(By.ID, "current-password").click()
    self.driver.find_element(By.ID, "current-password").send_keys(password)
    self.driver.find_element(By.CSS_SELECTOR, ".css-8csoim-button > .css-1mhnkuh").click()    
    time.sleep(5)
    self.driver.get("http://localhost:3000/d/rYdddlPWk/node-exporter-full?orgId=1")
    time.sleep(5)
    self.driver.execute_script("window.scrollTo(0,0)")
    element = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/main/div[3]/header/nav/div[1]/nav/div/div[2]/div')
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.XPATH, "/html/body/div/div[1]/main/div[3]/header/nav/div[1]/nav/div/div[2]/div/button").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    time.sleep(5)
    self.driver.find_element(By.LINK_TEXT, "Export").click()
    time.sleep(5)
    self.driver.find_element(By.XPATH, "/html/body[@class='theme-dark app-grafana no-overlay-scrollbar page-dashboard']/div[2]/div[@class='css-hv4bd1']/div[@class='css-1ad80n9']/div[@class='css-w3hlsh']/div[@class='css-g4isi4']/div[@class='css-13o0icp-horizontal-group']/div[@class='css-14c36pf-layoutChildrenWrapper'][3]/button[@class='css-z53gi5-button']/span[@class='css-1mhnkuh']").click()
    time.sleep(5)
if __name__ == "__main__":
  test= TestJsonfetch()
  test.setup_method()
  test.test_jsonfetch()
  test.teardown_method()

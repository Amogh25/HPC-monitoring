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



class TestStat():
  def setup_method(self):
    options=webdriver.ChromeOptions()
    options.add_argument("headless")
    path = "/home/sasha/projects/Selenium/panel-info"
    prefs = {"download.default_directory" : path }
    options.add_experimental_option("prefs",prefs)
    self.driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=options)
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()

  
  def url_generator(self):
    directory = "/home/sasha/projects/Selenium/json"
    file_list = os.listdir(directory)
    json_files = [f for f in file_list if f.endswith('.json')]
    latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    filepath = os.path.join(directory, latest_file)
    print(filepath)
    data = json.load(open(filepath))
    print("JSON file loaded")
  
    dashboard_name = "node-exporter-full"
    title_list=[]
    stat_list=[]
    for panel in data['panels']:
      if panel['type']=="stat":
        id = str(panel['id'])
        title_list.append(panel['title'])
        url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
        stat_list.append(url)

      if panel.get('panels',0) != 0:
        for pan in panel['panels']:
            if pan['type']=="stat":
                title = pan['title']
                id = str(pan['id'])
                title_list.append(pan['title'])
                url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
                stat_list.append(url)

    print("Panels found")
    for i in range(len(stat_list)):
      print(title_list[i])
      print(stat_list[i])
    return stat_list
  
  def test_login(self,url1):
    usr="xxx"
    pw="yyy"
    self.driver.get(url1)
    self.driver.set_window_size(1292, 638)
    self.driver.execute_script("window.scrollTo(0,0)")
    self.driver.find_element(By.NAME, "user").send_keys(usr)
    self.driver.find_element(By.ID, "current-password").click()
    self.driver.find_element(By.ID, "current-password").send_keys(pw)
    self.driver.find_element(By.XPATH, "/html/body/div/div[1]/main/div[3]/div/div[2]/div/div/form/button").click()
    time.sleep(5)

  def test_fetchpaneldata(self,url2):
    self.driver.execute_script("window.scrollTo(0,0)")
    self.driver.get(url2)
    self.driver.execute_script("window.scrollTo(0,0)")
    time.sleep(3)
    element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button/span").click()
    time.sleep(3)

    
if __name__=="__main__":

  test1 = TestStat()
  url1="http://localhost:3000/"
  test1.setup_method()
  test1.test_login(url1)
  print("Login Successful")
  list = test1.url_generator()
  for i in range(2):
    print("Fetching file "+str(i+1))
    start = time.time()
    test1.test_fetchpaneldata(list[i])
    end = time.time()
    print("File "+str(i+1)+" download complete")
    print(f"Time taken : {(end - start):.03f}s")
  test1.teardown_method()
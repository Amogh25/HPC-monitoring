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
from selenium.common.exceptions import NoSuchElementException
from colorama import Fore,Style
import pandas as pd

class TestTimeSeries():
  metrics = ['CPU Basic', 'Disk Space Used']
  def setup_method(self):
    options=webdriver.ChromeOptions()
    options.add_argument("headless")
    path = "panel-data/"
    prefs = {"download.default_directory" : path }
    options.add_experimental_option("prefs",prefs)
    self.driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=options)
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()

  
  def url_generator(self):
    directory = "json/"
    file_list = os.listdir(directory)
    json_files = [f for f in file_list if f.endswith('.json')]
    latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    filepath = os.path.join(directory, latest_file)
    print(filepath)
    data = json.load(open(filepath))
    print("JSON file loaded")
  
    dashboard_code="rYdddlPW"
    dashboard_name = "node-exporter-full"
    time_interval = "5m"
    refresh_time = "5s"
    title_list=[]
    timeseries_list=[]
    for panel in data['panels']:
      if panel['type']=="timeseries":
        id = str(panel['id'])
        title_list.append(panel['title'])
        url="http://localhost:3000/d/"+dashboard_code+"/"+ dashboard_name +"?orgId=1&editPanel="+id+"&from=now-"+time_interval+"&to=now&refresh="+refresh_time+"&inspect="+id
        timeseries_list.append(url)

      if panel.get('panels',0) != 0:
        for pan in panel['panels']:
            if pan['type']=="timeseries":
                title = pan['title']
                id = str(pan['id'])
                title_list.append(pan['title'])
                url="http://localhost:3000/d/"+dashboard_code+"/"+ dashboard_name +"?orgId=1&editPanel="+id+"&from=now-"+time_interval+"&to=now&refresh="+refresh_time+"&inspect="+id
                timeseries_list.append(url)

    print("\nPanels found\n")
    for i in range(len(timeseries_list)):
      print(title_list[i])
    return timeseries_list,title_list
  
  def test_login(self,url1):
    user="username"
    password="password"
    self.driver.get(url1)
    self.driver.set_window_size(1292, 638)
    self.driver.execute_script("window.scrollTo(0,0)")
    self.driver.find_element(By.NAME, "user").send_keys(user)
    self.driver.find_element(By.ID, "current-password").click()
    self.driver.find_element(By.ID, "current-password").send_keys(password)
    self.driver.find_element(By.XPATH, "/html/body/div/div[1]/main/div[3]/div/div[2]/div/div/form/button").click()
    time.sleep(5)

  def test_fetchpaneldata(self,url2):

    self.driver.execute_script("window.scrollTo(0,0)")
    self.driver.get(url2)
    time.sleep(2)
    self.driver.execute_script("window.scrollTo(0,0)")
    element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div").click()
    
    
    self.driver.execute_script("window.scrollTo(0,0)")
    time.sleep(3)
    try:
      element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div").click()
      self.driver.execute_script("window.scrollTo(0,0)")
      time.sleep(3)
      element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/input")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/input").send_keys("Series joined by time")
      actions = ActionChains(self.driver)
      actions.send_keys(Keys.ENTER).perform()
      self.driver.execute_script("window.scrollTo(0,0)")
      time.sleep(3)
    except NoSuchElementException:
      a=9

    finally:
      element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button/span").click()
      time.sleep(3)
  
  def test_alerting(self,title):

    modes = []
    directory = "panel-data/"
    files = [f for f in os.listdir(directory) if f.startswith(title) and f.endswith(".csv")]
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    data_file = os.path.join(directory,latest_file)
    data = pd.read_csv(data_file)
    for mode in data.columns:
      modes.append(mode)
    modes = modes[1:]

    for mode in modes:
      if pd.api.types.is_string_dtype(data[mode].dtype):
        data[mode] = data[mode].str.replace(r'(\d)\s*\D*$', r'\1', regex=True)
        data[mode] = data[mode].astype(float)

      standard_deviation = data[mode].std()
      mean = data[mode].mean()
      
      print("\nMean value of "+mode.title()+" :"+ str(mean))
      print("Standard Deviation of "+mode.title()+" :"+ str(standard_deviation)+"\n")

      acceptance_criteria_low = mean-standard_deviation
      acceptance_criteria_high = mean +standard_deviation
      print("Acceptance Criteria for " +mode.title()+ " : [" +str(acceptance_criteria_low)+", "+str(acceptance_criteria_high)+"]\n")


      fail_tests = data.loc[(data[mode] < acceptance_criteria_low) | (data[mode] > acceptance_criteria_high)]
      if len(fail_tests) != 0:
        print(Fore.RED , "ALERT: " +title)
        print(Fore.RED,fail_tests[['Time',mode]])
        print(Style.RESET_ALL)
        print("")
        directory = "alert/" 
        os.chdir(directory)
        if os.path.exists(title):
          os.chdir(title)
        else:
          os.makedirs(title)
          os.chdir(title)
        file_name = mode +".csv"
        fail_tests.to_csv(file_name,index=False)
        os.chdir("../..")
      else:
        print(Style.RESET_ALL)
        print("All tests have passed the acceptance criteria")

    
    
    

    
if __name__=="__main__":

  test1 = TestTimeSeries()
  url1="http://localhost:3000/"
  test1.setup_method()
  test1.test_login(url1)
  print("\nLogin Successful\n")
  timeseries_list,title_list = test1.url_generator()
  j=1
  for i in range(len(timeseries_list)):
    if title_list[i] in test1.metrics:
      print("\nFetching file "+str(j))
      start = time.time()
      try:
        test1.test_fetchpaneldata(timeseries_list[i])
        
      except NoSuchElementException:
        print(Fore.RED , "Alert: No Data")
        print(Style.RESET_ALL)
      else:
        end = time.time()
        directory = "panel-data/"
        files = [f for f in os.listdir(directory) if f.startswith(title_list[i]) and f.endswith(".csv")]
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        print("File "+ latest_file+" download complete")
        print(f"Time taken : {(end - start):.03f}s")
        j=j+1
  for i in range(len(timeseries_list)):
    if title_list[i] in test1.metrics:
        test1.test_alerting(title_list[i])

  test1.teardown_method()
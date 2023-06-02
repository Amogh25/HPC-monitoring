import time
import pandas as pd
import json
import os
import argparse
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


class TestKafka():
  #Enter the titles of the panels you would want to fetch the metrics from
  metrics = ['PDU_Power','Sensors_Node']
  def setup_method(self):
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    path = os.path.abspath("panel-data")
    options.add_experimental_option('prefs', {
    'download.default_directory': path,
    'download.prompt_for_download': True,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})
    self.driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=options)
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()
  

  def url_generator(self):
    directory = "json"
    file_list = os.listdir(directory)
    json_files = [f for f in file_list if f.startswith('Kafka') and f.endswith('.json')]
    latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    filepath = os.path.join(directory, latest_file)
    print(filepath)
    data = json.load(open(filepath))
    print("JSON file loaded")

    title_list=[]
    graph_list=[]
    dashboard_code="GYYoBhsVk"
    dashboard_name = "kafka-overview"
    time_interval = "5m"
    refresh_time = "5s"
    for panel in data['panels']:
      id = str(panel['id'])
      title_list.append(panel['title'])
      url="http://localhost:3000/d/"+dashboard_code+"/"+ dashboard_name +"?orgId=1&editPanel="+id+"&from=now-"+time_interval+"&to=now&refresh="+refresh_time+"&inspect="+id
      graph_list.append(url)

      if panel.get('panels',0) != 0:
        for pan in panel['panels']:
            id = str(pan['id'])
            title_list.append(pan['title'])
            url="http://localhost:3000/d/"+dashboard_code+"/"+ dashboard_name +"?orgId=1&editPanel="+id+"&from=now-"+time_interval+"&to=now&refresh="+refresh_time+"&inspect="+id
            graph_list.append(url)

    print("Panels found")
    for i in range(len(graph_list)):
      print(title_list[i])
      print(graph_list[i])
    return graph_list,title_list


  def test_login(self,url1):
    #Enter username
    usr="username" 
    #Enter password
    pw="password"
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
    time.sleep(5)
    self.driver.execute_script("window.scrollTo(0,0)")
    element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div").click()
    self.driver.execute_script("window.scrollTo(0,0)")
    time.sleep(5)
    try:
      element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div").click()
      self.driver.execute_script("window.scrollTo(0,0)")
      time.sleep(5)
      element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/input")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/input").send_keys("Series joined by time")
      actions = ActionChains(self.driver)
      actions.send_keys(Keys.ENTER).perform()
      self.driver.execute_script("window.scrollTo(0,0)")
      time.sleep(3)
    except NoSuchElementException:
      pass

    finally:
      element = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button/span").click()
      time.sleep(3)

  def acceptance(self,title):

    panels = dict()
    panels['title'] = title
    topic = title.lower()
    panels['topic'] = topic

    directory = "panel-data/"
    files = [f for f in os.listdir(directory) if f.startswith(title) and f.endswith(".csv")]
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    data_file = os.path.join(directory,latest_file)
    data = pd.read_csv(data_file)

    standard_deviation = data[topic].std()
    mean = data[topic].mean()

    print("\nMean value of "+title+" :"+ str(mean))
    print("Standard Deviation of "+title+" :"+ str(standard_deviation)+"\n")

    acceptance_criteria = mean-standard_deviation
    print("Acceptance Criteria for " +title+ " :" +str(acceptance_criteria)+"\n")

    panels['acceptance_criteria'] = acceptance_criteria

    filepath = "metrics/config1.json"
    with open(filepath,"r") as f:
      file = json.load(f)
      file['panels'].append(panels)
    with open(filepath,"w") as f:
      json.dump(file,f)

  def test_alerting(self,title):

    with open("metrics/config1.json","r") as f:
      accept = json.load(f)

    for panel in accept['panels']:
      if panel['title'] == title:
        topic = panel['topic']
        acceptance_criteria = panel['acceptance_criteria']
    
    directory = "panel-data/"
    files = [f for f in os.listdir(directory) if f.startswith(title) and f.endswith(".csv")]
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    data_file = os.path.join(directory,latest_file)
    data = pd.read_csv(data_file)
    
    
    fail_tests = data.loc[data[topic] < acceptance_criteria]
    if len(fail_tests) != 0:
      print(Fore.RED , "ALERT:")
      print(Fore.RED,fail_tests[['Time',topic]])
      print(Style.RESET_ALL)
      print("")
      directory = "alert/"
      file_name = topic +".csv"
      file_path = os.path.join(directory,file_name)
      fail_tests.to_csv(file_path,index=False)
    else:
      print(Style.RESET_ALL)
      print("All tests have passed the acceptance criteria")

    
    
if __name__ =="__main__":

  test1 = TestKafka()
  url1="http://localhost:3000/"
  test1.setup_method()
  test1.test_login(url1)
  print("Login Successful")
  graph_list,title_list = test1.url_generator()
  j=1
  for i in range(len(graph_list)):
    if title_list[i] in test1.metrics:
      print("Fetching file "+str(j))
      start = time.time()
      try:
        test1.test_fetchpaneldata(graph_list[i])
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
  with open("metrics/config1.json","w") as f:
    accept = dict()
    accept['panels'] = []
    json.dump(accept,f)
  for i in range(len(graph_list)):
    if title_list[i] in test1.metrics:
        test1.acceptance(title_list[i])
        test1.test_alerting(title_list[i])
    
  test1.teardown_method()
  
  


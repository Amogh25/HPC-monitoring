import json
import time
import pandas as pd
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
from colorama import Fore


class TestKafka():
  def setup_method(self):
    options=webdriver.ChromeOptions()
    options.add_argument("headless")
    path = "/home/sasha/projects/Selenium/panel-data"
    prefs = {"download.default_directory" : path}
    options.add_experimental_option("prefs",prefs)
    self.driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'),options=options)
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()
  

  def url_generator(self):
    directory = "/home/sasha/projects/Selenium/json"
    file_list = os.listdir(directory)
    json_files = [f for f in file_list if f.startswith('Kafka') and f.endswith('.json')]
    latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    filepath = os.path.join(directory, latest_file)
    print(filepath)
    data = json.load(open(filepath))
    print("JSON file loaded")

    title_list=[]
    graph_list=[]
    metrics = ['CPU Usage','Messages In Per Topic','Bytes In Per Topic','Bytes Out Per Topic']
    dashboard_code="8pLvf9BVk"
    dashboard_name = "kafka-overview"
    time_interval = "5m"
    for panel in data['panels']:
      if panel['title'] in metrics:
        id = str(panel['id'])
        title_list.append(panel['title'])
        url="http://localhost:3000/d/"+dashboard_code+"/"+ dashboard_name +"?orgId=1&editPanel="+id+"&from=now-"+time_interval+"&to=now&inspect="+id
        graph_list.append(url)

      if panel.get('panels',0) != 0:
        for pan in panel['panels']:
            if pan['title'] in metrics:
                id = str(pan['id'])
                title_list.append(pan['title'])
                url="http://localhost:3000/d/"+dashboard_code+"/"+ dashboard_name +"?orgId=1&editPanel="+id+"&from=now-"+time_interval+"&to=now&inspect="+id
                graph_list.append(url)

    print("Panels found")
    for i in range(len(graph_list)):
      print(title_list[i])
      print(graph_list[i])
    return graph_list


  def test_login(self,url1):
    usr="username"
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

  def test_alerting(self):

    directory = "/home/sasha/projects/Selenium/panel-data/"
    metrics = ['CPU Usage','Messages In Per Topic','Bytes In Per Topic','Bytes Out Per Topic']
    metrics_dict = dict()
    for i in range(len(metrics)):
       metrics_dict[metrics[i]]= [f for f in os.listdir(directory) if f.startswith(metrics[i]) and f.endswith(".csv")]
       print(metrics_dict[metrics[i]])

    

    #Alerting message size
    directory = "panel-data/"
    data_file = os.path.join(directory,metrics_dict['Bytes In Per Topic'][0])
    data = pd.read_csv(data_file)
    print(Fore.RED , "ALERT: Message size")
    fail_tests = data[data.tests2 > 40]
    print(Fore.RED,fail_tests[['Time','tests2']])
    print("")

    #Alerting high latency
    directory = "panel-data/"
    data_file = os.path.join(directory,metrics_dict['Messages In Per Topic'][0])
    data = pd.read_csv(data_file)
    print(Fore.RED , "ALERT: High Latency")
    fail_tests = data[data.tests2 < 0.150]
    print(Fore.RED,fail_tests[['Time','tests2']])
    print("")

    #Alerting high freguency
    directory = "panel-data/"
    data_file = os.path.join(directory,metrics_dict['Messages In Per Topic'][0])
    data = pd.read_csv(data_file)
    print(Fore.RED , "ALERT: High Frequency")
    fail_tests = data[data.tests2 > 0.500]
    print(Fore.RED,fail_tests[['Time','tests2']])
    print("")

    
if __name__=="__main__":

  test1 = TestKafka()
  url1="http://localhost:3000/"
  test1.setup_method()
  test1.test_login(url1)
  print("Login Successful")
  list = test1.url_generator()
  j=1
  for i in list:
    print("Fetching file "+str(j))
    start = time.time()
    try:
      test1.test_fetchpaneldata(i)
    except NoSuchElementException:
      print(Fore.RED , "Alert: No Data")
      print(Style.RESET_ALL))
    else:
      end = time.time()
      print("File "+str(j)+" download complete")
      print(f"Time taken : {(end - start):.03f}s")
    finally:
      j+=1
  test1.teardown_method()
  test1.test_alerting()
  


import time
import json
import os
import pandas as pd
import csv
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestJsonfinal():
    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome('driver_path')
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def test_jsonfinal(self):

        directory = "directory_path"

        file_list = os.listdir(directory)

        for filename in file_list:
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                os.remove(filepath)
                print(f"{filename} deleted successfully")

        user = "user_name"
        password = "password"
        self.driver.get("http://localhost:3000/d/rYdddlPWk/node-exporter-full?orgId=1/login")
        self.driver.find_element(By.NAME, "user").send_keys(user)
        self.driver.find_element(By.ID, "current-password").click()
        self.driver.find_element(By.ID, "current-password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".css-8csoim-button > .css-1mhnkuh").click()
        time.sleep(5)
        self.driver.get("http://localhost:3000/d/rYdddlPWk/node-exporter-full?orgId=1")
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0,0)")
        element = self.driver.find_element(By.XPATH,
                                           '/html/body/div/div[1]/main/div[3]/header/nav/div[1]/nav/div/div[2]/div')
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH,
                                 "/html/body/div/div[1]/main/div[3]/header/nav/div[1]/nav/div/div[2]/div/button").click()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(5)
        self.driver.find_element(By.LINK_TEXT, "Export").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH,
                                 "/html/body[@class='theme-dark app-grafana no-overlay-scrollbar page-dashboard']/div[2]/div[@class='css-hv4bd1']/div[@class='css-1ad80n9']/div[@class='css-w3hlsh']/div[@class='css-g4isi4']/div[@class='css-13o0icp-horizontal-group']/div[@class='css-14c36pf-layoutChildrenWrapper'][3]/button[@class='css-z53gi5-button']/span[@class='css-1mhnkuh']").click()
        time.sleep(5)

        #Read the recently downloaded json file
        
        directory = "directory_path"

        file_list = os.listdir(directory)

        json_files = [f for f in file_list if f.endswith('.json')]

        latest_file = max(json_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        filepath = os.path.join(directory, latest_file)

        print(filepath)

        #Grouping the panels

        data = json.load(open(filepath))
        gauge_list = []
        time_series_list = []
        stat_list = []
        for panel in data['panels']:
            if panel['type'] == "gauge":
                id = str(panel['id'])
                url = "http://localhost:3000/d/rYdddlPW/node-exporter-full?orgId=1&editPanel=" + id + "&inspect=" + id
                gauge_list.append(url)
            if panel['type'] == "timeseries":
                id = str(panel['id'])
                url = "http://localhost:3000/d/rYdddlPW/node-exporter-full?orgId=1&editPanel=" + id + "&inspect=" + id
                time_series_list.append(url)
            if panel['type'] == "stat":
                id = str(panel['id'])
                url = "http://localhost:3000/d/rYdddlPW/node-exporter-f?orgId=1&editPanel=" + id + "&inspect=" + id
                stat_list.append(url)

        # Download the csv file of first panel in Time series list 

        self.driver.get(time_series_list[0])
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0,0)")
        time.sleep(5)
        element = self.driver.find_element(By.XPATH,
                                            "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH,
                                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div").click()
        self.driver.execute_script("window.scrollTo(0,0)")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".theme-dark").click()
        time.sleep(3)

        element = self.driver.find_element(By.XPATH,
                                            "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]")
        self.driver.execute_script("window.scrollTo(0,0)")
        time.sleep(3)
        element = self.driver.find_element(By.XPATH,
                                            "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.XPATH,
                                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/button/span").click()
        time.sleep(3)

        # Acceptance criteria and moving failed test cases to another csv file

        directory = "directory_path"

        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        most_recent_csv = csv_files[0]

        print("Recently downloaded CSV file:", most_recent_csv)

        df = pd.read_csv(most_recent_csv)

        print(df)

        with open(most_recent_csv, 'r') as input_file, open('cpu_failed_tests.csv', 'w', newline='') as output_file:

            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            header_row = next(reader)
            writer.writerow(header_row)
            
            for row in reader:
            
                if float(row[1].replace('%','')) > 50.00:
                    print(row)
                    writer.writerow(row)

        self.driver.close()


if __name__ == "__main__":
    test = TestJsonfinal()
    test.setup_method()
    test.test_jsonfinal()
    test.teardown_method()

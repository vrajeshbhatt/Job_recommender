# Selenium Libraries & Modules-----------
from re import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#----------------------------------------

# for explicit wait----------------------
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#-----------------------------------------

import time
import pandas as pd
from csv import writer

PATH = 'C:/Program Files (x86)/chromedriver.exe'
driver = webdriver.Chrome(PATH)

indeed_url = 'https://ca.indeed.com/'
driver.get(indeed_url)



# Entering What and Where in search bars------------
what = "Data Analyst"

search_what = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
search_what.send_keys(what)


# where = "Toronto, ON"


# search_what = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
# search_what.send_keys(Keys.COMMAND + "a")
# search_what.send_keys(Keys.DELETE)
# search_what.send_keys(where)
# search_what.send_keys(Keys.RETURN)
#----------------------------------------------------------------------------



jobList = []

  
for pages in range(5):
    jobs = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
    for i in jobs:

        try:
            job_title = WebDriverWait(i, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobTitle"))
            )
            job_title = i.find_element(By.CLASS_NAME,'jobTitle').text
        
        except:
            job_title = '404'
        
        try:
            company = WebDriverWait(i, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "companyName"))
            )
            company = i.find_element(By.CLASS_NAME,'companyName').text.strip()
        
        except:
            company = '404'

        try:
            location = WebDriverWait(i, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "companyLocation"))
            )
            location = i.find_element(By.CLASS_NAME,'companyLocation').text.strip()
        
        except:
            location = '404'
        
        try:
            posted = WebDriverWait(i, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "date"))
            )
            posted = i.find_element(By.CLASS_NAME,'date').text.strip()
        except:
            posted = '404'
        

        #clicking job title to get description
        link = i.find_element(By.LINK_TEXT, job_title)
        link.click()

        
        try:
            description = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-jobDescriptionText"))
            )
            description = driver.find_element(By.CLASS_NAME,'jobsearch-jobDescriptionText').text
        except:
            description = '404'
        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        
        List=[job_title,company,location,posted,description]
        jobList.append(List)
        
    nextPage = driver.find_element(By.CLASS_NAME,'css-cy0uue')
    nextPage.click()


df = pd.DataFrame(jobList)
df.to_csv('Jobs.csv')

driver.quit()
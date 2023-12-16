# Import Libraries
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Time imports
import time
from datetime import datetime

# Python imports
import re, csv

# Html imports
import requests
from bs4 import BeautifulSoup

# Initializing script

def crawler():
    # Define functions
    def init_browser():
        browser_options = webdriver.ChromeOptions()

        chrome_options = ['--no-sandbox', '--disable-gpu', '--ignore-certificate-errors',
                        '--disable-extensions', '--auto-open-devtools-for-tabs', '--headless']

        for option in chrome_options:
            browser_options.add_argument(option)

        driver = webdriver.Chrome(options=browser_options)

        driver.set_window_position(1, 0)
        driver.maximize_window()

        return driver

    # Script variables
    jobTitle = 'auxiliar+de+pedreiro'
    location = 'Brasil'
    geoId = '106057199'

    # Scrip constants
    url = f'https://www.linkedin.com/jobs/search?keywords={jobTitle}&location={location}&geoId={geoId}&trk=public_jobs_jobs-search-bar_search-submit'


    driver = init_browser()

    driver.get(url)

    # Selenium get data
    job_list = []
    job_links = []
    n = 0

    # Record the start time
    start_time = time.time()

    while True:
        try:
            # Scrolling screen
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            print('Scrolling page...')
            time.sleep(3)        

            # Getting job general description
            n += 1
            job_description = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{n}]/div'))).text
            job_full_description = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{n}]/div/a'))).get_attribute('href')
            
            job_list += [job_description]
            job_links += [job_full_description]
            jobs = len(job_list)
            links = len(job_links)

            print(f'Element {n}: {jobs} jobs collected, {links} links collected.')
            

        except:
            if driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/button').text == 'Ver mais vagas':
                driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/button').click()
                print('Clicou em: Ver mais vagas')

                
                job_description = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{n}]/a'))).text
                job_full_description = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{n}]/a'))).get_attribute('href')
                
                job_list += [job_description]
                job_links += [job_full_description]
                jobs = len(job_list)
                links = len(job_links)

                print(f'Element {n}: {jobs} jobs collected, {links} links collected.')

                pass

            elif driver.find_element(By.XPATH, f'//*[@id="main-content"]/section[2]/div[2]/p').text == 'Você viu todas as vagas para esta pesquisa':
                print('Você viu todas as vagas para esta pesquisa')
                break
            else:
                pass       

        # Record the end time
        end_time = time.time()

        # Check if the elapsed time exceeds a threshold (e.g., 600 seconds)
        threshold = 600
        elapsed_time = end_time - start_time
        if elapsed_time > threshold:
            raise TimeoutError("Processing time exceeded the threshold.")


    # Writing headers to a CSV file

    headers = ['Job', 'Company', 'Location', 'Status', 'Published', 'URL', 'Today']
    path_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f'C:/Users/Ana Carolina/OneDrive/Documents/_dev/_localpipeline/output/_scrapingjobs/linkedin_{path_date}.csv'

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(headers)


    # Writing registers to a CSV file

    for i in range(0, jobs):

        # Splitting the text using '\n' as the delimiter
        items = re.split(r'\n', job_list[i])
        url = job_links[i]
        
        # Creating CSV register
        job_title = items[0]
        company_name = items[2]
        job_location = items[3]
        status = items[3]
        published = items[4]
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [job_title, company_name, job_location, status, published, url, today]

        # Writing registers to a CSV file
        with open(file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(row)
            

    print(f"New CSV file '{file_path}' has been created.")

crawler()
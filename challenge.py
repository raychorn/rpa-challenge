'''
### Challenge

Your challenge is to automate the process of extracting data from [**itdashboard.gov**](http://itdashboard.gov/).

- The bot should get a list of agencies and the amount of spending from the main page
    - Click "**DIVE IN"** on the homepage to reveal the spend amounts for each agency
    - Write the amounts to an excel file and call the sheet "**Agencies**".
- Then the bot should select one of the agencies, for example, National Science Foundation (this should be configured in a file or on a Robocloud)
- Going to the agency page scrape a table with all "**Individual Investments**" and write it to a new sheet in excel.
- If the "**UII**" column contains a link, open it and download PDF with Business Case (button "**Download Business Case PDF**")
- Your solution should be submitted and tested on [**Robocloud**](https://cloud.robocorp.com/).
- Store downloaded files and Excel sheet to the root of the `output` folder
- This task should take no more than 4 hours.
    - If you reach 3 hours with tasks still remaining, please describe how in theory you would complete this challenge if more time was allowed.
    
Please leverage pure Python (ex: here) without Robot Framework using the rpaframework for this exercise. While API's and Web Requests are possible the focus is on RPA skillsets so please do not use API's or Web Requests for this exercise. 

**Bonus**: We are looking for people that like going the extra mile if time allows or if your curiosity gets the best of you 😎

Extract data from PDF. You need to get the data from **Section A** in each PDF. Then compare the value "**Name of this Investment**" with the column "**Investment Title**", and the value "**Unique Investment Identifier (UII)**" with the column "**UII**"
    
'''
import os
import sys
import time

import requests

from bs4 import BeautifulSoup


def scrape_content(fpath, href):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    import os

    opts = Options()
    opts.binary_location = "/usr/bin/google-chrome-stable"

    chrome_driver = "/usr/bin/chromedriver"

    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

    driver.get(href)
    
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source)
    i = soup.prettify().find('019-0000')
    t = soup.prettify()[i-200:i+400]
    divs = soup.find_all("div", {"class": "dataTables_sizing"})
    headers = []
    for div in divs:
        headers.append(div.text)
    selects = soup.find_all("select", {"class": "form-control"})
    for select in selects:
        print(select.text)
    print(soup.find(id="test").get_text())
    

if (__name__ == "__main__"):
    url = 'http://itdashboard.gov/'

    r = requests.get(url)
    
    summary_links = []
    
    soup = BeautifulSoup(r.content, 'html5lib')
    links = soup.find_all('a')
    for link in links:
        href = link.attrs.get('href', '')
        if (href.find('/summary/') > -1):
            summary_links.append(href)
            print(href)
    summary_links = list(set(summary_links))
    alink = summary_links[0]
    fq_url = (url + alink).replace('//', '/')
    scrape_content(os.path.dirname(__file__), fq_url)
    print(soup.prettify())

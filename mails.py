from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np

# Declare target url
# url = "https://www.finelib.com/cities/lagos/business/chemical-service/chemical-suppliers"
# This is the chemical company search list link
url ='https://www.finelib.com/search.php?q=chemicals&start=0&t=795'

# This is to initialize option to avoid the chrome browser from popping up
option = webdriver.ChromeOptions()
option.add_argument('headless')

# This is to install the chrome driver whenever it is needed by the script
# the options part is to prevent the driver from automatically popping up the chrome browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

# This is to direct the web driver on the location of the chrome driver executable
# driver = webdriver.Chrome("/Users/AgbaneloChigozie/opt/anaconda3/lib/python3.9/site-packages/selenium/webdriver/chrome/chromedriver",options=option)

# This gets the targetted url data
driver.get(url)

# List of all elements with class div (box-headings box-new-hed) and first link containing chemical company names. This is for the category search on finelib.
# elements = driver.find_elements("xpath", '//div[@class="box-headings box-new-hed"]/a[1]')

# Get all the link elements for the search results page
pageelements = driver.find_elements("xpath", '//div[@class="paging-box"]/a')
# print(len(pageelements))

# Imitialize the pages list
pages = []

# Get the unique links for each search page
for x in range(len(pageelements)):
    y = pageelements[x].get_attribute('href')
    if y not in pages:
        pages.append(y)
    
print(pages)

# # Create a links list for all the businesses
# links = []
# # Loop through all the businesses html elements and append the links using the href attribute
# for i in range(len(elements)):
#     links.append(elements[i].get_attribute('href'))

# Initialize the lists
Company = []
Emails = []

# Lets loop through the search results page links
for page in pages:
    # Gets the link for the first page since it has no href link and its the current link.
    if page is None:
        page1 ='https://www.finelib.com/search.php?q=chemicals&start=0&t=795'
        # indicate what business link we are going to inorder to scrape data
        print('navigating to: ' + page1)
        # Go to the link
        driver.get(page1)

        # Get the business link elements for first search page
        elements = driver.find_elements("xpath", '//div[@id="search-result-cnt"]/dl[1]/dt/a[1]')
        # print(len(elements))

        # Create a links list for all the businesses
        links = []
        # Loop through all the businesses html elements and append the links using the href attribute
        for i in range(len(elements)):
            links.append(elements[i].get_attribute('href'))

        # Loop through all the business links and use the driver to get the links
        for link in links:
            # indicate what business link we are going to inorder to scrape data
            print('navigating to: ' + link)
            # Go to the link
            driver.get(link)

            # do stuff within that page here...

            # Get the company name and filter the edit listing character using the new line delimiter seperator
            companies = driver.find_element("xpath", '//div[@class="box-headings box-new-hed"]')
            company = companies.text
            company = company.split("\n")
            comp = company[0]
            Company.append(comp)
            print(comp)

            # Check if the business name included their email names or not

            # fetch the list of elements that contains the email
            l = driver.find_elements("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')
            # get the total number of email elements
            s = len(l)

            # if the total is greater than 0, print the email. Note: we expect just one email element
            # else just continue the for loop
            if s > 0:
                emails = driver.find_element("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')
                Emails.append(emails.text.strip())
                print(emails.text)
            else:
                emails = "N/A"
                Emails.append(emails)
                continue

            # Go back to the business list page
            driver.back()
    
    else:
        print('navigating to: ' + page)
        # Go to the link
        driver.get(page)

        # Get the business link elements for each search page
        elements = driver.find_elements("xpath", '//div[@id="search-result-cnt"]/dl[1]/dt/a[1]')
        # print(len(elements))

        # Create a links list for all the businesses
        links = []
        # Loop through all the businesses html elements and append the links using the href attribute
        for i in range(len(elements)):
            links.append(elements[i].get_attribute('href'))

        # Loop through all the links and use the driver to get the links
        for link in links:
            # indicate what business link we are going to inorder to scrape data
            print('navigating to: ' + link)
            # Go to the link
            driver.get(link)

            # do stuff within that page here...

            # Get the company name and filter the edit listing character using the new line delimiter seperator
            companies = driver.find_element("xpath", '//div[@class="box-headings box-new-hed"]')
            company = companies.text
            company = company.split("\n")
            comp = company[0]
            Company.append(comp)
            print(comp)

            # Check if the business name included their email names or not

            # fetch the list of elements that contains the email
            l = driver.find_elements("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')
            # get the total number of email elements
            s = len(l)

            # if the total is greater than 0, print the email. Note: we expect just one email element
            # else just continue the for loop
            if s > 0:
                emails = driver.find_element("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')
                Emails.append(emails.text.strip())
                print(emails.text)
            else:
                emails = "N/A"
                Emails.append(emails)
                continue

            # Go back to the business list page
            driver.back()
        # print('ok')



# Quit the driver that powers the automation of the browser
driver.quit()
# Put into a data frame and pass to a csv file
df = pd.DataFrame({'Chemical Companies':Company,'Emails':Emails})
df.to_csv('MarketingMails.csv', index=False)







#########################################################################################################################
# page = driver.page_source

# a = page.find_element("xpath", '//div[@class="box-headings box-new-hed"]').text
# print(a)

# b = driver.find_element('class_name', 'left-column')
# print(b)


# x = driver.find_element(By.LINK_TEXT, 'More info').text
# print(x)


# emails = driver.find_elements("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')
# print(emails)
# print(a)

# email = driver.find_elements("class_name", "subb-bx MT-15")
# print(email)
# x = len(a)
# y = range(x)



# for b in elements:
#     # print(b)
#     print(b.text)
    
    # # elem = WebDriverWait(driver, 10).until(
    # #             EC.element_to_be_clickable((By.XPATH, '//div[@class="box-headings box-new-hed"]/a[1]')))
    # # elem.click()
    # b.click()
    # # sleep(5)
    # # driver.current_url
    # # print(mate)
    # email = driver.find_element("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')
    # print(email.text)

    # elem = WebDriverWait(driver, 10).until(
    #             EC.element_to_be_clickable((By.XPATH, '//div[@class="breadcrumb"]/a[5]')))
    # print(elem.text)
    # elem.click()
    # sleep(30)
    

    # url = "https://www.finelib.com/cities/lagos/business/chemical-service/chemical-suppliers"
    # driver.get(url)
    
    

# for b in a:
#     y = driver.find_element("xpath", '//div[@class="box-headings box-new-hed"]/a[1]').text
#     print(y)

# print(driver.page_source)


# from online
# elements = driver.find_elements_by_xpath("//h2/a")

##########################################################################################################################


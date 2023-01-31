
import pandas as pd

import requests
from bs4 import BeautifulSoup
import selenium
import csv
from selenium.webdriver.common.by import By







# ## function to get the content of the page of required query
cookie={} # insert request cookies within{}
def purplleSearch(search_query):
    url="https://www.purplle.com/product/"+search_query
    print(url)
    page=requests.get(url,headers=header)
    if page.status_code==200:
        print('connected')
        return page
    else:
        return "Error"


# ## function to get the contents of individual product pages using 'data-asin' number (unique identification number)



def Searchasin(asin):
    url="https://www.amazon.com/dp/"+asin
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## function to pass on the link of 'see all reviews' and extract the content




def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## First page product reviews extraction





url='https://www.purplle.com/product/blue-heaven-silk-and-stain-lip-stain-brick-beauty/reviews'


header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.purplle.com/product/blue-heaven-silk-and-stain-lip-stain-brick-beauty/reviews'}

search_response=requests.get(url,headers=header)


print(search_response.status_code)




wanted = 'blue-heaven-silk-and-stain-lip-stain-brick-beauty/reviews'

from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Create a webdriver instance
# driver = webdriver.Chrome()

# # Load the desired page
# driver.get(url)

# # Wait for the content to load
# # (You can adjust the wait time as needed)
# time.sleep(10)

# # Get the source code of the page
# html_source = driver.page_source

# # Close the webdriver
# driver.quit()

# # Use BeautifulSoup to parse the HTML source code
# soup = BeautifulSoup(html_source, "html.parser")

# # Find the desired div tags
# div_tags = soup.findAll("div", {"class": "bc-std10"})
# reviews=[]

# for div_tag in div_tags:
#     text = div_tag.text
#     reviews.append(text)
# for i in reviews:
#     print(i)
#     print('----------')


# Create a webdriver instance
driver = webdriver.Chrome()

# Load the desired page
driver.get(url)

# Wait for the content to load
# (You can adjust the wait time as needed)
time.sleep(10)

# Get the source code of the page
html_source = driver.page_source

# Close the webdriver
# (You can move this to the end of the code)
# driver.quit()

# Use BeautifulSoup to parse the HTML source code
soup = BeautifulSoup(html_source, "html.parser")

# Find the desired div tags
div_tags = soup.findAll("div", {"class": "bc-std10"})

# Extract the information from each div tag
reviews = []
for div_tag in div_tags:
    text = div_tag.text
    reviews.append(text)

# Find the 'Show More' button
show_more_button = driver.find_element(By.XPATH,"/html/body/app-root/main/app-product-review/div[2]/div/div/div/div/div/div/div[1]/div/div[14]/div/a")

# Click the 'Show More' button
show_more_button.click()

# Wait for the new content to load
time.sleep(10)

# Get the updated source code of the page
html_source = driver.page_source

# Use BeautifulSoup to parse the updated HTML source code
soup = BeautifulSoup(html_source, "html.parser")

# Find the updated div tags
div_tags = soup.findAll("div", {"class": "bc-std10"})

# Extract the information from each updated div tag
for div_tag in div_tags:
    text = div_tag.text
    reviews.append(text)

# Repeat the above steps until there are no more 'Show More' buttons
while True:
    try:
        show_more_button = driver.find_element(By.XPATH,"/html/body/app-root/main/app-product-review/div[2]/div/div/div/div/div/div/div[1]/div/div[14]/div/a")
        show_more_button.click()
        time.sleep(10)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        div_tags = soup.findAll("div", {"class": "bc-std10"})
        for div_tag in div_tags:
            text = div_tag.text
            reviews.append(text)
    except:
        break

# Close the webdriver
driver.quit()

# Do something with the reviews
with open('purplle1.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(reviews)



print(reviews)

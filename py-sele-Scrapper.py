
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
import csv
import time
import gspread,oauth2client
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait




from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

scopes = ["https://spreadsheets.google.com/feeds",
                  "https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive",
                  "https://www.googleapis.com/auth/drive"]
cred = ServiceAccountCredentials.from_json_keyfile_name("sheetautho.json", scopes)
gclient = authorize(cred)
sheet = gclient.open('abhimoksh.io-demo').worksheet('Sheet1')


search = "Naturals saloon chennai"
pages = 2

header = ["data_cid", "title", "address", "website", "phone", "reviews","rating","image","category","timing","description","profiles"]
data = []

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.headless = True
driver = webdriver.Chrome(options=options)

driver.get('https://www.google.com')

driver.implicitly_wait(2)
driver.find_element(By.NAME,"q").send_keys(search + Keys.ENTER)
more = driver.find_element(By.TAG_NAME,"g-more-link")
more_btn = more.find_element(By.TAG_NAME,"a")
more_btn.click()
time.sleep(10)

for page in range(2, pages+1):
    elements = driver.find_elements(By.CSS_SELECTOR, 'div#search a[class="vwVdIc wzN8Ac rllt__link a-no-hover-decoration"')
    counter = 1
    for element in elements:
        data_cid = element.get_attribute('data-cid')
        element.click()
        print('item click... 5 seconds...')
        time.sleep(5)

        #title
        title = driver.find_element(By.CSS_SELECTOR,'h2[data-attrid="title"]')

        print('title: ', title.text)
        #address
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:address"] span:nth-child(2)')
            if len(temp_obj.text) > 0:
                address = temp_obj.text
        except NoSuchElementException:
            address =""
        print ('address: ',address)
        #website
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[class="kp-header"] div > div > div:nth-child(2) > div > a')
            if temp_obj.text == 'Website':
                website = temp_obj.get_attribute('href')
            else:
                website = ""
        except NoSuchElementException:
            website =""

        print('website:', website)

        #phone
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/collection/knowledge_panels/has_phone:phone"] span:nth-child(2) > span > a > span')
            if len(temp_obj.text) > 0:
                phone = temp_obj.text
        except NoSuchElementException:
            phone =""

        print('phone:', phone)
        #rating
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'g-review-stars span')
            if len(temp_obj.get_attribute('aria-label')) > 0:
                rating = temp_obj.get_attribute('aria-label')
        except NoSuchElementException:
            rating =""

        print('rating:',rating)
        
        # #total review
        # try:
        #     #//*[contains(concat( " ", @class, " " ), concat( " ", "wiI7pd", " " ))]
        #     #//*[contains(concat( " ", @class, " " ), concat( " ", "wiI7pd", " " ))]
        #     temp_obj = driver.find_elements(By.XPATH,"//*[@id='akp_tsuid_29']/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[12]/div/div[2]/div[2]/div[1]/div[2]")
            
        #     reviews = temp_obj
        # except NoSuchElementException:
        #     reviews =""
        # print('reviews:', reviews)

        #image
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:media"] > div > a > div')
            
            if len(temp_obj.get_attribute('style')) > 0:
                image = temp_obj.get_attribute('style')
                if 'background' in image:
                    image = image.replace('background-image: url("','')
                    image = image.replace('"','')
                    image = image.replace(');','')
        except NoSuchElementException:
            image =""
        print('image:', image)

        #category
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/local:lu attribute list"] > div > div > span')
            if len(temp_obj.text) > 0:
                category = temp_obj.text
        except NoSuchElementException:
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/local:one line summary"] > div > span')
                if len(temp_obj.text) > 0:
                    category = temp_obj.text
            except NoSuchElementException:
                category=""
        print('category:', category)

        #timing
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:hours"] > div > div > div:nth-child(2) > div > table')
            if len(temp_obj.get_attribute('innerHTML')) > 0:
                timing = temp_obj.get_attribute('innerHTML')
                timing = "<table>"+timing.replace(' class="SKNSIb"','')+"</table>"
        except NoSuchElementException:
            timing =""
        print('timing:', timing)

        #description
        try:
            temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-long-text]')
            if len(temp_obj.get_attribute('data-long-text')) > 0:
                description = temp_obj.get_attribute('data-long-text')
        except NoSuchElementException:
            '''
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/local:merchant_description"] > c-wiz > div > div:nth-child(2)')
                if len(temp_obj.get_attribute('innerHTML')) > 0:
                    description = temp_obj.get_attribute('innerHTML')
            except NoSuchElementException:
                description =""
            '''
            description=""
            
        print('description:', description)
        # social profiles
        profiles=""
        for s_count in range (1, 6):
            try:
                temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/common/topic:social media presence"] div:nth-child(2) > div:nth-child(' + str(s_count) + ') > div > g-link > a')
                if len(temp_obj.get_attribute('href')) > 0:
                    profiles_str = temp_obj.get_attribute('href')
            except NoSuchElementException:
                profiles_str = ""
                break
            profiles += "<br/>" + profiles_str
        print('profiles: ', profiles)




        #print(counter, data_cid, title.text, address, website, phone,rating,reviews,image,category,timing,description,profiles)
        row = [data_cid, title.text, address, website, phone,rating,image,category,timing,description,profiles]
        data.append(row)
        time.sleep(5)
        sheet.append_row(row)
        time.sleep(5)
        counter+=1
    try:
        page_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Page ' + str(page) + '"]')
        page_button.click()
        print('page click... 10 seconds...')
        time.sleep(10)
    except NoSuchElementException:
        break

with open('moksh.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
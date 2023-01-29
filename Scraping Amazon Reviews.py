#!/usr/bin/env python
# coding: utf-8

# # Scrapping Product Reviews from Amazon

# In[68]:


import pandas as pd

import requests
from bs4 import BeautifulSoup


# In[33]:


search_query="nike+shoes+men"


# In[34]:


base_url="https://www.amazon.com/s?k="


# In[35]:


url=base_url+search_query
url


# In[40]:


header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.amazon.com/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'}


# In[41]:


search_response=requests.get(url,headers=header)


# In[42]:


search_response.status_code


# In[43]:


search_response.text


# In[44]:


search_response.cookies


# ## function to get the content of the page of required query

# In[45]:


cookie={} # insert request cookies within{}
def getAmazonSearch(search_query):
    url="https://www.amazon.com/s?k="+search_query
    print(url)
    page=requests.get(url,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## function to get the contents of individual product pages using 'data-asin' number (unique identification number)

# In[46]:


def Searchasin(asin):
    url="https://www.amazon.com/dp/"+asin
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## function to pass on the link of 'see all reviews' and extract the content

# In[47]:


def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"


# ## First page product reviews extraction

# In[50]:


product_names=[]
response=getAmazonSearch('nike+shoes+men')
soup=BeautifulSoup(response.content)
for i in soup.findAll("span",{'class':'a-size-base-plus a-color-base a-text-normal'}): # the tag which is common for all the names of products
    product_names.append(i.text) #adding the product names to the list


# In[51]:


product_names


# In[52]:


len(product_names)


# #### The method of extracting data-asin numbers are similar to that of product names. Only the tag details have to be changed in findall()

# In[53]:


data_asin=[]
response=getAmazonSearch('nike+shoes+men')
soup=BeautifulSoup(response.content)
for i in soup.findAll("div",{'class':"sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"}):
    data_asin.append(i['data-asin'])


# In[54]:


response.status_code


# In[55]:


data_asin


# In[56]:


len(data_asin)


# #### By passing the data-asin numbers, we can extract the 'see all reviews' link for each product in the page

# In[57]:


link=[]
for i in range(len(data_asin)):
    response=Searchasin(data_asin[i])
    soup=BeautifulSoup(response.content)
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])


# In[58]:


len(link)


# #### Now we have the 'see all review' links. Using this link along with a page number, we can extract the reviews in any number of pages for all the products

# In[71]:


link


# In[59]:


reviews=[]
for j in range(len(link)):
    for k in range(100):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content)
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)


# In[60]:


len(reviews)


# In[61]:


rev={'reviews':reviews}


# In[64]:


review_data=pd.DataFrame.from_dict(rev)
pd.set_option('max_colwidth',800)


# In[72]:


review_data.head(5)


# In[66]:


review_data.shape


# In[78]:


review_data.to_csv('Scraping reviews.csv') #converting the dataframe to a csv file so as to use it later for further analysis


# In[ ]:





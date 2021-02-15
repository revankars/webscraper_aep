#!/usr/bin/env python
# coding: utf-8

# ## Libraries

# In[1]:


import pandas as pd
import requests
from scrapy.http import TextResponse


# ## No of pages to scrape

# In[22]:


pages=int(input('How Many Pages Do You Want to Scrape: '))


# ## Scraper code

# In[34]:


dictionary = {'One':'1', 'Two':'2', 'Three':'3', 'Four':'4', 'Five':'5'}
data={'Title':[],'Price':[],'Stock':[],'Star':[]}
for i in range(pages):
    url = 'http://books.toscrape.com/catalogue/page-'+str(i+1)+'.html'
    #url = 'http://books.toscrape.com/catalogue/page-1.html'
    res = requests.get(url)
    response = TextResponse(res.url, body=res.text, encoding='utf-8')
    print("Scaning page -> {0}".format(i+1))
    books=response.css('ol.row')
    for book in books:
        for b in book.css('article.product_pod'):
            #print(b.css('a::attr(title)').extract_first())
            data['Title'].append(b.css('a::attr(title)').extract_first())
            data['Price'].append(b.css('div.product_price p.price_color::text').extract_first().split('Â')[1])
            data['Stock'].append(b.css('div.product_price p.instock.availability::text').getall()[1].strip())
            data['Star'].append(''.join([v for k,v in dictionary.items() if k in b.css('p::attr(class)').getall()[0].split()[-1]]))


# In[ ]:


## Convert the dictionary to dataframe


# In[39]:


book_df=pd.DataFrame(data)
book_df.head(5)


# ## Save dataframe to notebook

# In[36]:


from platform_sdk.models import Dataset
from platform_sdk.dataset_writer import DatasetWriter
dataset = Dataset(get_platform_sdk_client_context()).get_by_id(dataset_id="602a6dce2dbf29194906f069")
dataset_writer = DatasetWriter(get_platform_sdk_client_context(), dataset)
write_tracker = dataset_writer.write(book_df, file_format='json')


# ## Read the saved data

# In[40]:


from platform_sdk.dataset_reader import DatasetReader
from datetime import date
dataset_reader = DatasetReader(get_platform_sdk_client_context(), dataset_id="602a6dce2dbf29194906f069")
df0 = dataset_reader.limit(100).read()
df0.head(5)


# In[ ]:





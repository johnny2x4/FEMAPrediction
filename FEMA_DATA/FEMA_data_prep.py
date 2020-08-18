#!/usr/bin/env python
# coding: utf-8

# In[110]:


import requests
import feedparser
from pprint import pprint
import pandas as pd
from pandas.io.json import json_normalize
import io
import sqlite3
from datetime import date
import datetime as dt
import time


# Info got it from:
# 
# 
# - https://www.fema.gov/openfema-dataset-disaster-declarations-summaries-v1
# -     https://www.fema.gov/openfema-dataset-disaster-declarations-summaries-v2
# - https://www.fema.gov/openfema-dataset-fema-web-disaster-summaries-v1
# 

# # Disaster Declarations Summaries

# In[111]:


url_1 = 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv'


# In[112]:


disaster_declar_summ = pd.read_csv(url_1)


# In[113]:


def clean_info(dataframe):
    #filter only disasters that happened after the year 2000
    greater_than_2000 = dataframe['fyDeclared']  >= 2000
    clean = dataframe[greater_than_2000]

    #filter only disasters that happened in Florida
    florida_state = clean['state'] == 'FL' 
    clean_2= clean[florida_state]
    
 
    
    return clean_2


# In[ ]:





# In[114]:


df_1 = clean_info(disaster_declar_summ)
df_1


# In[100]:





# In[ ]:





# # FEMA WEB Disaster Summaries

# In[115]:


url_2 = 'https://www.fema.gov/api/open/v1/FemaWebDisasterSummaries.csv'


# In[116]:


web_disaster_summ = pd.read_csv(url_2)


# In[117]:


web_disaster_summ


# # MERGE TABLES

# In[118]:


#Merge the 2 dataframes on disasterNumber

merge2 = pd.merge(df_1,web_disaster_summ, on = 'disasterNumber', how = 'inner')


# In[ ]:





# In[119]:

##Removes non-county data from dataset
merge2 = merge2[merge2['fipsCountyCode'] != 0]


# In[120]:


merge2.declarationDate


# In[121]:


##Selects only DRs - disaster declarations
merge2 = merge2[merge2['declarationType'] == 'DR']


# In[122]:


##Keeps only precipitation related disasters
incTypes = ['Hurricane', 'Severe Storm(s)', 'Coastal Storm']
merge2 = merge2[merge2.incidentType.isin(incTypes)]


# In[123]:


#Changes dates to number of days after Jan 1, 1970 and creates new columns - for linking with NASA data
merge2.declarationDate = pd.to_datetime(merge2.declarationDate).astype('int').div(86400000000000).astype('int')
merge2.incidentBeginDate  = pd.to_datetime(merge2.incidentBeginDate).astype('int').div(86400000000000).astype('int')
merge2.incidentEndDate = pd.to_datetime(merge2.incidentEndDate).astype('int').div(86400000000000).astype('int')
merge2.disasterCloseoutDate = pd.to_datetime(merge2.disasterCloseoutDate).astype('int').div(86400000000000).astype('int')



merge2.to_csv('/Users/brianyoder/Desktop/FEMA.csv')



# In[132]:


##columns to drop
merge2 = merge2.drop(['femaDeclarationString', 'declarationTitle','declarationRequestNumber', 'hash_x', 'lastRefresh_x', 'id_x', 'hash_y', 'lastRefresh_y', 'id_y'], axis=1)


# # POSTGRESQL

# In[106]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:newPassword@localhost:5432/fema')
df_1.to_sql('disaster', engine)














# In[42]:





# In[ ]:


#frame.to_csv('Users\\brianlyoder\\Desktop\\out\\untitled folder\\NASADataAll.csv')


# In[ ]:





import pandas as pd
disaster_declar_summ = pd.read_csv('../FEMA_DATA/DisasterDeclarationsSummaries2.csv')

def clean_info(dataframe):
    #filter only disasters that happened after the year 2000
    greater_than_2000 = dataframe['fyDeclared']  >= 2000
    clean = dataframe[greater_than_2000]

    #filter only disasters that happened in Florida
    florida_state = clean['state'] == 'FL'
    clean_2= clean[florida_state]
    return clean_2

df_1 = clean_info(disaster_declar_summ)
df_1

#FEMA WEB Disaster Summaries
web_disaster_summ = pd.read_csv('../FEMA_DATA/FemaWebDisasterSummaries.csv')
web_disaster_summ

#MERGE TABLES

#Merge the 2 dataframes on disasterNumber
merge2 = pd.merge(df_1,web_disaster_summ, on = 'disasterNumber', how = 'inner')
merge2

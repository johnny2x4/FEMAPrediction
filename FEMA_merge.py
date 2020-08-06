import pandas as pd


url_1 = 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv'
url_2 = 'https://www.fema.gov/api/open/v1/FemaWebDisasterSummaries.csv'
disaster_declar_summ = pd.read_csv(url_1)
web_disaster_summ = pd.read_csv(url_2)


def clean_info(dataframe):
    #filter only disasters that happened after the year 2000
    greater_than_2000 = dataframe['fyDeclared']  >= 2000
    clean = dataframe[greater_than_2000]

    #filter only disasters that happened in Florida
    florida_state = clean['state'] == 'FL'
    clean_2= clean[florida_state]
    return clean_2

df_1 = clean_info(disaster_declar_summ)


# Merge info from DisasterDeclarationSummaries and FemaWebDisasterSummaries
merge2 = pd.merge(df_1,web_disaster_summ, on = 'disasterNumber', how = 'inner')

print(merge2)

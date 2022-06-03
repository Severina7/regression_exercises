import pandas as pd
import numpy as np

import scipy.stats
import os
from env import host, user, password
# from sklearn.model_selection import train_test_split


# Acquiring the Zillow Data

def get_connection(db, user=user, host=host, password=password):
    '''
    get_connection uses login info from env.py file to access Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def get_zillow_data():
    '''
    zillow_data() gets the zillow (only properties_2017 table) data from Codeup db, then writes it to a csv file,
    and returns the DF.
    '''
    # Creating a SQL query
    sql_query = '''
                SELECT 
                       bedroomcnt,
                       bathroomcnt,
                       calculatedfinishedsquarefeet,
                       taxvaluedollarcnt,
                       yearbuilt,
                       taxamount,
                       fips,
                       propertylandusetypeid,
                       transactiondate
                FROM properties_2017
                JOIN propertylandusetype USING(propertylandusetypeid)
                JOIN predictions_2017 USING(parcelid)
                WHERE propertylandusetypeid = '261'
                '''
    
    # Reading in the DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df


def get_local_zillow():
    '''
    get_local_zillow reads in telco data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a DF.
    '''
    if os.path.isfile('properties_2017.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('properties_2017.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = get_zillow_data()
        
        # Cache data
        df.to_csv('properties_2017.csv')
        
    return df

# def split_zillow():
#     '''
#     Takes in a DataFrame and returns train, validate, and test DataFrames.
#     '''
#     # splits df into train_validate and test using train_test_split()
#     train_validate, test = train_test_split(df, test_size=.2, random_state=175)
    
#     # splits train_validate into train and validate using train_test_split() stratifying on species to get an even mix of each species
#     train, validate = train_test_split(train_validate, 
#                                        test_size=.3, 
#                                        random_state=175)
#     return train, validate, test


################# Cleaning and splitting the Zillow Data ######################

def wrangle_zillow():
    '''Cleans, and splits Zillow Data for exploration, once acquired'''

 # Creating a SQL query
    sql_query = '''
                SELECT 
                       bedroomcnt,
                       bathroomcnt,
                       calculatedfinishedsquarefeet,
                       taxvaluedollarcnt,
                       yearbuilt,
                       taxamount,
                       fips,
                       propertylandusetypeid,
                       transactiondate
                FROM properties_2017
                JOIN propertylandusetype USING(propertylandusetypeid)
                JOIN predictions_2017 USING(parcelid)
                WHERE propertylandusetypeid = '261'
                '''
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    # Or getting local zillow
    if os.path.isfile('properties_2017.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('properties_2017.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = get_zillow_data()
        
        # Cache data
        df.to_csv('properties_2017.csv')

        df = pd.read_csv('properties_2017.csv', index_col=0)

    # Dropping null values
    df = df.dropna(axis = 0, how ='any')

    # Dropping a column
    df = df.drop(['propertylandusetypeid'], axis = 1)

    # Renaming columns
    cols_to_rename = {
        'calculatedfinishedsquarefeet': 'indoor_squarefeet',
        'taxvaluedollarcnt': 'taxvalue',
    }
    df = df.rename(columns=cols_to_rename)

    # Converting the following columns to int
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)
    df["indoor_squarefeet"] = df["indoor_squarefeet"].astype(int)
    df["taxvalue"] = df["taxvalue"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["fips"] = df["fips"].astype(int)

    # Filtering the data through number of bedrooms
    df = df[df.bedroomcnt <= 8]

    return df
# # split the data
# train, validate, test = split_zillow()

# train, validate, test

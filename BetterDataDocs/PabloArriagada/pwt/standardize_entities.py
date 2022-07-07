# %%
# ACCESS TO STORAGE ----

# Acess keys to write to  our s3 cloud storage
from access_key import KEY_ID, SECRET_KEY 

# boto3  allows us to write data to our s3 cloud storage
import boto3

# A function we have written to help upload our data to our s3 cloud storage
from functions import upload_to_s3

# Set up access for writing files to s3  
session = boto3.session.Session()

client = session.client('s3',
                        endpoint_url="https://joeh.fra1.digitaloceanspaces.com",
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)

# %%
# Load packages

# Pandas is a standard package used for data manipulation in python code
import pandas as pd
               


# %% 
def standardize_and_save(raw_csv_url,
                        entity_mapping_url, # NB column names must be 'Original Name' and 'Our World In Data Name'
                        entity_name_in_raw,
                        resulting_entity_name,
                        s3_space_to_save_in,
                        as_filename):
    
    # Read in raw dataframe
    df_raw = pd.read_csv(raw_csv_url)


    # Read in mapping table which maps PWT names onto OWID names.
    df_mapping = pd.read_csv(entity_mapping_url)

    # Merge in mapping to raw
    df_harmonized = pd.merge(df_raw,df_mapping,
      left_on=entity_name_in_raw,right_on='Original Name', how='left')
    
    # Drop the old entity names column, and the matching column from the mapping file
    df_harmonized = df_harmonized.drop(columns=[entity_name_in_raw, 'Original Name'])
    
    # Rename the new entity column
    df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': resulting_entity_name})

    # Move the entity column to front:

    # get a list of columns
    cols = list(df_harmonized)
    
    # move the country column to the first in the list of columns
    cols.insert(0, cols.pop(cols.index(resulting_entity_name)))
    
    # reorder the columns of the dataframe according to the list
    df_harmonized = df_harmonized.loc[:, cols]


    # Upload prepared data to our database
    upload_to_s3(df_harmonized, s3_space_to_save_in, as_filename)

# %%

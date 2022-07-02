
# --------- SET UP -----------
# Here we provide details of which libraries and packages we use to prepare the data


# %%
# Pandas is a standard package used for data manipulation in python code
import pandas as pd
# %%
# Check write access
s3access = True

try:
        # Acess keys to write to  our s3 cloud storage
        from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

except:
        print("This notebook is not able to write prepared data to our cloud storage. Steps in the code relating to this will not be run.")
        s3access = False
# %%
# These modules and packages are used to write the transformed data to 
# our cloud storage (not available in notebook versions.)

if s3access:

        # Acess keys to write to  our s3 cloud storage
        from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

        # Acess keys to write to  our s3 cloud storage
        from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

        # boto3  allows us to write data to our s3 cloud storage
        import boto3


        # Acess keys to write to  our s3 cloud storage
        from joes_key import ENDPOINT, KEY_ID, SECRET_KEY 

        # A function we have written to help upload our data to our s3 cloud storage
        from functions import upload_to_s3


        # Set up access for writing files to s3  
        session = boto3.session.Session()

        client = session.client('s3',
                        endpoint_url="https://{}.digitaloceanspaces.com".format(ENDPOINT),
                        aws_access_key_id=KEY_ID,
                        aws_secret_access_key=SECRET_KEY)

        

   
        




# ------- RUN –––––––––

# %%
# Load the 'Walden' data (for the time being in Joe's s3) 

url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/pwt100-original.xlsx'

df_original = pd.read_excel(url, sheet_name='Data')


# %%
# Standardize country names

# %%
# Read in mapping csv – This needs to be two columns headed 'Original Name' and 'Our World In Data Name'
url = 'https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv'

df_mapping = pd.read_csv(url)

# %%
# Merge in the mapping to the main df
df_harmonized = pd.merge(df_original,df_mapping,
    left_on='country',right_on='Original Name', how='left')
    
# Drop the old entity names column, and the matching column from the mapping file
df_harmonized = df_harmonized.drop(columns=['country', 'Original Name'])
    
# Rename the new entity col as specefied in the args
df_harmonized = df_harmonized.rename(columns={'Our World In Data Name': 'country'})
    
# Move entity variable to first column
# get a list of columns
cols = list(df_harmonized)
    
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('country')))
    
# use loc to reorder
df_harmonized = df_harmonized.loc[:, cols]


# %%
if s3access:
    upload_to_s3(df_harmonized, 'pwt', 'harmonized.csv')


# %%
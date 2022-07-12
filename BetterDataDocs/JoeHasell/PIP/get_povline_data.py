#%%
import pandas as pd
import math
import gc



#%%
#%%
#specify as cents, not dolars
#pov_lines_cents = range(1,100, 1)
pov_lines_cents = range(95,100, 1)

dollar = 0

print(f"Downloading files for ${dollar}-{dollar+.1} a day")
#%%
for p in pov_lines_cents:
    pov_line = p/100


    if (math.floor(p/10)>dollar):
        dollar = p/10
        print(f"Downloading files for ${pov_line}-{pov_line+.1} a day")
    
    # Grab data from API
    request_url = f'https://api.worldbank.org/pip/v1/pip?country=all&year=all&povline={pov_line}&fill_gaps=true&welfare_type=all&reporting_level=all&format=csv'
    df = pd.read_csv(request_url)

    df = df[['country_name', 'reporting_year', 'reporting_level','welfare_type']]

    # Write to .CSV
    df.to_csv(f'API_output_poverty/{p}.csv')

    # Drop from memory
    del df
    gc.collect()



#%%


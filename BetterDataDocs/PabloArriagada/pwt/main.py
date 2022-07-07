
#import make_dataframe

from standardize_entities import standardize_and_save


# Standardize entity names in main data file
standardize_and_save(
    raw_csv_url="https://joeh.fra1.digitaloceanspaces.com/pwt/raw_dataframe.csv",
    entity_mapping_url= "https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv",
    mapping_varname_raw = 'Original Name',
    mapping_vaname_owid = "Our World In Data Name",
    data_varname_old='country',
    data_varname_new='entity',
    s3_space_to_save_in='pwt',
    as_filename='entities_standardized.csv'
                    )

#Standardize entity names in national accounts data file
standardize_and_save(
    raw_csv_url="https://joeh.fra1.digitaloceanspaces.com/pwt/raw_dataframe_national_accounts.csv",
    entity_mapping_url= "https://joeh.fra1.digitaloceanspaces.com/pwt/country_standardization_mapping.csv",
    mapping_varname_raw = 'Original Name',
    mapping_vaname_owid = "Our World In Data Name",
    entity_name_in_raw='countrycode',
    resulting_entity_name='entity',
    s3_space_to_save_in='pwt',
    as_filename='entities_standardized_national_accounts.csv'
                    )

import prepare_variables

import write_metadata



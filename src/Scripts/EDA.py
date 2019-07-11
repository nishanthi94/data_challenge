import pandas as pd
import numpy as np
import regex as re
# from geopy.geocoders import Nominatim
# import geopy
# import ssl

print("Loading dataset")
df = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/loan_16_17.csv', index_col=0)

print("Sneak-peak into the dataset")
print(df.head())

print("Filtering the dataframe wrt desired target values")
# target -> 'loan_status'
# Because of ambiguity, using 'Fully Paid', 'Charged Off' and 'Default' loan_status records alone


def replacevalues(df, replace_list):
    ''' replace_list: {k,v} -> (column name, {k1, v1} -> (present value, to be replaced)) '''
    df.replace(replace_list, inplace=True)


temp_dict = {'loan_status': {'Fully Paid': 0, 'Charged Off': 1, 'Default': 1}}
replacevalues(df, temp_dict)

df = df.loc[df['loan_status'].isin([0, 1])]

print("Target variable: loan_status")
print(df['loan_status'].value_counts())

print("No. of observations: ", df.shape[0])
print("No. of features: ", df.shape[1])

print("Datatypes of the features")
print(df.columns.to_series().groupby(df.dtypes).groups)

print("Number of missing values")
print(df.isna().sum())
# note: recurring number of missing values, a pattern

print("Statistical description of the data")
print(df.describe())
# range is not uniform

# check mean and median of numerical cols (can tell us if dist is normal)

# Chant: Better data beats fancier algorithms

# Data Cleaning

print("Remove duplicates")
df.drop_duplicates()

# Missing categorical values

obj_col = df.select_dtypes(include='object').columns.to_list()

# for col in obj_col:
#     print(df[col].value_counts())

temp_col = ['zip_code', 'addr_state']
temp_num = ['term', 'int_rate', 'emp_length', 'loan_status', 'revol_util']
date_col = ['issue_d', 'earliest_cr_line', 'last_pymnt_d', 'next_pymnt_d', 'last_credit_pull_d', 'sec_app_earliest_cr_line', 'hardship_start_date', 'hardship_end_date', 'payment_plan_start_date', 'debt_settlement_flag_date', 'settlement_date']

obj_col = [elem for elem in obj_col if elem not in date_col]
obj_col = [elem for elem in obj_col if elem not in temp_col]
obj_col = [elem for elem in obj_col if elem not in temp_num]

print("List of categorical variables", obj_col)

print("Adding a class 'Missing' for categorical missing values")
df[obj_col] = df[obj_col].fillna(value='Missing')

print("Addressing temp_num")
print("Removing special characters from cols to make it numerical")

# Remove special characters in temp_num


def remove_special_char(df, col_list):
    for col in col_list:
        df[col] = ['-1' if x is np.nan else re.sub(r'[^\d.]+', '', str(x)) for x in df[col]]


# Prepping emp_length
temp_dict = {'emp_length': {'< 1': 0}}
replacevalues(df, temp_dict)

remove_special_char(df, temp_num)

# check
# for col in temp_num:
#     print(df[col].value_counts())

# Change datatype


def change_dtype(df, col, datatype):
    df[col] = df[col].astype(datatype)


for col in temp_num:
    change_dtype(df, col, np.float)

print("Addressing date_col")
print("Extracting month and year from date columns")

# Save month and year separately in 2 columns


def month_converter(month):
    months = ['-1', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if month in months:
        return months.index(month)
    else:
        return 999


for col in date_col:
    print("For column ", col)
    df[col+"_month"] = ['-1' if x is np.nan else re.sub(r'[^a-zA-Z]+', '', str(x)) for x in df[col]]
    df[col+"_month"] = df[col+"_month"].map(month_converter)
    df[col+"_year"] = ['-1' if x is np.nan else re.sub(r'[^\d]+', '', str(x)) for x in df[col]]

print("Addressing zipcode and state")

# Remove xx in zipcode and have a fillvalue 3

df['zip_code'] = ['-1' if x is np.nan else re.sub(r'[^\d]+', '', str(x)) for x in df['zip_code']]
df['zip_code'] = df['zip_code'].astype(str).str.zfill(3)

# Extract latitude and longitude from State

# # Disabling TLS certification completely
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# geopy.geocoders.options.default_ssl_context = ctx
# geolocator = Nominatim(user_agent="nishabalu")
#
#
# def get_latitude(state):
#     location = geolocator.geocode(state, timeout=1000)
#     if location is None:
#         return 90
#     elif state is not np.nan:
#         return location.latitude
#     else:
#         return 90  # North Pole
#
#
# def get_longitude(state):
#     location = geolocator.geocode(state, timeout=1000)
#     if location is None:
#         return 0
#     elif state is not np.nan:
#         return location.longitude
#     else:
#         return 0  # North Pole
#
#
# df['addr_state_latitude'] = df['addr_state'].map(get_latitude)
# df['addr_state_longitude'] = df['addr_state'].map(get_longitude)

# Stored lat and lon in a .csv file to save time
# Spurce: https://developers.google.com/public-data/docs/canonical/states_csv

print("Extracting latitude and longitude from state name")
state = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/state_abbr.csv')
print(state.head())


def dropcolumn(df, col_list):
    df.drop(col_list, axis=1, inplace=True)


# Dropping state names
dropcolumn(state, ['Name'])

# Merging df and state
df = pd.merge(df, state, left_on='addr_state', right_on='State')

# Dropping old columns
dropcolumn(df, date_col)
dropcolumn(df, ['State', 'addr_state'])

# Addressing missing values
missing = df.columns[df.isnull().any()].to_list()
print("Column(s) with missing values", missing)

for col in missing:
    print(col, " Mean: ", df[col].mean(), "Median: ", df[col].median(), "Mode: ", df[col].mode())


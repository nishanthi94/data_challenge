import pandas as pd

df1_16 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2016Q1.csv', index_col = 0)
df2_16 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2016Q2.csv', index_col = 0)
df3_16 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2016Q3.csv', index_col = 0)
df4_16 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2016Q4.csv', index_col = 0)

df1_17 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2017Q1.csv', index_col = 0)
df2_17 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2017Q2.csv', index_col = 0)
df3_17 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2017Q3.csv', index_col = 0)
df4_17 = pd.read_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/2017Q4.csv', index_col = 0)

df = pd.concat([df1_16, df2_16, df3_16, df4_16, df1_17, df2_17, df3_17, df4_17], axis = 0)

df.to_csv('/Users/nishanthi/Documents/GitHub/data_challenge/data/loan_16_17.csv')
import pandas as pd
df = pd.read_csv('data.csv')
df['age'].fillna(df['age'].median(), inplace=True)
df['salary'].fillna(df['salary'].median(), inplace=True)
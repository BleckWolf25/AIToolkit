# Standardize dates to ISO-8601
df['date'] = pd.to_datetime(df['date'], errors='coerce')
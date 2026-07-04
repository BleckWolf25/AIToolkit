# Outlier detection using IQR
q1 = df['val'].quantile(0.25)
q3 = df['val'].quantile(0.75)
iqr = q3 - q1
outliers = df[(df['val'] < (q1 - 1.5 * iqr)) | (df['val'] > (q3 + 1.5 * iqr))]
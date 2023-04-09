import pandas as pd

df1 = pd.read_csv('camh_data.csv', index_col=0)
df2 = pd.read_csv('medhelp_data.csv', index_col=0)
df3 = pd.read_csv('patient_data.csv', index_col=0)

merged_df = pd.concat([df1, df2, df3], ignore_index=True)

#merged_df = merged_df.reset_index(drop=True)

merged_df.to_csv('merged_file.csv')

print('Done')
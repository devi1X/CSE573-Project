import pandas as pd

merged_file = pd.read_csv("merged_file.csv")
result_file = pd.read_csv("result.csv")

merged_df = pd.merge(merged_file, result_file, left_on="Index", right_on="content_index")
merged_df.to_csv("merged_result.csv", index=False)
print(merged_df)

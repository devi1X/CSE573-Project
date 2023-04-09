import pandas as pd
import numpy as np

# take symptoms_id.csv (which is a glossary of terms. ID->named symptom)
# make it into a dict

symptoms_id = {}
symptoms_id_file = 'symptoms_id.csv'
df_id = pd.read_csv(symptoms_id_file)
for i in df_id.iterrows():
    try:
        k = i[1]['symptom_id'].replace("'","")
        v = i[1][' description'].replace("'","")
    except:
        continue
    symptoms_id[k] = v
print(symptoms_id)
old_graph_file = 'sympgraph.csv'
df_old = pd.read_csv(old_graph_file)
df_new = pd.DataFrame(columns=['Source', 'Destination', 'Weight'])
for i in df_old.iterrows():
    # Source, Destination, Weight
    old_source = i[1]['Source']
    old_destination = i[1]['Destination']
    old_weight = i[1]['Weight']
    try:
        df_new = df_new._append({
                'Source': symptoms_id[old_source],
                'Destination': symptoms_id[old_destination],
                'Weight': old_weight}, ignore_index=True)
    except:
        continue
df_new.to_csv('new_graph.csv')
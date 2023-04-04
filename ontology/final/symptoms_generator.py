import numpy as np
import pandas as pd
import os

filename = 'ontology_symptoms.sql'
columns=['symptom_id', 'description']
txt = open(filename, "r")
csv_out = ''
col = ''
for index,line in enumerate(txt):
    if index == 0:
        continue #skip the first line
    if col == '':
        try:
            tmp = line.split('INSERT INTO ')[1].split(' (')[1]  # get the columns
            col = (tmp[:tmp.find(')')])
            csv_out += col
        except:
            continue
    # populate rows
    try:
        tmp = line.split('VALUES')[1].split(' (')[1]  # get the line
        if tmp.contains(');'):

        csv_out += tmp
        # tmp is the line to be inserted
    except:
        continue
writer = open('symptoms_id.csv', 'w')
writer.write(csv_out)
writer.close()

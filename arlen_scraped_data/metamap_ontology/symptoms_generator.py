import numpy as np
import pandas as pd
import os

sql_files = os.listdir('./')

for file in sql_files:
    if file.endswith('.sql'):
        txt = open(file,"r")
        csv_out = ''
        col = ''
        for line in txt:
            # print(line)
            # find column first
            if col == '':
                try:
                    tmp = line.split('INSERT INTO ')[1].split(' (')[1]# get the columns
                    col = (tmp[:tmp.find(')')])
                    csv_out+=col
                except:
                    continue
            # populate rows
            try:
                tmp = line.split('VALUES')[1].split(' (')[1]  # get the line
                csv_out+=tmp
                # tmp is the line to be inserted
            except:
                continue
        writer = open(file+'.csv','w')
        writer.write(csv_out)
        writer.close()


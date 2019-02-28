# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 00:26:04 2019

@author: huang
"""
#In [1]:
import sqlite3
import pandas as pd
import numpy as np
import os
from collections import Counter

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import pickle
os.chdir("D:\\GitHub\\Twitter-Search-and-Stream")


db='Trump'
with open("")
antUserHashtags=
proUserHashtags=

#'ant'+db+'UserList'
#'pro'+db+'UserList'



conn = sqlite3.connect('./'+db+'/'+db+'.db')
c = conn.cursor()
#cnx = sqlite3.connect('file.db')
print("The current topic we are analyzing is {}".format(db))

df_users = pd.read_sql_query("SELECT * FROM user_profile", conn)
print("currently, {} users are stored in the database".format(len(df_users)))



proTrumpUserList=[]
for idx,row in df_users.iterrows():
    for x in proTrumpHashtags:
        if x in row['description']:
            proTrumpUserList.append(row['user_id'])
            break

antiTrumpUserList=[]
for idx,row in df_users.iterrows():
    for x in antiTrumpHashtags:
        if x in row['description']:
            antiTrumpUserList.append(row['user_id'])
            break

print("Number of Trump supporters",len(proTrumpUserList))
print("Number of Trump haters",len(antiTrumpUserList))

with open('proTrumpUserList.data', 'wb') as filehandle:  
    # store the data as binary data stream
    pickle.dump(proTrumpUserList, filehandle,protocol=2)
    
with open('antiTrumpUserList.data', 'wb') as filehandle:  
    # store the data as binary data stream
    pickle.dump(antiTrumpUserList, filehandle,protocol=2)
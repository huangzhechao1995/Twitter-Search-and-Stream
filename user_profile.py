# -*- coding: UTF-8 -*-
from twython import Twython
from datetime import datetime, timedelta
import numpy as np
from helper import *
import sqlite3
from operator import itemgetter
import sys 
import os
reload(sys)
sys.setdefaultencoding('utf8')

conn=sqlite3.connect('./Brexit_snapshot2.db')
c=conn.cursor()

with open('credentials3.py') as f:
    lines = f.read().splitlines()
twitter = Twython(*lines)

##1step = get all teet ids in stream database
query = 'SELECT distinct(user_id) FROM tweet'
temp=c.execute(query).fetchall()

big_users=[i[0] for i in temp]


query ='SELECT distinct(user_id) FROM user_profile'
temp=c.execute(query).fetchall()

small_users=[i[0] for i in temp]

toinsert=list(set(big_users)-set(small_users))


today=datetime.now()
today=datetime(today.year,today.month,today.day,0,0,0)


queryAndInsertUsersProfiles(twitter, c, conn, today, toinsert)

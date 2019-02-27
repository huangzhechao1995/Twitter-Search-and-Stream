# -*- coding: UTF-8 -*-
from twython import Twython
from datetime import datetime, timedelta
import numpy as np
from helper import *
import sqlite3
from operator import itemgetter
import sys 
import os
import pickle

############################################################
####################### Set Parameters #####################
############################################################
credentials=sys.argv[1]
mode = sys.argv[2]
db=sys.argv[3]
target = sys.argv[4:]
if not os.path.exists(db):
    os.makedirs('./'+db)


#mode = 'hashtags'
#db= 'governmentshutdown'
#target = ['governmentshutdown','shut down the government','the shutdown','TrumpShutdown', '#shutdown','NoMoreShutdowns']

"""
# User Mode
mode='users'
db= 'antiTrumpUserTimeline'

with open('antiTrumpUserList.data', 'rb') as filehandle:  
    # read the data as binary data stream
    target = pickle.load(filehandle)
"""
    
if not os.path.exists(db):
    os.makedirs('./'+db)

conn = sqlite3.connect('./'+db+'/'+db+'.db')
c = conn.cursor()


############################################################
####################### Your credentials ###################
############################################################

with open("credential1.txt") as f:
    lines=f.read().splitlines()
#Jen's API
APP_KEY='zHwMGTtFTNKS7ANPuWUaL2HHT'
ACCESS_TOKEN='2610287817-yexyelXsRGO6uNwbEP5Sh8hgR2FvKgELgIqCmaR'
#APP_KEY = 'fGx0NB83fSPEabC2YD6MvsxY8'
APP_SECRET = '5GOHB4rr9U3yZ77YmOAcsimLLWVRQAwqTbnWeENxxFC3DblZKe'

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens(callback_url='http://ph-education.com/')

#####################################################################################
####################### Will create sqlite tables the first time  ###################
#####################################################################################
create_tables(c,conn)
create_tweet_tables(c,conn)

#################################################################
####################### Pick start/end dates ###################
################################################################

####### NOTE : if you want you can query the DB for the most recent date, or most recent tweet id, in order not to search again for previous tweets.
####### That is useful if you want to Crontab the queries on engaging for like a week. I did that once, if you're unfamiliar with sqlite queries from python ask me =)

today=datetime.now()
today=datetime(today.year,today.month,today.day,0,0,0)
start_date = datetime(2019,12,1,0,0,0) # or you can pick start_date = today
end_date = start_date + timedelta(62,0) # or you can pick another end_date 
earliestTweet=0 # or you can pick latest tweet from previous query
latestTweet=-1




#####################################
########## Query a hashtag ##########
#####################################

exceptionusers=[]

if(mode == 'hashtags'):
	input_list_of_target_hashtags = target 
	new_tweets = queryTweetsContainingHashtag(twitter, input_list_of_target_hashtags, start_date, end_date, earliestTweet, latestTweet, maxTweets=60000)
	print('Done querying tweets')
	print('Got at most', len(np.unique([i['id'] for i in new_tweets])), ' new tweets')
	print('Start inserting timelines in database')
	insertTweets(conn,c, new_tweets)
	
	##optional : query user profiles too... takes time
	print('Now querying profiles of people that posted the tweets')
	queryAndInsertUsersProfilesThatPostedTheTweets(twitter, c, conn, today, new_tweets)
	


#########################################
######## Query a user_timeline ##########
#########################################

elif(mode == 'users'):
    new_tweets = []
    user_count=0
    target_users = [int(i) for i in target]
    print('Start querying timelines')
    for user in target_users:
        print('Now querying tweets of user ', user)
        try:
            current_tweets= queryUserTimeline(twitter,user)
            new_tweets = new_tweets + current_tweets
            user_count+=1
            print('Got ', len(np.unique([i['id'] for i in new_tweets])), ' new tweets from user')
            print('Done querying user ', user, 'It is our {} user'.format(user_count))
            print('Start inserting timelines in database')
            insertTweets(conn,c, current_tweets)
        except:
               print 'error user is', user
               exceptionusers.append(user)
    print('Done querying timelines')
    
    print('Now querying profiles of people')
    queryAndInsertUsersProfiles(twitter, c, conn, today, target_users)

	##few line below do the same but should be slower
	# new_users = queryUsersProfiles(twitter, target_users)
	# print('Start inserting user profiles in database')
	# insertUserProfiles(c,conn,new_users,today,today)





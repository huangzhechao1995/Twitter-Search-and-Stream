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
import util

############################################################
####################### Set Parameters #####################
############################################################
args=util.get_args()
credential=args.credential
mode = args.mode
root = args.root
db= args.db
logfilenumber=args.logfilenumber
maxTweetsPerDay = args.maxTweetsPerDay
targetfile = args.targetfile
first_user = args.first_user
targetfile_type=args.filetype
if args.start_date!=None:
    start_date = datetime.strptime(args.start_date,"%Y-%m-%d") # or you can pick start_date = today
    end_date = start_date+timedelta(days=args.date_delta)
if not os.path.exists(db):
    os.makedirs('./'+db)




#mode = 'hashtags'
#db= 'governmentshutdown'
#target = ['governmentshutdown','shut down the government','the shutdown','TrumpShutdown', '#shutdown','NoMoreShutdowns']
assert mode in ['users','hashtags']

if mode=='users':
    
    if targetfile_type=="txt":
        with open(targetfile, 'r') as f:  
            # read the data as binary data stream
            target = f.read().split('\n')
            print(target)
    else:
        with open(targetfile, 'rb') as filehandle:  
            # read the data as binary data stream
            target = pickle.load(filehandle)
            
    log=open("usersScrapingLogs"+logfilenumber+".txt",'w+')

if first_user!=-1:
    assert first_user in target

if mode=='hashtags':
    with open(root+'/hashtagsForSearchTweets/'+targetfile,'r') as f:
        target=f.read().splitlines()
    log=open("tweetsScrapingLogs"+logfilenumber+".txt",'w+')
        
if not os.path.exists(db):
    os.makedirs('./'+db)

conn = sqlite3.connect('./'+db+'/'+db+'.db')
c = conn.cursor()

log.write('--------------------------------------------\n')
log.write('--------------------------------------------\n')
log.write('Job Created {}:\n'.format(datetime.now()))
if mode=='hashtags':
    log.write('hashtags：'+','.join(target)+'\n')
if mode=='users':
    log.write('users:'+','.join(list(map(str,target)))+'\n')

############################################################
####################### Your credentials ###################
############################################################

with open(credential) as f:
    cred=f.read().splitlines()
#Jen's API
APP_KEY, ACCESS_TOKEN, APP_SECRET, callbackUrl= cred[0],cred[1],cred[2],cred[3]
if credential=='credential2.txt': callbackUrl='oob'

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens(callback_url=callbackUrl)

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

earliestTweet=0 # or you can pick latest tweet from previous query
latestTweet=-1

log.write('*db:{}'.format(db))
if mode=='hashtags':
    log.write('*start date:{},end date:{},earliestTweet:{}\n'.format(start_date, end_date, earliestTweet))



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
    log.write("collected {} tweets".format(len(np.unique([i['id'] for i in new_tweets]))))
    log.write("----------------Querying Completed-------------------\n")
    ##optional : query user profiles too... takes time
    print('Now querying profiles of people that posted the tweets')
    queryAndInsertUsersProfilesThatPostedTheTweets(twitter, c, conn, today, new_tweets)
    log.write("----------------Insertion Completed-------------------\n")


#########################################
######## Query a user_timeline ##########
#########################################

elif(mode == 'users'):
    new_tweets = []
    user_count=0
    target_users = [int(i) for i in target]
    print('Start querying timelines')
    first_user_reached=False
    if first_user==-1: 
        first_user_reached=True
    for user in target_users:
        if not first_user_reached:
            print("not reached our first user yet")
            if user==first_user:
                first_user_reached=True
            continue          
        
        try:
            print('Now querying tweets of user ', user)
            current_tweets= queryUserTimeline(twitter,user)
            #new_tweets = new_tweets + current_tweets
            user_count+=1
            print('Got ', len(np.unique([i['id'] for i in current_tweets])), ' new tweets from user')
            log.write('Got '+ str(len(np.unique([i['id'] for i in current_tweets])))+ ' new tweets from user'+'\n')
            print('Done querying user ', user, 'It is our {} user'.format(user_count))
            log.write('Done querying user '+str(user)+'; It is our {} user'.format(user_count)+'\n')
            print('Start inserting timelines in database')
            insertTweets(conn,c, current_tweets)
        except Exception as e:
            print 'error user is', user
            print e
            #raise e
            exceptionusers.append(user)
        
    print('Done querying timelines')
    log.write('Done querying timelines')
    
    print('Now querying profiles of people')
    log.write('Now querying profiles of people')
    queryAndInsertUsersProfiles(twitter, c, conn, today, target_users)
    

	##few line below do the same but should be slower
	# new_users = queryUsersProfiles(twitter, target_users)
	# print('Start inserting user profiles in database')
	# insertUserProfiles(c,conn,new_users,today,today)
log.write('#########Job Completed Successfully##########\n')
log.close()





# Twitter-Search-and-Stream

This repo contains the code to script tweets using various APIs provided by Twitter.  

### Dependencies
**Python** Python 2
Package: **Twython**

### File structure
- Helper.py: It contains the key funtionalities that scrape data from Twitter calling Twitter's API  
- search-Andrew.py: It calls the functions in Helper.py to perform the two main tasks in this project  
    - (1) To Search for all the tweets that contain a specific "keyword within a certain timeframe (the hasttag mode)
    - (2) To download all the past tweets in a user's timeline (The timeline mode)
- stream.py: (currently not used in the project), running this code, it could get the most recent posts of users as live streams
- siftuser.py: This file is not directly related to searching and downloading tweets. This 

### The pipeline
1. prepare the list of keywords and save them in `targetfile` (as mentioned below in the parameter section)
2. run search-Andrew.py using `hashtag` mode
3. sift out the user using their profiles and save the user list to another `targetfile`
4. run search-Andrew.py using `user` mode
 
### Credentials
A twitter developer credential is needed to run the code.  
My personal credential is stored in `credential1.txt` and `credential2.txt`. They can be used to test the code.  
Yet I strongly recommend to apply for new ones for the purpose of future research.  
  
  
### The parameters of the code
In order to call the `search-Andrew.py` from command line, I added parameters parsing as a component of the program. The parameters and their meanings are as follow. Please search `argparser` package for detailed instructions. 

    '--credential', type=str, default="credential2.txt"        #Use this parameter to decide which twitter dev account to use
    '--root', type=str, default="D:/GitHub/Twitter-Search-and-Stream"     #Set
    '--mode',type=str, default="users"                                    # Choose between users/hashtag mode 
    '--db',type=str                                             #the name of the database we want to save our downloaded tweets
    '--targetfile',type=str                       #the input file that saves the hashtags or userlist we want to search with
    '--filetype',type=str,default='binary'            #the type of that input file
    '--start_date',type=str                                      #start date of the tweets we are search for, in the format of 2018
    '--date_delta',type=int, default=1                           #maximum length of the time period we want to scrape
    '--maxTweetsPerDay',type=int, default=60000
    '--first_user',type=int, default=-1                          #designed to resume previous scraping tasks
    '--logfilenumber',type=str, default=''                       #the program will save error information in logfilenumber

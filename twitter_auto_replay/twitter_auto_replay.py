# -*- coding: utf-8 -*-
"""
Created on Fri jan 5 22:59:56 2021

@author: thota
"""

from firebase import firebase
from twython import Twython
#Twython is a Twitter Python library
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
import re

#Calls firebase api through my dataset link
My_firebase = firebase.FirebaseApplication('https://twitter-auto-reply-8c790-default-rtdb.firebaseio.com/', None)

#imports the Twitter API keys

consumer_key='3Q56ksdRfAYlP79tKhiFemYpm'
consumer_secret='T6VE8my2MozjnN74bmUZhQW7VHaV7cmNu75qhM11KdAB1ITZ8d'
access_token="1296786017542787073-5NhH5ncJExwtt2AuCkUcNFcmtB15fg"
access_token_secret='0q2WxGrTaAVOb06OWH8U0zgbMnRV79wb4KFvuGYgbawtA'

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

# Create a SentimentIntensityAnalyzer object. 
sid_obj = SentimentIntensityAnalyzer()

positive_tweets=[]
negative_tweets=[]
neutral_tweets=[]

#++++++ SAVING REPLID ID'S INORDER TO AVOID REPLING TO SAME ID +++++++
ids_replied_to = []
with open('ids_replied_to.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()

    for line in filecontents:
        # remove linebreak which is the last character of the string
        current_place = line[:-1]
        # add item to the list
        ids_replied_to.append(current_place)


#^^^^^^^^^^^^^^^^^^ TO PRINT RESPECTIVE TWEETS^^^^^^^^^^^^^^^^^
def print_tweet(result):
        name = result['user']
        screen_name = name['screen_name']
    
        creation_date = result['created_at']
    
        tweet_txt = result['text']
    
        print('Twitter User:', screen_name)
        print('Posted:')
        print(tweet_txt)
        print('at:')
        print(creation_date)
        print('')
        

#*************TO POST REPLIES TO CORRESPONDING TWEETS***********
def give_replay(resultant):
    name = resultant['user']
    screen_name = name['screen_name']
    creation_date = resultant['created_at']
    tweet_txt = resultant['text']
    print_tweet(resultant)

    id = resultant['id']
    #This posts Tweets
    id = str(id)
    if id in ids_replied_to:
        print('')
        print('Skipped as already replied to')
        print('')
        print('')
    else:
        twitter_handle = '@' + screen_name
        message = twitter_handle + " " + random.choice(rand_message)
        twitter.update_status(status=message, in_reply_to_status_id=id)
        print("Tweeted: %s" % message)
        print("***************** SUCCESSFULLY REPLIED TO THIS TWEET **********************")
        id = int(id)
        ids_replied_to.append(id)
        store_in_firebase(screen_name,creation_date,tweet_txt,message)
        with open('ids_replied_to.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in ids_replied_to)

#****************TO STORE ALL DETAILS IN FIREBASE***************
def store_in_firebase(name,date,tweet,message):
    data_to_upload={
        'cust_name' : name,
        'cust_tweet' : tweet,
        'twee_date' : date,
        'reply_given' : message,
        'sen_tweet' : sid_obj.polarity_scores(tweet)}
    result=My_firebase.post('Tweets replied',data_to_upload)

#*************TO REMOVE LINKS, MENTIONS, TAGS BEFORE ANALYSIS **********
def cleanTxt(text):
            text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
            text = re.sub('#', '', text) # Removing '#' hash tag
            text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
            return text
        
#*******************This searches Tweets********************
search_term = input('What should I look for? ')

limit=int(input('How many tweets to consider'))
results = twitter.cursor(twitter.search, q=search_term,lang='en')


#$$$$$$$$$$$$ TO DIFFERENTIATE TWEETS BASED ON SENTIMENTS $$$$$$$$$$$$$$$$

print('')
print('Searching Twitter...')
print('')
index=0
for result in results:
    index=index+1
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    result['text']=cleanTxt(result['text'])
    sentiment_dict = sid_obj.polarity_scores(result['text']) 
    if sentiment_dict['compound'] >= 0.05 : 
        print("**********Positive Tweet**********") 
        positive_tweets.append(result)
        print_tweet(result)
        for k in sentiment_dict:
            print(k,sentiment_dict[k])
    elif sentiment_dict['compound'] <= - 0.05 : 
        print("**********Negative Tweet**********")
        negative_tweets.append(result)
        print_tweet(result)
        for k in sentiment_dict:
            print(k,sentiment_dict[k])
    else:
        print('************ Neutral Tweet*********')
        neutral_tweets.append(result)
        print_tweet(result)
        for k in sentiment_dict:
            print(k,sentiment_dict[k])
    if index==limit:
        break

#^^^^^^^^^^^^ ASSIGNING DIFFERENT MESSAGES LIST BASED ON SENTIMENTS ^^^^^^^^^^^^^
print("Hurray!! we got the Tweets,Total positive tweets are  ",len(positive_tweets))
print("Total Negative are  ",len(negative_tweets))
print("Total Neutral Tweets are  ",len(neutral_tweets))
response=input("If you want to reply for positive tweets type 'pos', if you want to tweet for negative tweets type 'neg', if you want to tweet for neutral posts type 'neu' ")


if response=="pos":
    rand_message = ['THANK YOU SOO MUCH FOR YOUR LOVE',
                    'THIS TWEET MADE OUR DAY',
                    'OUR TEAM WILL CELEBRATE FOR YOUR LOVE',
                    'THANK YOU SOO MUCH FOR THIS',]
    for p_result in positive_tweets:
        resultant=p_result
        give_replay(resultant)

elif response=="neg":
    rand_message = ['WE ARE SOO SORRY FOR THE INCONVENIENCE PLEASE WRITE THIS TO OUR SUPPORT TEAM',
                    'SORRY, PLEASE WRITE TO OUR SUPPORT TEAM',
                    'WE FEEL SO SAD FOR THIS, PLEASE WRITE TO OUR SUPPORT TEAM',
                    'WE WILL LOOK INTO THIS PROBLEM PLEASE WRITE TO OUR SUPPORT TEAM',]
    for n_result in negative_tweets:
        resultant=n_result
        give_replay(resultant)

elif response=="neu":
    rand_message = ['WE LOOK FORWARD TO SERVE YOU AGAIN',
                    'THANKS FOR REACHING TO US',
                    'WE ALWAYS STRIVE TO GIVE YOU THE BEST',
                    'OUR ORGANISATION MEANT FOR BEST',]
    for neu_result in neutral_tweets:
        resultant=neu_result
        give_replay(resultant)
        
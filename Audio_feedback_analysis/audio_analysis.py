# -*- coding: utf-8 -*-
"""
Created on Sat jan 13 18:23:38 2021

@author: thota
"""

import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

AUDIO_FILE=("Voice 002.wav")
r=sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio=r.record(source)
try:
    print(r.recognize_google(audio))
except sr.UnknownValueError:
    print("not recognised")
except sr.RequestError:
    print("no result")
gen_text=r.recognize_google(audio)
sid_obj = SentimentIntensityAnalyzer()
sentiment_dict = sid_obj.polarity_scores(gen_text)
print("**********SENTIMENT ANALYSIS************")
for k in sentiment_dict:
    print(k,sentiment_dict[k])
if sentiment_dict['compound'] >= 0.05 :
    print("**********Positive statement**********")
    rand_message = ['THANK YOU SOO MUCH FOR YOUR LOVE',
                    'THIS TWEET MADE OUR DAY',
                    'OUR TEAM WILL CELEBRATE FOR YOUR LOVE',
                    'THANK YOU SOO MUCH FOR THIS',]
elif sentiment_dict['compound'] <= - 0.05 :
    print("**********Negative statement**********")
    rand_message = ['WE ARE SOO SORRY FOR THE INCONVENIENCE PLEASE WRITE THIS TO OUR SUPPORT TEAM',
                    'SORRY, FOR THE INCONVINENCE PLEASE WRITE TO OUR SUPPORT TEAM',
                    'WE FEEL SO SAD FOR THIS, PLEASE WRITE TO OUR SUPPORT TEAM',
                    'WE WILL LOOK INTO THIS PROBLEM PLEASE WRITE TO OUR SUPPORT TEAM',]
else:
    print("**********Neuutral Statemnt**********")
    rand_message = ['WE LOOK FORWARD TO SERVE YOU AGAIN',
                    'THANKS FOR REACHING TO US',
                    'WE ALWAYS STRIVE TO GIVE YOU THE BEST',
                    'OUR ORGANISATION MEANT FOR BEST',]
print(random.choice(rand_message))
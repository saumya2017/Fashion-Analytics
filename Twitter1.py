from twython import Twython
import json
import csv
from pymongo import MongoClient
from textblob import TextBlob

#Set parameters
f = open("input.txt", "r")
keyword = (f.read().split("\n"))[0]
tweetsXiteration = 100
done = False; #to collect more data

#Setting the OAuth
Consumer_Key = '3gN0mh60RKpUnyvPY3LOgOH2M';
Consumer_Secret = 'QwcetTY1e4dbah4iTzn3pxqPUvZ3WJdrDdHRO5TmfstGMa3JV2';
Access_Token = '358637575-rjNVSGkO8DeVompLgZS7sSJ9VDkArPdfAhXwhWz1';
Access_Token_Secret = 'TbUQkO0kHlYrXh9KgcPEvuYjtviBxKbJnUIcC82CyzIJE';

#Connection established with Twitter API v1.1
twitter = Twython(Consumer_Key, Consumer_Secret, Access_Token, Access_Token_Secret);

#setting the initials
#dictionary wo
dictionary = {}
dict1 = {}
if keyword == 'bag':
    myList = ['Chanel', 'Fendi', 'Hermes', 'Louis Vuitton', 'Marc Jacobs', 'Prada', 'Kate spade', 'coach']
elif keyword == 'belt':
    myList = ['nautica', 'louis vuitton', 'woodland', 'fossil', 'hermes', 'armani', 'gucci', 'calvin klein', 'tommy hilfiger']
elif keyword == 'lipstick':
    myList = ['revlon', 'lakme', 'loreal', 'colorbar', 'mac', 'nyx', 'maybelline']
elif keyword == 'sunglass':
    myList = ['Dolce & Gabbana', 'Burberry', 'Versace', 'Emporio Armani', 'Prada', 'Gucci', 'Fendi', 'Maui Jim', 'Ray Ban', 'Oakley']


client = MongoClient()
db = client.tweet_db
tweet_collection = db.tweet_collection
output_collection = db.output_collection


for i in myList:
#Twitter is queried
    countTweets = 0
    polarity = 0
    response = twitter.search(q = i, count = tweetsXiteration, result_type = 'mixed');
    tweet_collection.insert(response["statuses"])
    #Results (partial)
    countTweets = len(response['statuses']);
    # print countTweets

    #If all the tweets have been fetched, then we are done
    if not ('next_results' in response['search_metadata']):
        done = True;

    #If not all the tweets have been fetched, then...
    while (done == False):

    #Parsing information for maxID
        parse1 = response['search_metadata']['next_results'].split("&");
        parse2 = parse1[0].split("?max_id=");
        parse3 = parse2[1];
        maxID = parse3;

    #Twitter is queried (again, this time with the addition of 'max_id')
        response = twitter.search(q = i, count = tweetsXiteration, max_id = maxID, include_entities = 1, result_type = 'mixed');
        # print response
        for statuse in response["statuses"]:
            tweet_collection.insert(statuse)
        tweet_cursor = tweet_collection.find({})
        for document in tweet_cursor:
            # print document
            # text = document["text"]
            # blob = TextBlob(text)
            blob = TextBlob(document["text"])
            polarity = polarity + blob.sentiment.polarity
            # document['polarity'] = polarity
            # print document['polarity']
    #Updating the total amount of tweets fetched
        countTweets = countTweets + len(response['statuses']);
        polarity = polarity / len(response['statuses'])
    #If all the tweets have been fetched, then we are done
        if not ('next_results' in response['search_metadata']):
            done = True;

    #print(countTweets);
    dictionary[i] = countTweets
    # dict1[i] = polarity
print dictionary
# print dict1
output_collection.insert({"title":"myList","output":dictionary})

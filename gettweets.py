# This script gathers Tweets using a Twitter API and counts the most common
# content words from two different twitter handles specified by the user.
# Excludes stopwords, URL links, hashtags, retweets, and mentions (@example) from word counts
# The script then displays the top ten most frequent words in a bar plot.
#
# Martin Horst, February 2019
import twitter
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# build api object that stores Tweet information 
def initialize():       
    api = twitter.Api(consumer_key='CcNJQ2hIEIJd5GkVjlBDxeX3u',
      consumer_secret='uxMzyQmvxSCKy5eod6JVDnjoSkIKjZr33TwhSotFiqI8AzHZ9I',
      access_token_key='1088648868659523584-YtC5vHwVw33nMTR80EBgmbuUFYeqWW',
      access_token_secret='aj9fTV1bYA0sA8SQFZPVdxsbB2U2N6aU0hsUBKhO4Cohf', 
      tweet_mode = 'extended')  # for over 140 chars
    return api

# get valid screen names
# handle invalid screen name input
def get_name(api, name1):
    if(name1):
        name = input("Enter the handle of a twitter user with or without @ symbol: ")
    else:
        name = input("Enter the handle of a different twitter user with or without @ symbol: ")
    while True:
        try:
            t = api.GetUser(screen_name=name)
            break
        except Exception:
            name = input("Twitter page '{}' not found. Please retype handle: ".format(name))
    return name

# get valid number of tweets to analyze as integer
# handle ValueErrors
def get_num():
    number_of_tweets = input("How many tweets do you want to analyze? Enter number between 1 and 3200: ")
    while True:
        try:
            number_of_tweets = int(number_of_tweets)
            while int(number_of_tweets) < 1 or int(number_of_tweets) > 3200:
                number_of_tweets = input("'{}' is outside the valid range. Please type an integer between 1 and 3200 : ".format(number_of_tweets))
            break
        except ValueError:
            number_of_tweets = input("'{}' is an invalid number. Please type an integer between 1 and 3200: ".format(number_of_tweets)) 
    return int(number_of_tweets), int(number_of_tweets)

# get tweet data from API and return list of tweets
def get_all_tweet_data (api, name, number_of_tweets):
    all_tweet_data = []
    first_try = True
    while  number_of_tweets > 0 and len(all_tweet_data) < 3200:        
        if len(all_tweet_data) > 0:  # if statement is for 2+ time through the loop
            if len(tweets) == 0:  #  no more tweets in timeline
                break
            max_tweet_id = (tweets[-1]['id']) - 1
            t = api.GetUserTimeline(screen_name=name, count = number_of_tweets, include_rts=False, max_id=max_tweet_id)
        else: # generate a first API using count and not max_id
            t = api.GetUserTimeline(screen_name=name, count = number_of_tweets, include_rts=False)
        tweets = [i.AsDict() for i in t] # get tweet data into dict form
        number_of_tweets = number_of_tweets - len(tweets) # update total tweet number
        for tweet in tweets:
            all_tweet_data.append(tweet)
    return all_tweet_data

# rid list of tokens of punctuation, returns clean tokens
def purify_words(old_words):
    new_words = []
    for word in old_words:
        if '&amp' in word or '@' in word or word.startswith('#') or word.startswith('https'):
            word = ''
        new_word = re.sub(r'\A[^a-zA-Z]+', '', word)
        new_word = re.sub(r'[^a-zA-Z]+\Z', '', new_word)
        new_words.append(new_word)
    return new_words

# get only words from all_tweet_data list
def get_tweet_tokens(all_tweet_data):
    all_tweet_words = []
    for tweet in all_tweet_data:
        all_tweet_words.append(tweet['full_text'])  # full_text argument used for 280 chars of tweet
        
    # tokenize tweets
    stops = set(stopwords.words('english'))
    tweet_tokens = []
    for tweet in all_tweet_words:
        token_list = tweet.split()
        token_list = [word for word in token_list if not word.lower() in stops]
        pure_tokes = purify_words(token_list)
        for toke in pure_tokes:
            if len(toke) > 0:
                tweet_tokens.append(toke.lower())
    return tweet_tokens

# get date of first analyzed tweet
def get_tweet_dates(all_tweet_data):
    dates = []
    for date in all_tweet_data:
        dates.append(date['created_at'])
    first_tweet = dates[-1]
    first_tweet = first_tweet.split()
    first_date = "{} {} {}".format(first_tweet[1], first_tweet[2], first_tweet[-1])
    return first_date

# get content words using API and name
# filter out unnecessary information given by API 
def run_prog(api, name, number_of_tweets):
    all_tweet_data = get_all_tweet_data(api, name, number_of_tweets)
    tweet_tokens = get_tweet_tokens(all_tweet_data)
    first_date = get_tweet_dates(all_tweet_data)
    return tweet_tokens, first_date, len(all_tweet_data)

# create frequency counts from word lists
def create_axes(words):
    fdist = FreqDist(words)
    top_ten = [i[0] for i in fdist.most_common(10)]
    frequency = [i[1] for i in fdist.most_common(10)]
    percent = []
    for f in frequency:
        percent.append(f/len(words) * 100)
    return top_ten, percent

# set color, labels, legends, and type of plot
def format_plot(ax, top_ten, percent, first_date, col, name, tweet_count):
    ax.bar(top_ten, percent, color=col)
    ax.grid(color='w')
    ax.set_ylabel("Word percentage")
    p = mpatches.Patch(color=col, label= " {} ({} total tweets)\n since {}".format(name, tweet_count, first_date))
    ax.legend(handles=[p], fontsize=9)

# run all functions
def main():
    api = initialize()
    name1 = get_name(api, name1=True)
    name2 = get_name(api, name1=False)    
    while name1.lower() is name2.lower():
        print("You must enter a DIFFERENT handle")
        name2 = get_name(api, name1=False)

    if name1.startswith('@'):
        name1 = name1[1:]
    if name2.startswith('@'):
        name2 = name2[1:]
        
    number_of_tweets, orig_tweet_count = get_num()

    tweet_tokens1, first_date1, tweet_count1 = run_prog(api, name1, number_of_tweets)
    tweet_tokens2, first_date2, tweet_count2 = run_prog(api, name2, number_of_tweets)
       
    plt.style.use('classic')
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    top_ten1, percent1 = create_axes(tweet_tokens1)
    format_plot(ax1, top_ten1, percent1, first_date1, "black", name1, tweet_count1)
    top_ten2, percent2 = create_axes(tweet_tokens2)
    format_plot(ax2, top_ten2, percent2, first_date2, "purple", name2, tweet_count2)

    if not name1.startswith('@'):
        name1 = "@{}".format(name1)
    if not name2.startswith('@'):
        name2 = "@{}".format(name2)
        
    plt.suptitle("Most Common Words Tweeted by: \n{} and {}".format(name1, name2), fontsize = 16)
    
    if orig_tweet_count > tweet_count1:
        print("Note: only {} available tweets for {}".format(tweet_count1, name1))
    if orig_tweet_count > tweet_count2:
        print("Note: only {} available tweets for {}".format(tweet_count2, name2))
    plt.show()
    
main()

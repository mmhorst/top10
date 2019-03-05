# Top 10 

by Martin Horst

## About:
Top 10 is a useful programmatic tool that displays the most frequently used content words by two distinct Twitter handles. It is intended for prelimiary data exploration of a Twitter user's latest tweets. Top 10 excludes retweets, @mentions, URL links, and hashtags to focus solely on the most informative words present in up to 3200 tweets.

## Getting started:
To download the latest version of Python please visit: https://www.python.org/downloads/ 

The files [requirements.txt](/requirements.txt) and [setup.py](setup.py) have been provided to help installation run smoothly. Ensure that these files as well as the main script [gettweets.py](/gettweets.py) are placed in the same directory that is used to run similar Python programs.

## Installation:
Top 10 requires certain Python packages found in [requirements.txt](/requirements.txt). To install these packages using the latest Package Installer for Python, run the command: 
```
pip3 install -r requirements.txt
```
Another requirement is downloading the Natural Language Toolkit (NLTK), an open source Python library for Natural Language Processing. To download NLTK, simply run:
```
python3 setup.py
```
This will download all NLTK data and required packages onto your machine.

## Deployment:
After installing the requirements file and the setup file, Top 10 is ready to scrape and analyze tweets. To use Top 10, run the following command:
```
python3 gettweets.py
```
Then follow the prompts given by Top 10 in the command terminal to specify Twitter handles and number of tweets. 

## Comparisons of interest:
The following pairs of twitter handles and tweet numbers produce interesting results. What patterns can you uncover?

@realdonaldtrump @barackobama 2800    *(Donald Trump and Barack Obama)*

@sensanders @senwarren 2450    *(Bernie Sanders and Elizabeth Warren)*

@uwlinguistics @languagemit 700    *(UW Linguistics and Ted Gibson's Language Lab at MIT)*

@natgeo @ngkids 3150   *(National Geographic and National Geographic for Kids)*

## FAQS and Debugging:
During the installation or useage of Top 10, you may encounter the following errors:
### 1) error in command terminal
```
‘some package’ is not recognized as an internal or external command, operable program or batch file.
```
a) Double check that the path of the location of gettweets.py is part of the system’s environmental variables. For help editing path variables, see: https://www.computerhope.com/issues/ch000549.htm  
b) Ensure that all requirements are installed using
```
pip3 install -r requirements.txt
 ```

### 2) error when running nltk.download()
```
[SSL: CERTIFICATE_VERIFY_FAILED]
```
a) See https://stackoverflow.com/questions/41348621/ssl-error-downloading-nltk-data for NLTK error resolution with Mac OS.
b) Run:
```
Applications/Python\ 3.7/Install\ Certificates.command 
```
in terminal to bypass certificate verification.


### 3) error when running gettweets.py script
```
twitter.error.TwitterError: [{'message': 'Rate limit Exceeded', 'code': 88}]
```
a) Twitter imposes rate limiting based either on user tokens or application tokens. 
Please read https://developer.twitter.com/en/docs/basics/rate-limiting for a more detailed explanation of Twitter’s policies.
b) Wait approximately 15 minutes, then try to run the command again. 
c) This error also happens when gettweets.py attempts to scrape the tweets of a Twitter User who has no tweets on their timeline. If this is the case, gettweets.py should be run on a valid, active twitter handle after the 15 minute rest period. 

import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        
        # authenticating
        consumerKey = '1X2SkRnFZCIGd4VZmGtUbyKPD'
        consumerSecret = 'UIQkoJZ1dqzvSm7cndAXE6hdVzOrwOqSLVtFP0JwnTKYIbWBp6'
        accessToken = '834095173348909057-KNMZpB12pJS72fGmdoij4OVCGVoBvLY'
        accessTokenSecret = 't7Dru6smFkrYkXPwosMm69BVXuBSFTc1jtnL0633ZtNAJ'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter a place to fetch tweets: ")
        numTweets = int(input("Enter How many tweets do you want to fetch?: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(numTweets)

        # Open/create a file to append data to
        csvFile = open('tweets.csv', 'w')
        
        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0 
        positive = 0
        weakly_positive = 0
        strongly_positive = 0        
        negative = 0
        weakly_negative = 0
        strongly_negative = 0        
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0): # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                weakly_positive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                strongly_positive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                weakly_negative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                strongly_negative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive            = self.percentage(positive,             numTweets)
        weakly_positive     = self.percentage(weakly_positive,      numTweets)
        strongly_positive   = self.percentage(strongly_positive,    numTweets)
        negative            = self.percentage(negative,             numTweets)
        weakly_negative     = self.percentage(weakly_negative,      numTweets)
        strongly_negative   = self.percentage(strongly_negative,    numTweets)
        neutral             = self.percentage(neutral,              numTweets)

        # finding average reaction
        polarity = polarity / numTweets
        
        # printing out data
        print("How people are feeling in " + searchTerm)
        print()
        print("General Report: ")

        if (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity == 0):
            print("Neutral")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print('Detailed Report: ')
        print(str(positive)             +  "% people feel positive")
        print(str(weakly_positive)      +  "% people feel weakly positive")
        print(str(strongly_positive)    +  "% people feel strongly positive")
        print(str(negative)             +  "% people feel negative")              
        print(str(weakly_negative)      +  "% people feel weakly negative")        
        print(str(strongly_negative)    +  "% people feel strongly negative")
        print(str(neutral)              +  "% people feel neutral")
        

        #with open('victim_data.csv', mode='a', newline='') as victim:
        #    victim = csv.writer(victim, delimiter=',')
        #   victim.writerow([searchTerm,numTweets,strongly_positive,positive,weakly_positive,neutral,weakly_negative,negative,strongly_negative])
                
        # append a new place info. to victim_data.csv
        df = pd.read_csv("victim_data_old.csv")
        df.loc[len(df)] = [searchTerm,numTweets,strongly_positive,positive,weakly_positive,neutral,weakly_negative,negative,strongly_negative]
        df.to_csv (r'victim_data_old.csv', index = False, header=True)
        
        
        self.plotPieChart(positive, weakly_positive, strongly_positive, negative, weakly_negative, strongly_negative, neutral, searchTerm, numTweets)

    # Remove Links, Special Characters etc from tweet
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, weakly_positive, strongly_positive, negative, weakly_negative, strongly_negative, neutral, searchTerm, numTweets):
        labels = ['Positive [' + str(positive) + '%]',
                  'Weakly Positive [' + str(weakly_positive) + '%]',
                  'Strongly Positive [' + str(strongly_positive) + '%]',
                  'Negative [' + str(negative) + '%]', 
                  'Weakly Negative [' + str(weakly_negative) + '%]', 
                  'Strongly Negative [' + str(strongly_negative) + '%]',
                  'Neutral [' + str(neutral) + '%]']
    
        sizes = [positive, weakly_positive, strongly_positive,  negative, weakly_negative, strongly_negative,neutral]
        colors = ['yellowgreen','lightgreen','darkgreen','red','lightsalmon','darkred','gold']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are feeling in ' + searchTerm + ' by analyzing ' + str(numTweets) + ' tweets')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()

check_victim = input("Check places that need physiologist? Yes/No ")
if check_victim == "Yes":    
    df = pd.read_csv("victim_data.csv")
    # Places having Strongly Negative value not 0
    victim = df.loc[df['Strongly_Negative'] != 0]
    print("\nThese Places Need Physiologist : \n",victim)
    







    
    

#Description : This is a sentiment analysis program that parses the tweets fetched from Twitter using Python

#Import the libraries
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np 
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#Load the data
file_name = input("Enter twitter file name = ")
data_set= pd.read_csv(file_name)

#Extract 200 tweets from the file
limit = data_set.shape[0]
N=input("Enter the number of tweets to be analysed (Max Limit : "+ str(limit) +") = " )

column_names = data_set.columns
print(column_names)

for col in column_names:
  if(col in ['tweets','tweet','content','Tweet','Tweets','text']):
    column_name = col
    break
data= data_set[[column_name]].head(int(N))


#To show Full content
pd.options.display.max_colwidth = 500

#Show first 5 tweets
print(data.head())


#clean the text

#create a function to clean the tweets
def cleanText(text):
  text = re.sub(r'@[A-Za-z0-9]+','',text)# Removed @mentions
  text = re.sub(r'#','',text)# Removed '#' symbols
  text = re.sub(r'â€','',text)# Removed ':' symbols
  text = re.sub(r'http:\/\/\S+','',text)# Removed links
  text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)# Removed links
  text = re.sub(r':','',text)# Removed ':' symbols
  text = re.sub(r'"','',text)# Removed '""' symbols
  text = re.sub(r'-','',text)# Removed '-' symbols
  text = re.sub(r'!','',text)# Removed ':' symbols
  text = re.sub(r'|','',text)# Removed ':' symbols

  return text
  
#Cleaning the text
data[column_name] = data[column_name].apply(cleanText)

#Show the cleaned Text
print(data.head())

#Create function to generate Subjectivity and Polarity of the Tweets

#Function For Subjectivity
def getSubjectitivty(text):
  return TextBlob(text).sentiment.subjectivity

#Function For Polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

#Adding the Subjectivity Column to the DataSet
data['Subjectivity'] = data['content'].apply(getSubjectitivty)

#Adding the Polarity Column to the DataSet
data['Polarity'] = data['content'].apply(getPolarity)

#Show the Added Columns to the DataSet
print(data.head())

#Creating the WordCloud

#Collecting Words
allWords = ' '.join( [tweets for tweets in data['content']] )

#Generating the WordCloud
wordCloud = WordCloud(width = 500, height = 300, random_state = 32, max_font_size = 120).generate(allWords)

#Plotting the WordCloud
plt.imshow(wordCloud, interpolation = 'bilinear')
plt.axis('off')# Removing the axis
plt.show()

#Create a function to compute the negative , postive and neutral analysis
def doAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

#Applying the doAnalysis function to polarity scores of the tweets
data['Analysis'] = data['Polarity'].apply(doAnalysis)

#Print the updated DataSet
print(data.head()) 

#Print all the Positive Tweets
x = 1
sortedData = data.sort_values(by = ['Polarity'])
for i in range(0, sortedData.shape[0]):
  if(sortedData['Analysis'][i] == 'Positive'):
    print(str(x) + ') '+sortedData['content'][i])
    print()
    x=x+1

#Print all the Negative Tweets
x = 1
sortedData = data.sort_values(by = ['Polarity'], ascending = 'false')
for i in range(0, sortedData.shape[0]):
  if(sortedData['Analysis'][i] == 'Negative'):
    print(str(x) + ') '+sortedData['content'][i])
    print()
    x=x+1

#Print all the Neutral Tweets
x = 1
sortedData = data.sort_values(by = ['Polarity'])
for i in range(0, sortedData.shape[0]):
  if(sortedData['Analysis'][i] == 'Neutral'):
    print(str(x) + ') '+sortedData['content'][i])
    print()
    x=x+1

#Plot the Polarity and Subjectivity
plt.figure(figsize = (8,6))
for i in range(0,data.shape[0]):
  plt.scatter(data['Polarity'][i], data['Subjectivity'][i], color = 'Red')

plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')

#Get the percentage of Positive Tweets
posTweets = data[data.Analysis == 'Positive']
posTweets = posTweets['content']

round((posTweets.shape[0] / data.shape[0])*100 , 1)

#Get the percentage of Negative Tweets
posTweets = data[data.Analysis == 'Negative']
posTweets = posTweets['content']

round((posTweets.shape[0] / data.shape[0])*100 , 1)

#Get the percentage of Neutral Tweets
posTweets = data[data.Analysis == 'Neutral']
posTweets = posTweets['content']

round((posTweets.shape[0] / data.shape[0])*100 , 1)

#Show the value Counts
data['Analysis'].value_counts()

#plot and visualise the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
data['Analysis'].value_counts().plot(kind = 'bar')
plt.show()




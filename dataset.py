import pandas as pd
import numpy as np 
import os 
import re 
from datetime import datetime 

bot =  raw_input('enter the bot name')

def getdatafromcsv():
    data = pd.read_csv('chats.csv')
    responseDictionary = dict()
    rMessages = data[data['Sender']!= bot]
    sMessages = data[data['Sender']== bot]
    
    combined = pd.concat([sMessages,rMessages])
  
    otherPersonMess,botMess = "",""
    firstMessage = True
    for index, row in data.iterrows():
        if(row['Sender']!=bot):
            if botMess and otherPersonMess :
                #otherPersonMess = cleanMessage(otherPersonMess)
                #botMess =  cleanMessage(botMess)
                responseDictionary[otherPersonMess.rstrip()] = botMess.rstrip()
                otherPersonMess, botMess = "",""
            otherPersonMess = otherPersonMess + str(row['Message'])+ " " 
        else:
            if(firstMessage):
                firstMessage= False
                continue
            botMess = botMess+ str(row['Message']) + ""
    return responseDictionary            

def cleanMessage(message):
	
	cleanedMessage = message.replace('\n',' ').lower()
	
	cleanedMessage = cleanedMessage.replace("\xc2\xa0", "")
	
	cleanedMessage = re.sub('([.,!?])','', cleanedMessage)
	cleanedMessage = re.sub(' +',' ', cleanedMessage)
	return cleanedMessage    

combinedDictionary = {}

print "creating dataset"
combinedDictionary.update(getdatafromcsv())

print "length of dataset", len(combinedDictionary) 
print "saving data to npy"
np.save('chats.npy',combinedDictionary)
convofile = open('convo.txt','w')
for key,value in combinedDictionary.iteritems():
    if(not key.strip() or not value.strip()):
        continue
    convofile.write(key.strip()+value.strip())

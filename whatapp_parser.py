#for changing the Date format to US
import os
import re
def getdata():
    responsedictionary = dict() #key value pairs for char responses.
    mytext,hertext,currentspeaker,lastspeaker="","","",""
    openedfile = open("finalchat.txt",'r+')
    allines = openedfile.readlines()            #total number of lines
    f= open("new.txt","w+")
    #for index, lines in enumerate(allines):
     
    for index,lines in enumerate(allines):
        date=lines[:2]
        month=lines[3:5]
        year=lines[8:10]
        f.write(month+"/"+date+"/"+year+ lines[10:])

getdata()            
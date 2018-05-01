import tensorflow as tf
import numpy as np 
import sys
from random import randint
import datetime
from sklearn.utils import shuffle
import pickle
import os


def createTrainingMatrix(convoFile,wlist,maxLen):
    convoDictionary = np.load(convoFile).item()
    numExamples = len(convoDictionary)
    xTrain = np.zeros((numExamples,maxLen), dtype='int32')
    yTrain = np.zeros((numExamples,maxLen), dtype='int32')
    for index,(key,value) in enumerate(convoDictionary.iteritems()):
        #need to store integerized representation of strings here
        #initialised as padding

        encoderMessage = np.full((maxLen),wlist.index('<pad>'),dtype='int32')
        


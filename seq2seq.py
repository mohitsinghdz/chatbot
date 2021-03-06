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
    print "num ex:", numExamples
    xTrain = np.zeros((numExamples,maxLen), dtype='int32')
    yTrain = np.zeros((numExamples,maxLen), dtype='int32')
    print "XTRAIN  :",xTrain
    
    for index,(key,value) in enumerate(convoDictionary.iteritems()):
        #need to store integerized representation of strings here
        #initialised as padding
        #print "key "+ key + "value "+ value
              
        encoderMessage = np.full((maxLen),wlist.index('<pad>'),dtype='int32')
        decoderMessage = np.full((maxLen),wlist.index('<pad>'),dtype="int32")
        #print encoderMessage
        #getting all the individual words in a single string as a list
        keySplit =  key.split()
        valueSplit = value.split()
        keyCount = len(keySplit)
        valueCount = len(valueSplit)

        #throw sentences that are either too empty or long

        if(keyCount > (maxLen - 1) or valueCount > (maxLen - 1) or valueCount == 0 or keyCount == 0 ):
            continue
        
        #integerizing the encoded string
        for keyIndex, word in enumerate(keySplit):
            try:
                    encoderMessage[keyIndex] = wlist.index(word)
            except ValueError:
                    encoderMessage[keyIndex] = 0
        encoderMessage[keyIndex + 1] = wlist.index('<EOS>')
#decoded string	
        for valueIndex, word in enumerate(valueSplit):
			try:
				decoderMessage[valueIndex] = wlist.index(word)
			except ValueError:
				decoderMessage[valueIndex] = 0
        decoderMessage[valueIndex + 1] = wlist.index('<EOS>')         
        xTrain[index] = encoderMessage
        yTrain[index] =  decoderMessage
    # Remove rows with all zeros
    
    yTrain = yTrain[~np.all(yTrain == 0, axis=1)]
    xTrain = xTrain[~np.all(xTrain == 0, axis=1)]
    print "Xtrain 2 : ",xTrain
    numExamples = xTrain.shape[0]
    return numExamples, xTrain, yTrain
#cant gaurantee will it work or not 
def getTrainingBatch(localXTrain, localYTrain, localBatchSize, maxLen):
    print numTrainingExamples 
    print localBatchSize
    
    num = randint(0,numTrainingExamples - localBatchSize - 1)
    
    arr = localXTrain[num:num + localBatchSize]
    labels = localYTrain[num:num + localBatchSize]
	# Reversing the order of encoder string apparently helps as per 2014 paper
    reversedList = list(arr)
    for index,example in enumerate(reversedList):
		reversedList[index] = list(reversed(example))

	# Lagged labels are for the training input into the decoder
    laggedLabels = []
    EOStokenIndex = wordlist.index('<EOS>')
    padTokenIndex = wordlist.index('<pad>')
    for example in labels:
		eosFound = np.argwhere(example==EOStokenIndex)[0]
		shiftedExample = np.roll(example,1)
		shiftedExample[0] = EOStokenIndex
		# The EOS token was already at the end, so no need for pad
		if (eosFound != (maxLen - 1)):
			shiftedExample[eosFound+1] = padTokenIndex
		laggedLabels.append(shiftedExample)

	# Need to transpose these 
    reversedList = np.asarray(reversedList).T.tolist()
    labels = labels.T.tolist()
    laggedLabels = np.asarray(laggedLabels).T.tolist()
    return reversedList, labels, laggedLabels

def translateToSentences(inputs, wList, encoder=False):
	EOStokenIndex = wList.index('<EOS>')
	padTokenIndex = wList.index('<pad>')
	numStrings = len(inputs[0])
	numLengthOfStrings = len(inputs)
	listOfStrings = [''] * numStrings
	for mySet in inputs:
		for index,num in enumerate(mySet):
			if (num != EOStokenIndex and num != padTokenIndex):
				if (encoder):
					# Encodings are in reverse!
					listOfStrings[index] = wList[num] + " " + listOfStrings[index]
				else:
					listOfStrings[index] = listOfStrings[index] + " " + wList[num]
	listOfStrings = [string.strip() for string in listOfStrings]
	return listOfStrings

def getTestInput(inputMessage, wList, maxLen):
	encoderMessage = np.full((maxLen), wList.index('<pad>'), dtype='int32')
	inputSplit = inputMessage.lower().split()
	for index,word in enumerate(inputSplit):
		try:
			encoderMessage[index] = wList.index(word)
		except ValueError:
			continue
	encoderMessage[index + 1] = wList.index('<EOS>')
	encoderMessage = encoderMessage[::-1]
	encoderMessageList=[]
	for num in encoderMessage:
		encoderMessageList.append([num])
	return encoderMessageList

def idsToSentence(ids, wList):
    EOStokenIndex = wList.index('<EOS>')
    padTokenIndex = wList.index('<pad>')
    myStr = ""
    listOfResponses=[]
    for num in ids:
        if (num[0] == EOStokenIndex or num[0] == padTokenIndex):
            listOfResponses.append(myStr)
            myStr = ""
        else:
            myStr = myStr + wList[num[0]] + " "
    if myStr:
        listOfResponses.append(myStr)
    listOfResponses = [i for i in listOfResponses if i]
    return listOfResponses


#hyper parameteres
batchSize = 24
maxEncoderLength = 15 
maxDecoderLength = 15
lstmUnits = 112
embeddingDim = lstmUnits
numLayersLSTM = 3
numIterations = 500000

#loading in all the data structures 
with open("wordlist.txt","rb") as fp:
    wordlist = pickle.load(fp)

vocabSize = len(wordlist)

#if ill use my own word to vec algo then these line should be used
#in embeddingMatrix
if (os.path.isfile('embeddingMatrix.npy')):
	wordVectors = np.load('embeddingMatrix.npy')
	wordVecDimensions = wordVectors.shape[1]  

#for future use
wordVecDimensions = int(input('since i cant not find an embedding matrix, how many dimensions do you want your word vectors to be? ;'))

#add two entries to the word vector matrix, one to represent padding token
#one to represent an end of sentece token
padVector = np.zeros((1,wordVecDimensions), dtype='int32')
EOSVector = np.ones((1,wordVecDimensions),dtype='int32')

if( os.path.isfile('embeddingMatrix.npy')):
    wordVectors = np.concatenate((wordVectors,padVector),axis = 0)
    wordVectors = np.concatenate((wordVectors,EOSVector),axis = 0)
    
#need to modify the word list as well
wordlist.append('<pad>')
wordlist.append('<EOS>')
vocabSize = vocabSize + 2


if (os.path.isfile('Seq2SeqXTrain.npy') and os.path.isfile('Seq2SeqYTrain.npy')):
    xTrain =  np.load('Seq2SeqXTrain.npy')
    yTrain = np.load('Seq2SeqYTrain.npy')
    print 'finished loading training matrices'
    numTrainingExamples = xTrain.shape[0]
else: #if the program is running for the first time
    numTrainingExamples, xTrain, yTrain = createTrainingMatrix('chats.npy',wordlist,maxEncoderLength)

    np.save('Seq2SeqXTrain.npy',xTrain)
    np.save('Seq2SeqYTrain.npy',yTrain)
    print 'Finished creating training matrices'

tf.reset_default_graph()

#making placeholders

encoderInputs = [tf.placeholder(tf.int32,shape=(None,)) for i in range(maxEncoderLength)]
decoderLabels = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxDecoderLength)]
decoderInputs = [tf.placeholder(tf.int32, shape=(None,)) for i in range (maxDecoderLength)] 
feedPrevious = tf.placeholder(tf.bool)

encoderLSTM = tf.nn.rnn_cell.BasicLSTMCell(lstmUnits, state_is_tuple=True)

#mohit try this later
#encoderLSTM = tf.nn.rnn_cell.MultiRNNCell([singleCell]*numLayersLSTM, state_is_tuple=True)  

#decoderOutputs,decoderFinalState = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(encoderInputs, decoderInputs, )
decoderOutputs, decoderFinalState = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(encoderInputs, decoderInputs, encoderLSTM, vocabSize, vocabSize, embeddingDim, feed_previous=feedPrevious)
decoderPrediction = tf.argmax(decoderOutputs, 2)

lossWeight = [tf.ones_like(l,dtype=tf.float32) for l in decoderLabels]
loss = tf.contrib.legacy_seq2seq.sequence_loss(decoderOutputs, decoderLabels, lossWeight, vocabSize)

optimizer = tf.train.AdamOptimizer(1e-4).minimize(loss)
 

sess =tf.Session()
saver =tf.train.Saver()

#if i am using a saved model, use the following
# saver.restore(sess,tf.train.latest_checkpoint('model/'))
sess.run(tf.global_variables_initializer())


#uploading to tenson board
tf.summary.scalar('Loss',loss)
merged = tf.summary.merge_all()
logdir = "tensorboard/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"
writer = tf.summary.FileWriter(logdir,sess.graph)


#test strings
encoderTestStrings = ["hi there",
                        "hi",
                        "hello",
                        "Good morning",
                        "How r you"
                        
                        ]
zeroVector = np.zeros((1), dtype='int32')

for i in range(numIterations):
    encoderTrain, decoderTargetTrain, decoderInputTrain = getTrainingBatch(xTrain, yTrain, batchSize, maxEncoderLength)
    print encoderTrain
    feedDict = {encoderInputs[t]: encoderTrain[t] for t in range(maxEncoderLength)}
    feedDict.update({decoderLabels[t]: decoderTargetTrain[t] for t in range(maxDecoderLength)})
    feedDict.update({decoderInputs[t]: decoderInputTrain[t] for t in range(maxDecoderLength)})
    feedDict.update({feedPrevious: False})

    curLoss, _, pred = sess.run([loss, optimizer, decoderPrediction], feed_dict=feedDict)
	
    if (i % 50 == 0):
		print('Current loss:', curLoss, 'at iteration', i)
		summary = sess.run(merged, feed_dict=feedDict)
		writer.add_summary(summary, i)
    if (i % 25 == 0 and i != 0):
		num = randint(0,len(encoderTestStrings) - 1)
		print encoderTestStrings[num]
		inputVector = getTestInput(encoderTestStrings[num], wordlist, maxEncoderLength)
		feedDict = {encoderInputs[t]: inputVector[t] for t in range(maxEncoderLength)}
		feedDict.update({decoderLabels[t]: zeroVector for t in range(maxDecoderLength)})
		feedDict.update({decoderInputs[t]: zeroVector for t in range(maxDecoderLength)})
		feedDict.update({feedPrevious: True})
		ids = (sess.run(decoderPrediction, feed_dict=feedDict))
		print idsToSentence(ids, wordlist)

    if (i % 10000 == 0 and i != 0):
		savePath = saver.save(sess, "models/pretrained_seq2seq.ckpt", global_step=i)

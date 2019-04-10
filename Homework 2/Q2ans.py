import csv
import json, pickle
import sys

def read_data(fileName):
	data = []
	file = open(fileName, "r")

	for sentence in file.read().split(' . '):
		for word in sentence.split():
			data.append(word)

	file.close()
	return data


def create_Bigram(data):
	listOfBigrams = []
	bigramCounts = {}
	unigramCounts = {}
	nbyn = {}

	for i in range(len(data)):
		if i < len(data) - 1:

			listOfBigrams.append((data[i], data[i + 1]))

			if (data[i], data[i+1]) in bigramCounts:
				bigramCounts[(data[i], data[i + 1])] += 1
			else:
				bigramCounts[(data[i], data[i + 1])] = 1

		if data[i] in unigramCounts:
			unigramCounts[data[i]] += 1
		else:
			unigramCounts[data[i]] = 1

	return listOfBigrams, unigramCounts, bigramCounts


# ------------------------------ Simple Bigram Model --------------------------------


def calc_bigram_prob(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}
	for bigram in listOfBigrams:
		word1 = bigram[0]
		word2 = bigram[1]
		
		listOfProb[bigram] = (bigramCounts.get(bigram))/(unigramCounts.get(word1))

	file = open('bigramProb.txt', 'w')
	file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

	for bigrams in listOfBigrams:
		file.write(str(bigrams) + ' : ' + str(bigramCounts[bigrams])
				   + ' : ' + str(listOfProb[bigrams]) + '\n')

	file.close()

	return listOfProb


# ------------------------------- Add One Smoothing ---------------------------------


def add_One_smothing(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}
	cStar = {}


	for bigram in listOfBigrams:
		word1 = bigram[0]
		word2 = bigram[1]
		listOfProb[bigram] = (bigramCounts.get(bigram) + 1)/(unigramCounts.get(word1) + len(unigramCounts))
		cStar[bigram] = (bigramCounts[bigram] + 1) * unigramCounts[word1] / (unigramCounts[word1] + len(unigramCounts))

	file = open('addOneSmoothing.txt', 'w')
	file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

	for bigrams in listOfBigrams:
		file.write(str(bigrams) + ' : ' + str(bigramCounts[bigrams])
				   + ' : ' + str(listOfProb[bigrams]) + '\n')

	file.close()

	return listOfProb, cStar


# ---------------------------- Good Turing Discounting ------------------------------


def good_turing_discounting(listOfBigrams, bigramCounts, totalNumberOfBigrams):
	listOfProb = {}
	bucket = {}
	bucketList = []
	cStar = {}
	pStar = {}
	listOfCounts = {}
	i = 1

	for bigram in bigramCounts.items():
		key = bigram[0]
		value = bigram[1]
		
		if not value in bucket:
			bucket[value] = 1
		else:
			bucket[value] += 1	

	# Sorted Bucket
	print("bucket = ")
	print(bucket)
	bucketList = sorted(bucket.items() , key=lambda t : t[0])
	zeroOccurenceProb = bucketList[0][1] / totalNumberOfBigrams
	lastItem = bucketList[len(bucketList)-1][0]

	for x in range(1, lastItem):
		if x not in bucket:
			bucket[x] = 0

	bucketList = sorted(bucket.items() , key=lambda t : t[0])
	lenBucketList = len(bucketList)
	print("BucketList = ")
	print(bucketList)
	for k, v in bucketList:

		if i < lenBucketList-1:
			if v == 0:
				cStar[k] = 0
				pStar[k] = 0

			else:
				cStar[k] = (i+1) * bucketList[i][1] / v
				#print("bucketList = ",bucketList[i][1])
				#print("v = ",v)
				pStar[k] = cStar[k] / totalNumberOfBigrams

		else:
			cStar[k] = 0
			pStar[k] = 0

		i += 1


	for bigram in listOfBigrams:
		listOfProb[bigram] = pStar.get(bigramCounts[bigram])
		listOfCounts[bigram] = cStar.get(bigramCounts[bigram])



	file = open('good_turing_discounting.txt', 'w')
	file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

	for bigrams in listOfBigrams:
		file.write(str(bigrams) + ' : ' + str(bigramCounts[bigrams])
				   + ' : ' + str(listOfProb[bigrams]) + '\n')

	file.close()

	return listOfProb, zeroOccurenceProb, listOfCounts


if __name__ == '__main__':

	fileName = 'q2dataset'
	data = read_data(fileName)
	listOfBigrams, unigramCounts, bigramCounts = create_Bigram(data)
	bigramProb = calc_bigram_prob(listOfBigrams, unigramCounts, bigramCounts)
	bigramAddOne, addOneCstar = add_One_smothing(listOfBigrams, unigramCounts, bigramCounts)
	bigramGoodTuring, zeroOccurenceProb, goodTuringCstar = good_turing_discounting(listOfBigrams, bigramCounts, len(listOfBigrams))


	# ------------------------------------- Testing --------------------------------------

	input = sys.argv[1]
	#input = "The Fed chairman warned that the board's decision is bad"
	inputList = []
	bigramOutput = open('bigramProb-OUTPUT.txt', 'w')
	addOneSmoothingOutput = open('addOneSmoothing-OUTPUT.txt', 'w')
	goodTuringOutput = open('good_turing_discounting-OUTPUT.txt', 'w')

	bigram_probs = 1
	add_one_smoth_output = 1
	goodTuringprob = 1

	for i in range(len(input.split())-1):
		inputList.append((input.split()[i], input.split()[i+1]))

	print (inputList)


	# ------------------------------ Simple Bigram Model --------------------------------


	bigramOutput.write('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n\n')
	for i in range(len(inputList)):
		if inputList[i] in bigramProb:
			bigramOutput.write(str(inputList[i]) + '\t\t' + str(bigramCounts[inputList[i]]) + '\t\t' + str(bigramProb[inputList[i]]) + '\n')
			bigram_probs *= bigramProb[inputList[i]]
		else:
			bigramOutput.write(str(inputList[i]) + '\t\t\t' + str(0) + '\t\t\t' + str(0) + '\n')
			bigram_probs *= 0

	bigramOutput.write('\n' + 'Probablility = ' + str(bigram_probs))
	print ('Bigram Model: ', bigram_probs)

	# ------------------------------- Add One Smoothing ---------------------------------


	addOneSmoothingOutput.write('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n\n')
	for i in range(len(inputList)):
		if inputList[i] in bigramAddOne:
			addOneSmoothingOutput.write(str(inputList[i]) + '\t\t' + str(addOneCstar[inputList[i]]) + '\t\t' + str(bigramAddOne[inputList[i]]) + '\n')
			add_one_smoth_output *= bigramAddOne[inputList[i]]
		else:
			if inputList[i][0] not in unigramCounts:
				unigramCounts[inputList[i][0]] = 1
			prob = (1) / (unigramCounts[inputList[i][0]] + len(unigramCounts))
			addOneCStar = 1 * unigramCounts[inputList[i][0]] / (unigramCounts[inputList[i][0]] + len(unigramCounts))
			add_one_smoth_output *= prob
			addOneSmoothingOutput.write(str(inputList[i]) + '\t' + str(addOneCStar) + '\t' + str(prob) + '\n')

	addOneSmoothingOutput.write('\n' + 'Probablility = ' + str(add_one_smoth_output))
	print ('Add One: ', add_one_smoth_output)


	# ---------------------------- Good Turing Discounting ------------------------------


	goodTuringOutput.write('Bigram\t\t\t\t' + 'CStar\t\t\t\t' + 'Probability\n\n')
	for i in range(len(inputList)):
		if inputList[i] in bigramGoodTuring:
			goodTuringOutput.write(str(inputList[i]) + '\t\t' + str(goodTuringCstar[inputList[i]]) + '\t\t' + str(bigramGoodTuring[inputList[i]]) + '\n')
			goodTuringprob *= bigramGoodTuring[inputList[i]]
		else:
			goodTuringOutput.write(str(inputList[i]) + '\t\t\t' + str(0) + '\t\t\t' + str(zeroOccurenceProb) + '\n')
			goodTuringprob *= zeroOccurenceProb

	goodTuringOutput.write('\n' + 'Probablility = ' + str(goodTuringprob))
	print ('Good Turing: ' , goodTuringprob)


	print('UnigramCounts = ',unigramCounts)
	print('number of unigrams = ',len(unigramCounts))
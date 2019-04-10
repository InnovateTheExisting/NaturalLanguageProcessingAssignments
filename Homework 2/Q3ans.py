import sys
from collections import Counter

def read_data(fileName):
	data = []
	Tokens = []
	tags = []

	file = open(fileName, 'r')

	for sentence in file.read().split('\n'):
		for word in sentence.split():
			Tokens.append(word.split('_')[0])
			tags.append(word.split('_')[1])

	return data, Tokens, tags


def create_Unigrams(Tokens, tags):
	token_tags = {}
	unique_tags = set(tags)

	# {and: [VB, NN, VB, NN]}

	for i in range(len(Tokens)):
		if not Tokens[i] in token_tags:
			token_tags[Tokens[i]] = [tags[i]]
		else:
			token_tags[Tokens[i]].append(tags[i])

	return token_tags, unique_tags


def most_Probable_POS(dictionary):

	for key, value in dictionary.items():

		counter = Counter(value)
		maxValue = counter.most_common()[0]
		dictionary[key] = maxValue[0]

	return dictionary


def most_probable_errors(Tokens, tags, dictionary):
	mod_tags = []
	error = 0

	for word in Tokens:
		mod_tags.append(dictionary[word])

	for i in range(len(mod_tags)):
		if mod_tags[i] != tags[i]:
			error += 1


	int2 = open('mostProbableTags.txt', 'w')
	int2.write('Word' + '\t\t' + 'Most Probable Tag' + '\n\n')

	for i in range(len(tags)):
		int2.write(str(Tokens[i]) + '\t\t\t' + str(mod_tags[i]) + '\n')

	int2.close()


	return mod_tags


def brills_POS(tags, mostProbableTags, unique_tags):
	brills_template = {}
	mod_tags = mostProbableTags[:]

	# for loop traversing the unique_tags - for from - from tag1 to tagn
	# for loop traversing the unique_tags - for to - from tag1 to tagn
	# for loop traversing the mod_tags/tags - from 1 to corpus size


	# Traversing on the corpus tags
	# For good error,
	# if tag[currentPosition] == to Tag from the rule
	# AND modTag[currentPosition] == from Tag from the rule
	# 		then, GoodError + 1

	# For bad error,
	# if tag[currentPosition] == from Tag from the rule
	# AND modTag[currentPosition] == from Tag from the rule
	# 		then, BadError + 1

	index = 0

	while index < 10:
		threshold = 0
		index += 1
		print ('Rule ', index)
		for fromTag in unique_tags:
			for toTag in unique_tags:

				brills_ruleDictionary = {}
				if fromTag == toTag:
					continue

				for pos in range(1,len(mod_tags)):
					if tags[pos] == toTag and mod_tags[pos] == fromTag:

						#rule = (PREVIOUS_TAG, FROM, TO)
						rule = (mod_tags[pos-1], fromTag, toTag)
						if rule in brills_ruleDictionary:
							brills_ruleDictionary[rule] += 1
						else:
							brills_ruleDictionary[rule] = 1

					elif tags[pos] == fromTag and mod_tags[pos] == fromTag:

						rule = (mod_tags[pos-1], fromTag, toTag)
						if rule in brills_ruleDictionary:
							brills_ruleDictionary[rule] -= 1
						else:
							brills_ruleDictionary[rule] = -1

				if brills_ruleDictionary:
					maxValueKey = max(brills_ruleDictionary, key=brills_ruleDictionary.get)
					maxValue = brills_ruleDictionary.get(maxValueKey)

					if maxValue > threshold:
						threshold = maxValue
						tupel = maxValueKey

		for i in range(len(mod_tags)-1):
			if mod_tags[i] == tupel[0] and mod_tags[i+1] == tupel[1]:
				mod_tags[i+1] = tupel[2]

		brills_template[tupel] = threshold

	sorted_brills_template = sorted(brills_template.items(), key=lambda x: x[1], reverse=True)

	int1 = open('brillsTags.txt', 'w')
	int1.write('PREVIOUS WORD' + '\t\t' + 'FROM' + '\t\t' + 'TO' + '\t\t' + 'SCORE' + '\n\n')

	for i in range(len(sorted_brills_template)):
		int1.write(str(sorted_brills_template[i][0][0]) + "\t\t" + str(sorted_brills_template[i][0][1]) + "\t\t" +
				   str(sorted_brills_template[i][0][2]) + "\t\t" + str(sorted_brills_template[i][1]) + "\n" )

	int1.close()

	return sorted_brills_template


if __name__ == '__main__':
	fileName = 'q3dataset'
	data, Tokens, tags = read_data(fileName)
	Unigrams, unique_tags = create_Unigrams(Tokens, tags)
	most_Probable_POS = most_Probable_POS(Unigrams)
	mod_tags = most_probable_errors(Tokens, tags, most_Probable_POS)
	brills_rule = brills_POS(tags, mod_tags, unique_tags)


	# ------------------------------------- Testing --------------------------------------

	#input = sys.argv[1]
	input = "The_DT standard_?? Turbo_NN engine_NN is_VBZ hard_JJ to_TO work_??"
	inputList = []
	inputTokens = []
	inputGoldTags = []
	input_most_probable = []
	most_probable_errorIndex = []
	brillRuleErrorIndex = []
	most_probable_error = 0
	brillRuleError = 0


	for i in range(len(input.split())):
		if i < (len(input.split()) - 1):
			inputList.append((input.split()[i], input.split()[i + 1]))
		inputTokens.append(input.split()[i].split('_')[0])
		inputGoldTags.append(input.split()[i].split('_')[1])


	for i in range(len(inputTokens)):
		input_most_probable.append(most_Probable_POS[inputTokens[i]])

	inputBrills = input_most_probable[:]

	for i in range(len(input_most_probable)-1):
		for k, v in brills_rule:
			prev = k[0]
			frm = k[1]
			to = k[2]

			if inputBrills[i] == prev and inputBrills[i+1] == frm:
				inputBrills[i+1] = to
				brillRuleErrorIndex.append(i+1)
				break


	for i in range(len(inputGoldTags)):
		if(inputGoldTags[i] != input_most_probable[i]):
			most_probable_errorIndex.append(i)
			most_probable_error += 1
		if(inputGoldTags[i] != inputBrills[i]):
			brillRuleError += 1

	print ('\n')

	print ('Most Probable Tag Error Rate: ', most_probable_error/len(inputGoldTags))
	print ('Brills Tag Error Rate: ', brillRuleError / len(inputGoldTags))

	output1 = open('mostProbable-OUTPUT.txt', 'w')
	output2 = open('brillsTagging-OUTPUT.txt', 'w')

	output1.write('Word' + '\t\t' + 'Most Probable Tag' + '\n\n')
	output2.write('Word' + '\t\t' + 'Brills Tag' + '\n\n')

	for i in range(len(inputTokens)):
		output1.write(str(inputTokens[i]) + '\t\t\t' + str(input_most_probable[i]) + '\n')
		output2.write(str(inputTokens[i]) + '\t\t\t' + str(inputBrills[i]) + '\n')

	output1.write('\nMost Probable Tag Error Rate: ' + str(most_probable_error/len(inputGoldTags)))
	output2.write('\nBrills Tag Error Rate: ' + str(brillRuleError / len(inputGoldTags)))

	output1.close()
	output2.close()
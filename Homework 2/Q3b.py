import random

f1=open("q3dataset","r")
tagDict={}     
wordAndTagDictionary={} 
for line in f1:
    tokens=line.rstrip().split()
    for token in tokens:
        token=token.lower()
        if not token in wordAndTagDictionary.keys():
            wordAndTagDictionary[token]=1
        else:
            wordAndTagDictionary[token]=wordAndTagDictionary[token]+1        
        token_break=token.split("_")
        word=token_break[0]
        tag=token_break[1]
        if not tag in tagDict.keys():
            tagDict[tag]=1
        else:
            tagDict[tag]=tagDict[tag]+1
        
total_no_of_tags=sum(tagDict.values())

##########testing################################

f1=open("q3btest","r")
f2=open("q3bresults.txt","w")
f3=open("q3bprobability_of_all_tags_given_word.txt","w")
tagGivenTheWord={}
for line in f1:
    #f2.write(line)
    words=line.rstrip().split()
    for wordToken in words :
        word=wordToken.lower()
        maxProbabilityOfTag=0
        predicted_tags_with_max_probability=[] 
        predicted_tags_with_max_probability.append("nnp") 
        for tag in tagDict.keys():
            priorOfTheTag=tagDict[tag]/float(total_no_of_tags) 
            print("tag = ",tag, "prior = ",priorOfTheTag)

            #print("prior of tag = ")
            #print(priorOfTheTag)
            wordTag=word+"_"+tag   
            if wordTag in wordAndTagDictionary.keys():
                likelihood_of_word_given_tag=wordAndTagDictionary[wordTag]/float(tagDict[tag])
                probOfTagGivenTag=priorOfTheTag * likelihood_of_word_given_tag
                
                if probOfTagGivenTag>maxProbabilityOfTag:
                    predicted_tags_with_max_probability=[] 
                    predicted_tags_with_max_probability.append(tag)
                elif probOfTagGivenTag==maxProbabilityOfTag:  
                    predicted_tags_with_max_probability.append(tag)
                    
                
                if not wordTag in tagGivenTheWord.keys():
                    tagGivenTheWord[wordTag]=probOfTagGivenTag
                    f3.write("p("+tag.upper()+"|"+wordToken+")"+":"+str(tagGivenTheWord[wordTag])+"\n")
            else :
                if not wordTag in tagGivenTheWord.keys():
                    tagGivenTheWord[wordTag]=0
                    f3.write("p("+tag.upper()+"|"+wordToken+")"+":"+str(tagGivenTheWord[wordTag])+"\n")
        f2.write(wordToken+"_"+random.choice(predicted_tags_with_max_probability).upper()+" ") 
       
    f2.write("\n")    
f3.close()
f2.close()    

            
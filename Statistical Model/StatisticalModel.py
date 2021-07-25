#Number Of Documents
N = 3

#function to generate a random string
def randString(n):
    import random
    alpha , res = "ABCDE" , ""
    for i in range(int(random.random()*20+10)):
        res += alpha[int(random.random()*len(alpha))]
    return res

#function to save a string in a flile, note that the file name must be between quotation marks and the file must be in the same folder
def saveString(s , fileName):
    f = open(fileName , 'w')
    f.write(s)
    f.close

#function to read a file, note that the file name must be between quotation marks and the file must be in the same folder
def readFileAsString(fileName):
    f = open(fileName , 'r')
    myString = f.readline()
    f.close
    return myString

#functions to measure the frequency of letters in a given string
def getFrequency(s):
    res = {} 
    for keys in s: 
        res[keys] = (res.get(keys, 0) + 1)
    return res
    
def freqCounter(s):
    import copy
    s = s.replace('\n' , '')
    dic = getFrequency(s)
    res = copy.deepcopy(dic)
    for i in dic:
        res[i] = dic[i] / len(s)
    return res


#Edit query and save it in a dictionary
def editQuery(query):
    queryEdited = query.split(" ")
    queryDic = {}
    for i in range(len(queryEdited)):
        queryDic[queryEdited[i][0]] = float(queryEdited[i][2:])
    return queryDic

# Generating random strings and saving them in files D1,D2,D3 up to Dn
for i in range(1,N+1):
    saveString(randString(10) , "D" + str(i) + ".txt")

#sorting dictionary keys alphabetically
def sortDic(Dic):
    sortedList , sortedDic = sorted(list(Dic.items())) , {}
    for i in range(len(sortedList)):
       sortedDic [sortedList[i][0]] = sortedList[i][1]
    Dic = sortedDic
    return Dic

#adding unexistant keys with values equal to zero
def addValuesToDic(Dic , query):
    queryKeys = sorted(editQuery(query).keys())
    for i in range(len(queryKeys)):
        if queryKeys[i] not in Dic:
            Dic[queryKeys[i]] = 0
    return sortDic(Dic)

def similarityFunc(Dic,query):
    document , queryDocument , score = sortDic(Dic) , sortDic(editQuery(query)) , 0
    for i in queryDocument:
        for j in document:
            if i == j:
                score += queryDocument[i] * document[j]
                break
    return score

#function to sort documents according to similarity
def sortDocuments(query):
    similarityDic = {"D1" : similarityFunc(freqCounter(readFileAsString("D1.txt")) ,query)}
    for i in range(N-1):
        similarityDic ["D" + str(i+2)] = similarityFunc(freqCounter(readFileAsString("D" + str(i+2) + ".txt")),query)
    return sorted(list(similarityDic.items()), key=lambda x: x[1], reverse=True)

def showRes(query):
    res = "Search results Are:- \n\n"
    for i in range(len(sortDocuments(query))):
        res += str(sortDocuments(query)[i][0]) + ": " + str(round(sortDocuments(query)[i][1]*100,4)) + "%" + "\n"
    return res

test = "A:0.2 B:0.9 D:0.8"
print(showRes(test))
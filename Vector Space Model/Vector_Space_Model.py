#Number Of Documents
N = 2

#function to generate a random string
def randString(n):
    import random
    alpha , res = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" , ""
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

# #Generating random strings and saving them in files D1,D2,D3,D4 and D5
# for i in range(1,6):
#     saveString(randString(10) , "D" + str(i) + ".txt")

#function to search for a specific key in a dictionary
def serachnKeyObject(dict , value):
    for i in range(len(dict.keys())):
        if list(dict.keys())[i] == value:
            return list(dict.keys())[i]

#function to measure the frequency of letters in a given string
def freqCounter(s):
    res = {} 
    s = s.replace('\n' , '')
    for keys in s: 
        res[keys] = (res.get(keys, 0) + 1)
    return res

#sorting dictionary keys alphabetically
def sortDic(Dic):
    sortedList , sortedDic = sorted(list(Dic.items())) , {}
    for i in range(len(sortedList)):
       sortedDic [sortedList[i][0]] = sortedList[i][1]
    Dic = sortedDic
    return Dic

#adding unexistant keys with values equal to zero
def addValuesToDic(Dic):
    queryKeys = sorted(list(freqCounter(readFileAsString("Q.txt")).keys()))
    for i in range(len(queryKeys)):
        if queryKeys[i] not in Dic:
            Dic[queryKeys[i]] = 0
    return sortDic(Dic)

#function to calculate the term frequency for the document
def tf_dict(s):
    import collections
    res = addValuesToDic(freqCounter(s))
    div = collections.Counter(s).most_common(1)[0][1]
    for i in res:
        res[i] /= div
    return res

#function to generate a dictionary that have the frequency of each term in the collecttion
def IDF_Dict():
    generalDic = {}
    for i in range(1,N+1):
        generalDic.update(freqCounter(readFileAsString("D" + str(i) + ".txt")))
        IDF_dic = {}
        for i in (generalDic.keys()):
            IDF_dic[i] = 0
            for j in range(1,N+1):
                if i in list(readFileAsString("D" + str(j) + ".txt")):
                    IDF_dic[i] = IDF_dic[i] + 1
    
    for i in readFileAsString("Q.txt"):
        if i in IDF_dic:
            IDF_dic[i] += 1
    return IDF_dic

def TF_IDF(fileName):
    import math
    tf = sortDic(tf_dict(readFileAsString(fileName)))
    idf = sortDic(IDF_Dict())
    tf_idf_dict = {}

    for i in tf:
        x = idf[serachnKeyObject(idf , i)] # number of times the term i appeared in the documents
        a1 = float(N+1) / float(x)
        tf_idf_dict[i] = tf[i] * math.log(a1 , 2)

    return addValuesToDic(tf_idf_dict)


#function to calculate the similarity between two documents
def sim(file1 , file2):
    TF_IDF_File1 = TF_IDF(file1)
    TF_IDF_File2 = TF_IDF(file2)
    res = 0

    for i in TF_IDF_File1:
        for j in TF_IDF_File2:
            if i == j:
                res += TF_IDF_File1[i] * TF_IDF_File2[j]
                break
    return res

def cosSim(file1, file2):
    import math
    TF_IDF_File1 = TF_IDF(file1)
    TF_IDF_File2 = TF_IDF(file2)
    file1_W , file2_W = 0 , 0
    
    for i in TF_IDF_File1:
        file1_W += math.pow(TF_IDF_File1[i] , 2)
    for i in TF_IDF_File2:
        file2_W += math.pow(TF_IDF_File2[i] , 2)

    div = math.sqrt(file1_W * file2_W)

    return sim(file1,file2) / div

#function to sort documents according to similarity
def sortDocuments():
    similarityDic = {"D1" : cosSim("D1.txt" , "Q.txt")}
    for i in range(N-1):
        similarityDic ["D" + str(i+2)] = cosSim("D" + str(i+2) + ".txt" , "Q.txt")
    return sorted(list(similarityDic.items()), key=lambda x: x[1], reverse=True)
    
def showRes():
    res = "Search results Are:- \n\n"
    for i in range(len(sortDocuments())):
        res += str(sortDocuments()[i][0]) + ": " + str(round(sortDocuments()[i][1]*100,4)) + "%" + "\n"
    return res


# print(showRes())
import bz2
import math
import os
import pickle
import regex as re
import requests
import sys
import time
from zipfile import ZipFile

regex = '\p{L}+' 

def tokenize(text):
    matchList = re.findall(regex, text)
    posList = []
    for word in matchList:
        posList.append(re.search(word, text))
    return posList

def text_to_idx(words):
    idxDict = {}
    for word in words:
        if word.group() in idxDict:
            idxDict[word.group()].append(word.start()) 
        else:
            idxDict[word.group()] = [word.start()]

    return idxDict

with open('Selma/marbacka.txt', 'r') as f:
    data = f.read().lower().strip()
marbackaToken = tokenize(data)
idx = text_to_idx(marbackaToken)

pickle.dump( idx, open( "idxfile.txt", "wb" ) )

idx = pickle.load( open( "idxfile.txt", "rb" ) )

def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files
get_files("Selma", ".txt")

master_index = {}
for file in get_files("Selma", ".txt"):
    f = open('Selma/' + file, 'r')
    data = f.read().lower().strip()
    tokenized = tokenize(data)
    idxL = text_to_idx(tokenized)
    for word in idxL:
        master_index.setdefault(word, {})[file] = idxL[word]

pickle.dump( master_index, open( "master_idxfile.txt", "wb" ) )
master_index = pickle.load( open( "master_idxfile.txt", "rb" ) )

# Write your code here
def concordance(word, master_index, window):
    concordList = ''
    for filename, indList in master_index[word].items():
        concordList += filename + '\n'
        f = open('Selma/' + filename, 'r')
        data = f.read().lower().replace('\n', ' ')
        for wordIndex in indList:
            concordList += (data[wordIndex-window:wordIndex+window]) + '\n'
    print(concordList)


# Write your code here
tfidf = {}
sizeOfFiles = len(get_files("Selma", ".txt"))

for filename in get_files("Selma", ".txt"):
    f = open('Selma/' + filename, 'r')
    data = f.read().lower()
    regex = '\p{L}+'
    sizeOfWords = len(re.findall(regex, data))
    
    for word, occurances in master_index.items():
        occurancesSize = 0
        if occurances.get(filename) != None:
            occurancesSize = len(occurances.get(filename))
        tf = occurancesSize / sizeOfWords
        idf = math.log10(sizeOfFiles /  len(master_index[word]))
        comb = tf * idf
        tfidf.setdefault(filename, {})[word] = comb


# Write your code here
def cosine_similarity(document1, document2):
    totalUpper = 0
    l1 = 0
    l2 = 0
    totalLower = 0
    for word in master_index:
        if document1 in master_index[word] or document2 in master_index[word]:
            t1 = 0
            t2 = 0
            if document1 in master_index[word]:
                t1 = len(master_index[word][document1])
                l1 += pow(len(master_index[word][document1]), 2)
            if document2 in master_index[word]:
                t2 = len(master_index[word][document2])
                l2 += pow(len(master_index[word][document2]), 2)
            totalUpper += t1 * t2
        totalLower = math.sqrt(l1) * math.sqrt(l2)
    print(totalUpper / totalLower)
    
cosine_similarity('troll.txt', 'nils.txt')

# Write your code here
maxval = 0
sim_matrix = ''
files = get_files('Selma', '.txt')
print(files)
for doc in files:
    sim_matrix += doc + '\t'
    for other in files:
        cs = cosine_similarity(doc, other)
        sim_matrix += str(format(cs, '.4f')) + ' '
    sim_matrix += '\n'
    
print(sim_matrix)
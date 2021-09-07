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
for filename in get_files("Selma", ".txt"):
    f = open('Selma/' + filename, 'r')
    data = f.read().lower().replace('\n', ' ')
    for word, occurances in master_index.items():
        # Regex to count words?
        tf = len(occurances) / len(master_index[word])
        idf = math.log10(len(get_files("Selma", ".txt")) / len(master_index[word]))
        comb = tf * idf
        tfidf.setdefault(word, {})[filename] = comb
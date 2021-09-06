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
concordList = []
def concordance(word, master_index, window):
    for file in get_files("Selma", ".txt"):
        f = open('Selma/' + file, 'r')
        data = f.read().lower().strip()
        for filename in master_index[word]:
            print(filename)
            #for wordIndex in indList:
                #print(wordIndex)
                #concordList.append(data[wordIndex-window:wordIndex+window])
    #return concordList
    
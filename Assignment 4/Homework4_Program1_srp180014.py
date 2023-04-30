# Homework 4
# Program 1
# Supraj Punnam
# CS 4395.001

import sys
import os
from random import randint
import pickle

import nltk
nltk.download('punkt')
import nltk.corpus
from nltk import *
from nltk.util import ngrams


def getNgrams(fileName):
    current_dir: str = os.getcwd()
    # Check to see if file name is valid
    try:
        current_dir: str = os.getcwd()
        dataFile = open(os.path.join(current_dir, fileName), encoding='utf-8')
    # Print error if file name is not valid
    except:
        print("The file name [" + fileName + "] is not valid")
        return ''

    # Tokenize the text.
    rawText = dataFile.read()
    textFile = rawText.replace('\n', '')
    tokens = Text(word_tokenize(textFile))

    # Create Unigram and Bigram lists for textFile.
    unigrams = word_tokenize(rawText)
    bigrams = list(ngrams(unigrams, 2))

    # Create a dictionary using bigrams and unigrams.
    unigram_dict = {x: unigrams.count(x) for x in set(unigrams)}
    bigram_dict = {y: bigrams.count(y) for y in set(bigrams)}

    return unigram_dict, bigram_dict


if __name__ == "__main__":
    # Prompt user for each training file name (3 times for each language).
    count = 0
    while count < 3:
        fileName = ''
        while True:
            if count == 0:
                fileName = input("Please enter English training file name: ")
            elif count == 1:
                fileName = input("Please enter French training file name: ")
            elif count == 2:
                fileName = input("Please enter Italian training file name: ")

            # Check to make sure file was processed properly.
            if getNgrams(fileName) != '':
                break

        # Pickle each training file's unigram and bigram dictionaries.
        unigram_dict, bigram_dict = getNgrams(fileName)
        if count == 0:
            pickle.dump(unigram_dict, open('english_unigram.p', 'wb'))
            pickle.dump(bigram_dict, open('english_bigram.p', 'wb'))
        if count == 1:
            pickle.dump(unigram_dict, open('french_unigram.p', 'wb'))
            pickle.dump(bigram_dict, open('french_bigram.p', 'wb'))
        if count == 2:
            pickle.dump(unigram_dict, open('italian_unigram.p', 'wb'))
            pickle.dump(bigram_dict, open('italian_bigram.p', 'wb'))

        # Increment counter and prompt user for next training file.
        count += 1

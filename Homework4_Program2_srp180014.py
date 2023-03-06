# Homework 4
# Program 2
# Supraj Punnam
# CS 4395.001

import sys
import os
from random import randint
import pickle

import nltk.corpus
from nltk import *
from nltk.util import ngrams

# Main method
if __name__ == '__main__':

    # Unpickle English Ngrams.
    english_unigrams = pickle.load(open('english_unigram.p', 'rb'))
    english_bigrams = pickle.load(open('english_bigram.p', 'rb'))

    # Unpickle French Ngrams.
    french_unigrams = pickle.load(open('french_unigram.p', 'rb'))
    french_bigrams = pickle.load(open('french_bigram.p', 'rb'))

    # Unpickle Italian Ngrams.
    italian_unigrams = pickle.load(open('italian_unigram.p', 'rb'))
    italian_bigrams = pickle.load(open('italian_bigram.p', 'rb'))

    # Calculate probability of each language:

    # Read in Test file.
    current_dir: str = os.getcwd()
    dataFile_test = open(os.path.join(current_dir, 'LangId.test'), encoding='utf-8')
    rawText_test = dataFile_test.read()

    # Read in Solution file.
    dataFile_sol = open(os.path.join(current_dir, 'LangId.sol'), encoding='utf-8')
    rawText_sol = dataFile_sol.read()
    solLines = rawText_sol.splitlines()

    # Get total Vocabulary size
    v = len(english_unigrams) + len(french_unigrams) + len(italian_unigrams)

    # Count correct test cases
    correctCases = 0

    # List to store incorrectly assigned lines.
    wrongLines = []

    count = 1
    # Iterate through test file and get probabilities.
    for line in rawText_test.splitlines():

        # Separate each line into unigrams and bigrams.
        test_unigrams = word_tokenize(line)
        test_bigrams = list(ngrams(test_unigrams, 2))

        # Values to hold final probability of each language.
        english_prob = 1.0
        french_prob = 1.0
        italian_prob = 1.0

        # Find probability of each language:
        for testBigram in test_bigrams:
            # Probability of language being English.
            b_1 = english_bigrams[testBigram] if testBigram in english_bigrams else 0
            u_1 = english_unigrams[testBigram[0]] if testBigram[0] in english_unigrams else 0
            english_prob = english_prob * ((b_1 + 1) / (u_1 + v))

            # Probability of language being French.
            b_2 = french_bigrams[testBigram] if testBigram in french_bigrams else 0
            u_2 = french_unigrams[testBigram[0]] if testBigram[0] in french_unigrams else 0
            french_prob = french_prob * ((b_2 + 1) / (u_2 + v))

            # Probability of language being Italian.
            b_3 = italian_bigrams[testBigram] if testBigram in italian_bigrams else 0
            u_3 = italian_unigrams[testBigram[0]] if testBigram[0] in italian_unigrams else 0
            italian_prob = italian_prob * ((b_3 + 1) / (u_3 + v))

        # If language is most likely English:
        if english_prob >= french_prob and english_prob >= italian_prob:
            # If case is correct:
            if solLines[count - 1] == str(count) + " English":
                print(str(count) + " English")
                correctCases += 1
            # Case is not correct
            else:
                print(str(count) + " English     Correct: " + solLines[count - 1])
                wrongLines.append(count)

        # If language is most likely French:
        elif french_prob >= english_prob and french_prob >= italian_prob:
            # If case is correct:
            if solLines[count - 1] == str(count) + " French":
                print(str(count) + " French")
                correctCases += 1
            # Case is not correct
            else:
                print(str(count) + " French     Correct: " + solLines[count - 1])
                wrongLines.append(count)

        # If language is most likely Italian:
        else:
            # If case is correct:
            if solLines[count - 1] == str(count) + " Italian":
                print(str(count) + " Italian")
                correctCases += 1
            # Case is not correct
            else:
                print(str(count) + " Italian     Sol: " + solLines[count - 1])
                wrongLines.append(count)

        count += 1

    # Print total number of correct cases.
    print("\nTotal Correct Cases: " + str(correctCases) + " / 300 = " + str(
        round(((correctCases / count) * 100), 3)) + "%\n")

    # Print lines where language was guessed incorrectly.
    print("Incorrectly classified items: " + str(wrongLines) + "\n")

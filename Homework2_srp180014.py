# Homework 2
# Supraj Punnam
# CS 4395.001


import sys
import os
from random import randint

from nltk import pos_tag
from nltk.book import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.text import Text


def preProcessText(raw_text):

    # Tokenize raw text.
    textFile = Text(word_tokenize(raw_text.lower()))
    tokenList = textFile.tokens

    # Reduce tokens to alpha, non-stop words, and words longer than 5 characters.
    tempList = []
    stopWords = set(stopwords.words('english'))
    tempList = [token for token in tokenList if token.isalpha() and token not in stopWords and len(token) > 5]
    wordList = tempList

    # Lemmatize tokens, then keep only unique lemmas.
    lemmatizer = WordNetLemmatizer()
    tempList = [lemmatizer.lemmatize(token) for token in wordList]
    lemmaList = set(tempList)

    # Get Part of Speech (POS) of each lemma.
    posList = pos_tag(lemmaList)
    # Print first 20 lemmas with POS.
    print("First 20 lemmas with POS:\n\n" + str(posList[:20]) + "\n")

    # Create list of lemmas that are nouns.
    nounList = [lemma[0] for lemma in posList if lemma[1] == 'NN']

    # Compare number of tokens with number of nouns.
    print("Number of tokens: " + str(len(wordList)) + "\n")
    print("Number of nouns: " + str(len(nounList)) + "\n")

    return wordList, nounList

def guessingGame(nounList):

    playerScore = 5
    wordsFinished = 0
    playerGuess = ''
    correctWord = ''
    lettersGuessed = ''
    wordCompleted = True

    # Prompt user to play word guessing game.
    print("\n[ Let's play a word guessing game! ]\n")

    # Choose a word at random from the 50 most common words.
    correctWord = nounList[randint(0,49)]

    # Start word guessing game.
    while True:

        # Print current guessing progress
        wordCompleted = True
        for letter in correctWord:
            if letter in lettersGuessed:
                print(letter, end=' ')
            else:
                print('_', end=' ')
                wordCompleted = False

        # Check if player has finished guessing word correctly.
        if wordCompleted is True:
            print("\nYou solved it!\n")
            print("[ Current Score: " + str(playerScore) + ' ]\n')
            wordsFinished+=1

            # Start a new game and change the random word to a different word.
            tempWord = nounList[randint(0,49)]
            while tempWord == correctWord:
                tempWord = nounList[randint(0,49)]
            correctWord = tempWord
            lettersGuessed = ''

        # If user has not completed word yet:
        else:
            # Let user guess a letter in the word
            playerGuess = input("\nGuess a letter: ")

            # Check for correct formatting.
            while len(playerGuess) != 1 or playerGuess in lettersGuessed:
                if len(playerGuess) != 1:
                    playerGuess = input("You did not enter a letter. Please enter a letter: ")
                else:
                    playerGuess = input("You already used that letter. Guess a different letter: ")

            lettersGuessed += playerGuess   # Add letter to string of letters already inputted by user.

            # If user inputs '!', stop guessing game.
            if playerGuess == '!':
                break

            # Check to see if user's guess is in the word.
            if playerGuess in correctWord:
                playerScore += 1
                print("Correct! Your score is now " + str(playerScore) + "\n")
            else:
                # Decrement user's score if guess is not correct.
                playerScore -= 1
                if playerScore > -1:
                    print("Sorry, guess again. Your score is now " + str(playerScore) + "\n")

                # Exit the game if the score falls below 0.
                if playerScore < 0:
                    print("\n[ Game over! Better luck next time ]")
                    print("[ The word was: " + correctWord + " ]")
                    print("[ Total words completed: " + str(wordsFinished) + " ]\n")
                    break


if __name__ == '__main__':
    # User must input a system argument.
    if len(sys.argv) < 2:
        # Print error if no sysarg is given.
        print('\nERROR: No sysarg detected.\nPlease enter a filename as a sysarg.')

    else:
        # Open file and read in as raw text.
        fileName = sys.argv[1]
        current_dir: str = os.getcwd()
        dataFile = open(os.path.join(current_dir, fileName), 'r')
        raw_text = dataFile.read()

        # Tokenize raw text.
        textFile = Text(word_tokenize(raw_text))

        # Calculate lexical diversity.
        text_list = textFile.tokens  # Put tokens into list
        text_set = set(text_list)  # Create set of items in list (remove duplicates)
        listCount = len(text_list)  # Total number of tokens
        setCount = len(text_set)  # Total number of UNIQUE tokens

        lexicalDiversity = setCount / listCount

        # Print lexical diversity.
        print("\nLexical diversity of the text: " + str(round(lexicalDiversity, 2)) + "\n")

        # Preprocess text.
        tokens, nouns = preProcessText(raw_text)

        # Create dict to hold nouns and counts and sort the dict into a list.
        nounCounts = {noun: tokens.count(noun) for noun in nouns}
        nounCountDict = {}
        nounCountDict = sorted(nounCounts.items(), key=lambda kv: kv[1])
        nounCountDict.reverse()

        # Print the 50 most common words.
        print("50 most common words in the text, and their count: \n")
        print(nounCountDict[:50])

        # Save the 50 most common words into a list.
        x=0
        nounList = []
        for key, value in nounCountDict:
            if x < 50:
                nounList.append(key)
            x += 1

        # Start the word guessing game.
        guessingGame(nounList)






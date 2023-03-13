# Homework 6
# Supraj Punnam
# CS 4395.001

import copy
import urllib
from urllib import request
from bs4 import BeautifulSoup
import requests
from collections import deque
from urllib.request import urlopen
import re
import nltk
from nltk import *
from nltk.corpus import stopwords
import string
import pickle

def webCrawler(ogLink):
    # Store links in lists for later use
    relevantLinks = []  # Store the most relevant links
    extraLinks = []  # Store links that may not be relevant

    # Queue to store links to crawl
    linkQueue = deque([])

    # Crawl through links to find 15 relevant ones
    linksFound = 0
    linksCrawled = 0
    outsideLinkFound = False
    tempLink = ogLink
    count = 1
    currentLink = ogLink
    print("")
    while True:
        # Loop through links found in original link.
        print(str(linksCrawled+1) + " Crawling through: " + str(currentLink))

        # Create Soup object to iterate over all text in currentLink
        r = requests.get(currentLink)
        linkData = r.text
        soup = BeautifulSoup(linkData, "html.parser")

        # Get original link's domain name.
        parsedUrl = urllib.request.urlparse(currentLink)
        domainName = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUrl)

        # Iterate through all links on page from mainLink
        for link in soup.find_all('a'):
            link_string = str(link.get('href'))

            # Get links related to topic; i.e, NFL
            if 'NFL' in link_string or 'nfl' in link_string:

                # Format link string for easier processing
                tempLink = link_string

                # Get rid of prepended query string label.
                if tempLink.startswith('/url?q='):
                    tempLink = tempLink[7:]

                # Get only part of link before any '&' appear.
                if '&' in tempLink:
                    i = tempLink.find('&')
                    tempLink = tempLink[:i]

                # Add URLs that are not links to other parts of the page, are not Google searches to allLinks, and are not already in the list of links.
                if tempLink.startswith('http') and 'google' not in tempLink and tempLink not in relevantLinks:

                    # If the link is not in the domain of the original link, prepend to linkQueue.
                    if domainName not in tempLink:
                        linkQueue.appendleft(tempLink)
                        relevantLinks.append(tempLink)
                        linksFound += 1
                        # print("     " + str(linksFound) + " " + tempLink)
                        if linksFound >= 14:
                            break
                    else:
                        extraLinks.append(tempLink)

        # If outside links found is below 15, append other links.
        if linksFound < 15:
            for tempLink in extraLinks:
                if tempLink not in relevantLinks:
                    linkQueue.append(tempLink)
                    relevantLinks.append(tempLink)
                    # print("     " + str(linksFound) + " " + tempLink)
                    linksFound += 1
                    if linksFound >= 14:
                        break
        # If 15 relevant links found, either crawl through next site or stop loop.
        if linksCrawled >= 14:
            break
        else:
            #print("")
            linksCrawled += 1
            linksFound = 0
            currentLink = linkQueue.popleft()  # Pop and crawl through first item in list

    return relevantLinks

def scrapeText(urlList):

    # Scrape Text
    count = 0
    for url in urlList:
        # Attempt to scrape text from URLs.
        try:
            html = request.urlopen(url).read().decode('utf8')
        # If request to open fails, move to next URL.
        except:
            print("\t [ERROR] Failed to open: " + str(url))
            continue
        # Write contents of the URL's HTML file to a Text file.
        else:
            print(str(count + 1) + " Writing to file: " + str(url))
            soup = BeautifulSoup(html, "html.parser")

            # Remove all tags from HTML code.
            for script in soup(["script", "style"]):
                script.extract()

            # Extract text from soup.
            text = soup.get_text()

            # Write text to file
            fileName = "urlText_" + str(count+1) + ".txt"
            file = open(fileName, "w", encoding="utf-8")
            file.write(str(text))
            file.close()
            if count >= 14:
                break
            else:
                count += 1

def cleanUpText(fileName):
    try:
        with open(fileName, "r", encoding="utf-8") as file:
            fileContents = file.read()
    except:
        print("[ERROR] Failed to open file.")
    else:
        # Remove newlines and tabs, and remove duplicate spaces.
        fileContents = re.sub(r"[\n\t]*", "", fileContents)
        fileContents = re.sub(r"\s+", " ", fileContents)

        # Tokenize text
        fileSentences = sent_tokenize(fileContents)

        # Write sentences to new file.
        ext = fileName.find('.txt')
        newFileName = fileName[:ext] + "_clean.txt"
        newFile = open(newFileName, 'w').close()    # Erase contents of file before appending
        newFile = open(newFileName, "a", encoding="utf-8")
        for sent in fileSentences:
            newFile.write(sent)
            newFile.write("\n")
        newFile.close()

def getTermFrequency(fileName, freqDict):
    # Open file for reading.
    with open(fileName, "r", encoding="utf-8") as file:
        fileContents = file.read()

    # Lowercase all text, remove stopwords, remove punctuation, and tokenize words in file.
    fileContents = fileContents.lower()
    fileContents = re.sub(r'[^\w\s]', '', fileContents)
    wordList = word_tokenize(fileContents)
    stopWords = set(stopwords.words('english'))
    filteredText = [word for word in wordList if word not in stopWords]

    # Get term frequency of all words found in the documents
    for word in set(filteredText):
        # Add word and its frequency to dictionary if absent.
        if word not in freqDict:
            freqDict[word] = (filteredText.count(word)+1) / len(filteredText)
        # Else, simply get word (key) and multiply the frequency (value).
        else:
            freqDict[word] = freqDict[word] + ((filteredText.count(word)+1) / len(filteredText))
    return freqDict
def getTopTerms(freqDict, numTerms):
    # topTerms stores the top terms
    topTerms = []

    print("[ Top " + str(numTerms) + " Terms: ]")

    tempDict = copy.deepcopy(freqDict)
    count = 0
    while count < numTerms:
        topTerms.append(max(tempDict, key=tempDict.get))
        tempDict.pop(topTerms[count])
        print(str(count+1) + " " + topTerms[count])
        count += 1
    print("")
    return topTerms


if __name__ == '__main__':

    # Crawl through and save URLs related to "Evangelion"
    urlList = webCrawler("https://en.wikipedia.org/wiki/National_Football_League")
    print("")

    # Scrape text from URLs and save to file.
    scrapeText(urlList)

    # Clean up text from Text files.
    print("")
    count = 0
    while count < 15:
        fileName = "urlText_" + str(count + 1) + ".txt"
        cleanUpText(fileName)
        count += 1

    # Get term frequencies for all documents.
    termFreq = {}
    count = 0
    while count < 15:
        fileName = "urlText_" + str(count + 1) + "_clean.txt"
        termFreq = getTermFrequency(fileName, termFreq)
        count += 1

    # Get top 25 terms and print them
    topTerms = getTopTerms(termFreq, 25)

    # Build a searchable knowledge base from top 10 words and all sentences containing said word.
    count = 0
    knowledgeBase = {}
    while count < 10:
        term = topTerms[count]
        relevantSentences = []
        i = 0
        while i < 15:
            fileName = "urlText_" + str(count + 1) + "_clean.txt"
            with open(fileName, "r", encoding="utf-8") as file:
                fileContents = file.readlines()
                for line in fileContents:
                    if term in word_tokenize(line.lower()):
                        relevantSentences.append(line)
            i += 1
        knowledgeBase[term] = relevantSentences
        count += 1

    # Pickle the knowledge base.
    pickle.dump(knowledgeBase, open('knowledgeBase.p', 'wb'))

    # Unpickle the knowledge base, and print it out.
    knowledgeBase_in = pickle.load(open('knowledgeBase.p', 'rb'))
    for key, value in knowledgeBase_in.items():
        print(key + ": " + str(value) + '\n')


    print('Done.')

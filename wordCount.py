import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists
from collections import defaultdict, OrderedDict

inputFile = sys.argv[1]
outputFile = sys.argv[2]

wordDict = defaultdict(int)

# attempt to open input file
with open(inputFile, 'r') as file:
    for line in file:
        # split line on whitespace and punctuation
        wordList = re.split('[ \t]|[\W+]', line)
        for word in wordList:
            if len(word) < 2 and not word == 'I' and not word == 'a':
                continue
            word = word.lower()
            wordDict[word] = wordDict[word] + 1

# Sort the dictionary by key values
wordDict = OrderedDict(sorted(wordDict.items()))
with open(outputFile, 'w+') as output:
    for word in wordDict:
        output.write(word + ' ' + str(wordDict[word]) + '\n')


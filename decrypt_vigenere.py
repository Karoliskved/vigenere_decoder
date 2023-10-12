import math
import numpy as np

f = open("kodas.txt", "r", encoding="utf-8")
text = f.read()
newText = ""

with open("abc_frequencies.txt", "r") as file:
    abcFreq = file.read().split()
    abcFreq = [float(num) for num in abcFreq]
abcFreq = [i/100 for i in abcFreq]

abc = "aąbcčdeęėfghiįyjklmnoprsštuųūvzž"

def removePunctuationAndSpaces(text):
    text = text.replace(',', '')
    text = text.replace(':', '')
    text = text.replace(';', '')
    text = text.replace('.', '')
    text = text.replace(' ', '')
    text = text.lower()
    return text

def codeToText(code):
    text = ''
    for el in range(0, len(code)):
        for a in range(0, len(abc)):
            if(code[el] == a):
                text += abc[a]
                continue
    return(text)


def decrypt(text, key_code, key_length):
    initialTextCode = [] # numbers

    for i in range(0, len(text)):
        for j in range(0, len(abc)):
            if(text[i].lower() == abc[j]):
                initialTextCode.append(j)
                continue

    newTextCode = []
    for i in range(0, len(text), key_length):
        text_fragment_size = key_length if math.floor((len(text)-i)/key_length) > 0 else len(text)%key_length
        for j in range(0, text_fragment_size):
            newTextCode.append((initialTextCode[i+j]-key_code[j])%len(abc))

    newText = ''
    for el in newTextCode:
        newText += abc[el]

    key = codeToText(key_code)
    print("Possible key:", key)
    print("Decrypted text:", newText)


def splitTextIntoPairs(text):
    pairs = []
    for i in range(0, len(text)-1):
        pairs.append(text[i] + text[i+1])
    return pairs

def checkForDigrams(pairs):
    digrams = []
    indices = []
    minKeyLength = 2
    maxKeyLength = 10
    
    for i in range(0, len(pairs)-1):
        for j in range(i+1, len(pairs)):
            if(pairs[i] == pairs[j]):
                digrams.append(pairs[j])
                indices.append(j-i)

    divisorCount = [0] * (maxKeyLength-1)
    for i in range(0, len(indices)-1):
        for j in range(minKeyLength, maxKeyLength+1):
            if(indices[i]%j == 0):
                divisorCount[j-minKeyLength] += 1
    
    topKeyIndices = np.argsort(np.array(divisorCount))
    topKeyIndices = np.flip(topKeyIndices)[:3]
    topKeys = topKeyIndices + minKeyLength
    return list(topKeys)

def splitIntoLength(text, length):
    splitArray = []
    for i in range(0, len(text), length):
        item = ''
        itemSize = length if math.floor((len(text)-i)/length) > 0 else len(text)%length
        for j in range(0, itemSize):
            item += text[i+j]
        splitArray.append(item)
    return(splitArray)

def shiftArray(array):
    newArray = []
    for i in range(0, len(array)):
        newArray.append(array[(i+1)%len(array)])
    return newArray

def countLetterPossibility(array):

    allSteps = []

    for i in range(0, len(array[0])):
        letterCount = [0] * len(abc)
        for j in range(0, len(array)-1):
            for k in range(0, len(abc)):
                if(array[j][i] == abc[k]):
                    letterCount[k] +=1
                    continue

        allLetterCount = sum(letterCount)
        letterPercentages = [i/allLetterCount for i in letterCount]
        
        maxStep = 0
        maxNum = 0
        for i in range(0, len(abc)):
            res = 0
            for j in range(0, len(abc)):
                res += letterPercentages[j] * abcFreq[j]
            if(res > maxNum):
                maxNum = res
                maxStep = i
            letterPercentages = shiftArray(letterPercentages)
        allSteps.append(maxStep)

    return(allSteps)

text = removePunctuationAndSpaces(text)
letter_pairs = splitTextIntoPairs(text)
key_lengths = checkForDigrams(letter_pairs)

for i in range(0, len(key_lengths)):
    print(f"\nKey length: {key_lengths[i]}")
    split_text = splitIntoLength(text, key_lengths[i])
    possible_key = countLetterPossibility(split_text)
    decrypt(text, possible_key, key_lengths[i])
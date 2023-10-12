import math
import numpy as np

f = open("kodas2.txt", "r", encoding="utf-8")
text = f.read()

with open("abc_frequencies.txt", "r") as file:
    abc_freq = file.read().split()
    abc_freq = [float(num) for num in abc_freq]
abc_freq = [i/100 for i in abc_freq]

abc = "aąbcčdeęėfghiįyjklmnoprsštuųūvzž"

def remove_punctuation_and_spaces(text):
    text = text.replace(',', '')
    text = text.replace(':', '')
    text = text.replace(';', '')
    text = text.replace('.', '')
    text = text.replace(' ', '')
    text = text.replace('-', '')
    text = text.lower()
    return text

def code_to_text(code):
    text = ''
    for el in range(0, len(code)):
        for a in range(0, len(abc)):
            if(code[el] == a):
                text += abc[a]
                continue
    return(text)

def decrypt(text, key_code, key_length):
    encrypted_text_code = [] # encrypted text converted to numbers

    for i in range(0, len(text)):
        for j in range(0, len(abc)):
            if(text[i].lower() == abc[j]):
                encrypted_text_code.append(j)
                continue

    decrypted_text_code = [] # decrypted text in numbers
    for i in range(0, len(text), key_length):
        text_fragment_size = key_length if math.floor((len(text)-i)/key_length) > 0 else len(text)%key_length
        for j in range(0, text_fragment_size):
            decrypted_text_code.append((encrypted_text_code[i+j]-key_code[j])%len(abc))

    decrypted_text = '' # decrypted text string
    for el in decrypted_text_code:
        decrypted_text += abc[el]

    key = code_to_text(key_code)
    print("Possible key:", key)
    print("Decrypted text:", decrypted_text)

def split_text_into_pairs(text):
    pairs = []
    for i in range(0, len(text)-1):
        pairs.append(text[i] + text[i+1])
    return pairs

def check_for_digrams(pairs):
    digrams, spaces_between_digrams = [], []
    min_key_length = 2
    max_key_length = 10
    
    for i in range(0, len(pairs)-1):
        for j in range(i+1, len(pairs)):
            if(pairs[i] == pairs[j]):
                digrams.append(pairs[j])
                spaces_between_digrams.append(j-i)

    divisor_count = [0] * (max_key_length-1)
    for i in range(0, len(spaces_between_digrams)-1):
        for j in range(min_key_length, max_key_length+1):
            if(spaces_between_digrams[i]%j == 0):
                divisor_count[j-min_key_length] += 1
    
    top_key_indices = np.argsort(np.array(divisor_count))
    top_key_indices = np.flip(top_key_indices)[:3]
    top_keys = top_key_indices + min_key_length
    return list(top_keys)

def split_text_by_key_length(text, key_length):
    split_array = []
    for i in range(0, len(text), key_length):
        item = ''
        item_size = key_length if math.floor((len(text)-i)/key_length) > 0 else len(text)%key_length
        for j in range(0, item_size):
            item += text[i+j]
        split_array.append(item)
    return(split_array)

def shift_array(array):
    newArray = []
    for i in range(0, len(array)):
        newArray.append(array[(i+1)%len(array)])
    return newArray

def find_key_elements(array):

    key_elements = []

    for i in range(0, len(array[0])):
        letter_count = [0] * len(abc)
        for j in range(0, len(array)-1):
            for k in range(0, len(abc)):
                if(array[j][i] == abc[k]):
                    letter_count[k] +=1
                    continue

        all_letter_count = sum(letter_count)
        letter_percentages = [i/all_letter_count for i in letter_count]
        
        max_step = 0
        max_num = 0
        for i in range(0, len(abc)):
            res = 0
            for j in range(0, len(abc)):
                res += letter_percentages[j] * abc_freq[j]
            if(res > max_num):
                max_num = res
                max_step = i
            letter_percentages = shift_array(letter_percentages)
        key_elements.append(max_step)

    return(key_elements)

text = remove_punctuation_and_spaces(text)
letter_pairs = split_text_into_pairs(text)
key_lengths = check_for_digrams(letter_pairs)

for i in range(0, len(key_lengths)):
    print(f"\nKey length: {key_lengths[i]}")
    split_text = split_text_by_key_length(text, key_lengths[i])
    possible_key = find_key_elements(split_text)
    decrypt(text, possible_key, key_lengths[i])
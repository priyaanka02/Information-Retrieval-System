# porter_stemmer.py
# Implements Porter's stemming algorithm based on the 1980 paper

import re

def consonant(word, i):
    c = word[i]
    if c in "aeiou":
        return False
    if c == 'y':
        return i == 0 or not consonant(word, i - 1)
    return True

def measure(word):
    m = 0
    i = 0
    length = len(word)
    while i < length:
        if not consonant(word, i):
            break
        i += 1
    while i < length:
        while i < length and not consonant(word, i):
            i += 1
        while i < length and consonant(word, i):
            i += 1
        m += 1
    return m

def contains_vowel(word):
    return any(not consonant(word, i) for i in range(len(word)))

def ends_double_consonant(word):
    return len(word) >= 2 and word[-1] == word[-2] and consonant(word, len(word) - 1)

def cvc(word):
    if len(word) < 3:
        return False
    if not consonant(word, -1) or consonant(word, -2) or not consonant(word, -3):
        return False
    return word[-1] not in 'wxy'

def step1a(word):
    if word.endswith('sses'):
        return word[:-2]
    if word.endswith('ies'):
        return word[:-2]
    if word.endswith('ss'):
        return word
    if word.endswith('s'):
        return word[:-1]
    return word

def step1b(word):
    base = None
    if word.endswith('eed'):
        base = word[:-3]
        if measure(base) > 0:
            return base + 'ee'
        else:
            return word
    elif word.endswith('ed'):
        base = word[:-2]
        if contains_vowel(base):
            word = base
        else:
            return word
    elif word.endswith('ing'):
        base = word[:-3]
        if contains_vowel(base):
            word = base
        else:
            return word
    else:
        return word

    if word.endswith(('at', 'bl', 'iz')):
        return word + 'e'
    elif ends_double_consonant(word) and word[-1] not in 'lsz':
        return word[:-1]
    elif measure(word) == 1 and cvc(word):
        return word + 'e'
    return word

def step1c(word):
    if word.endswith('y') and contains_vowel(word[:-1]):
        return word[:-1] + 'i'
    return word

def step2(word):
    suffixes = {
        'ational': 'ate', 'tional': 'tion', 'enci': 'ence', 'anci': 'ance',
        'izer': 'ize', 'abli': 'able', 'alli': 'al', 'entli': 'ent',
        'eli': 'e', 'ousli': 'ous', 'ization': 'ize', 'ation': 'ate',
        'ator': 'ate', 'alism': 'al', 'iveness': 'ive', 'fulness': 'ful',
        'ousness': 'ous', 'aliti': 'al', 'iviti': 'ive', 'biliti': 'ble'
    }
    for key in suffixes:
        if word.endswith(key):
            base = word[:-len(key)]
            if measure(base) > 0:
                return base + suffixes[key]
            return word
    return word

def step3(word):
    suffixes = {
        'icate': 'ic', 'ative': '', 'alize': 'al', 'iciti': 'ic',
        'ical': 'ic', 'ful': '', 'ness': ''
    }
    for key in suffixes:
        if word.endswith(key):
            base = word[:-len(key)]
            if measure(base) > 0:
                return base + suffixes[key]
            return word
    return word

def step4(word):
    suffixes = [
        'al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement',
        'ment', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize'
    ]
    for suffix in suffixes:
        if word.endswith(suffix):
            base = word[:-len(suffix)]
            if measure(base) > 1:
                if suffix == 'ion' and base[-1] not in 'st':
                    return word
                return base
            return word
    return word

def step5a(word):
    if word.endswith('e'):
        base = word[:-1]
        m = measure(base)
        if m > 1 or (m == 1 and not cvc(base)):
            return base
    return word

def step5b(word):
    if measure(word) > 1 and ends_double_consonant(word) and word.endswith('l'):
        return word[:-1]
    return word

def stem(word):
    word = word.lower()
    word = step1a(word)
    word = step1b(word)
    word = step1c(word)
    word = step2(word)
    word = step3(word)
    word = step4(word)
    word = step5a(word)
    word = step5b(word)
    return word

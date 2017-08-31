#! python3

import re
import random

class ParseLengthError(Exception):
    pass

def weighted_choice(choices, weights):

    total = 0
    cumulative_weights = []
    for num in weights:
        total += num
        cumulative_weights.append(total)

    rand = random.random() * total
    for choice, weight in zip(choices, cumulative_weights):
        if rand < weight:
            return choice

def parse_input(text, step):

    invalidRegex = re.compile(r'(@|\w+://)\S*')
    text = text.lower()
    results = [word.strip(r'&,[]()\/') for word in text.split() if not invalidRegex.match(word)]

    if len(results) < step:
        yield ParseLengthError('Length of text too small to parse'), ''
    
    for index in range(step, len(results)):
        yield tuple(results[index - step:index]), results[index]

def build_dict(words_dict, key, value):

    words_dict.setdefault(key, {})
    
    if value not in words_dict[key]:
        words_dict[key][value] = 1
    else:
        words_dict[key][value] += 1
    
def generate_sentence(words_dict, max_length=140): 

    result = ''
    start = random.choice(list(words_dict.keys()))
    sentence = start

    while (True):

        try:
            next_word = weighted_choice(words_dict[start].keys(), words_dict[start].values()),
        except KeyError:
            # Return the sentence as is.
            return result

        if len(next_word) + len(result) >= max_length:
            break

        sentence += next_word
        start = start[1:] + next_word
        result = ' '.join(sentence)

    return result
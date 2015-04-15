# This script will tokenize the file politician_text.txt and store it in politician_n-grams.txt

import nltk
import collections


with open("politician_text.txt", 'r') as f:
    tokens = nltk.word_tokenize(f.read())
    words = [word.lower() for word in tokens]
    word_count = collections.Counter(words)
    most_common = [word[0] for word in word_count.most_common(1000) if len(word[0]) > 2]
    
with open("politics_keywords.py", "w") as unigrams:
    unigrams.write(str(most_common))

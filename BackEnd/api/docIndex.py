# Import Necessary Packages
from BackEnd import *
import string
import numpy as np
import pandas as pd

from gensim.models import Doc2Vec
from collections import namedtuple
import gensim.utils
import re
# Set of useless words
wordList = set()
with open("./BackEnd/api/stoplist.txt", "r") as wordList_fh:
    for line in wordList_fh:
        wordList.add(line.strip('\n'))

# get all of the oil news text paired with the reference
items = get_oil_news_list()
data = list()
reference = list()
for obj in items:
    data.append(obj.content)
    reference.append(obj.reference)

# delete items variable from memory
del items

# create the np arrays
data = np.asarray(data)
reference = np.asarray(reference)

# prepare the data
SentimentDocument = namedtuple('SentimentDocument', 'words tags title original_number')
n = 0
alldocs = list()

regex = re.compile('[%s]' % re.escape(string.punctuation)) #to remove punctuation
for line_no, line in enumerate(data):
    line = regex.sub('', line)
    tokens = gensim.utils.to_unicode(line).lower().split()
    temp = tokens[0:]
    words = []
    for word in temp:
        if(word in wordList):
            continue;
        else:
            words.append(word)
    tags = [n]
    title = reference[line_no]
    alldocs.append(SentimentDocument(words, tags, title, line_no))
    n = n+1
# print for debug purposes
#doc = alldocs[0]
#print(doc, '\n')
#print(data[doc.original_number])


from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim import similarities

dct = Dictionary(doc.words for doc in alldocs)  # fit dictionary
corpus = [dct.doc2bow(line.words) for line in alldocs]  # convert dataset to BoW format
model_tfidf = TfidfModel(corpus)  # fit model

tokens = "turkey".split()
index = similarities.MatrixSimilarity([dct.doc2bow(tokens)],num_features=len(dct))

similarity=np.zeros((len(alldocs)))
maxsim = 0
for id, doc in enumerate(alldocs):
    similarity[id] = index[dct.doc2bow(doc.words)]

docsim= alldocs[np.argmax(similarity)]
print(data[docsim.original_number])
print(docsim.title)

'''
# Creating and training the Doc2Vec models
model = Doc2Vec(dm=1, size = 300, window = 10, hs = 0, min_count = 3, dbow_words = 1, sample = 1e-5)
# build the vocabulary
model.build_vocab(alldocs)

model.train(alldocs, total_examples=model.corpus_count, epochs=100, start_alpha=0.01, end_alpha=0.01)
model.save("smallModel")

# Evaluate Document Embedding
testToken = "coal"
new_vector = model.infer_vector(testToken.split(), alpha=0.001, steps = 5)
tagsim = model.docvecs.most_similar([new_vector])[0]
docsim = alldocs[tagsim[0] ]
print("Document : ", data[docsim.original_number], "\n")
print("Title : ", docsim.title)
print("Distance : ", tagsim[1])
'''

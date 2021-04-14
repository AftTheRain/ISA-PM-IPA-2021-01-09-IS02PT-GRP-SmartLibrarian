# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 08:01:47 2021

@author: nirav
"""

#basic imports
import numpy as np

#pre-processing imports
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

#imports related to word2vec modeling
from gensim.models import KeyedVectors
from scipy import spatial

# BERT Extractive Summarizer
from summarizer import Summarizer


class IntelligentBookAnalytics:
    #Load W2V model.  
    w2v_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    print(f'done loading Word2Vec: {len(w2v_model.vocab.keys())}')
    
    # Load Bert model.      
    BERT_model = Summarizer()
    print ('done loading BERT model')

    def __init__(self):
        self.vector_model = IntelligentBookAnalytics.w2v_model
        self.summarizer_model = IntelligentBookAnalytics.BERT_model
    
    def get_summary(self, full_text: str, max_length = 100) -> str:
        summary = self.summarizer_model(full_text, min_length=10, max_length=max_length)
        return ''.join(summary)
        
    
    def find_matchingtitle(self, org_title: str, alt_titles: list) -> str:        
        
        text = [org_title] + alt_titles
        
        #preprocess the text.
        def preprocess_text(text, mystopwords):    
            def remove_stopswords(sentence):
                #remove stop words, digits & punctuations
                return [word.lower() for word in sentence if word not in mystopwords and not word.isdigit()
                       and word not in punctuation]
            #loop thru all sentences in text
            return [remove_stopswords(word_tokenize(sentence.lower())) for sentence in text]
        
        mystopwords = set(stopwords.words("english"))
        text_processed = preprocess_text(text, mystopwords)
        
        # Creating sentence vectors from text
        def generate_vectors(text):
            vectors = []
            for sentence in text:
                sent_vec =  np.zeros(300)
                word_count = 0
                for word in sentence:
                    if word in self.vector_model:
                        word_vec = self.vector_model[word]
                        sent_vec += word_vec
                        word_count +=1
                vectors.append(sent_vec/word_count)        
            return vectors
        
        sent_vectors = generate_vectors(text_processed)
        
        # calculate sentence distances
        title_vector = sent_vectors[0]
        alt_vectors = sent_vectors[1:]
        distances = [spatial.distance.cosine(v,title_vector) for v in alt_vectors]

        closest_match = alt_titles[np.argmin(distances)]
        return closest_match
      
      
        
#### test #######        
        
titles = [
    "Sapiens: A Brief History of Humankind",
    "Sapiens: A Brief History of Man",
    "Homo Deus: A Brief History of Man"
]

myObj = IntelligentBookAnalytics()
matching_title = myObj.find_matchingtitle(titles[0], titles[1:])
print(f'\nMatching Title: {matching_title}')

full_text = \
"One hundred thousand years ago, at least six human species inhabited the earth.\
Today there is just one. Us. Homo sapiens. How did our species succeed in the \
battle for dominance? Why did our foraging ancestors come together to create \
cities and kingdoms? How did we come to believe in gods, nations, and human \
rights; to trust money, books, and laws; and to be enslaved by bureaucracy, \
timetables, and consumerism? And what will our world be like in the millennia \
to come? In Sapiens, Professor Yuval Noah Harari spans the whole of human history, \
from the very first humans to walk the earth to the radical—and sometimes \
devastating—breakthroughs of the Cognitive, Agricultural, and Scientific \
Revolutions. Drawing on insights from biology, anthropology, paleontology, and \
economics, and incorporating full-color illustrations throughout the text, he \
explores how the currents of history have shaped our human societies, the \
animals and plants around us, and even our personalities. Have we become happier \
as history has unfolded? Can we ever free our behavior from the legacy of our \
ancestors? And what, if anything, can we do to influence the course of the \
centuries to come? Bold, wide-ranging, and provocative, Sapiens integrates \
history and science to challenge everything we thought we knew about being \
human: our thoughts, our actions, our heritage...and our future."

summary = myObj.get_summary(full_text)
print (f'\nSummary: {summary}')

## initiate second object to confirm models do not have to reload
myObj2 = IntelligentBookAnalytics()
matching_title = myObj2.find_matchingtitle(titles[0], titles[1:])
print(f'\nMatching Title: {matching_title}')

summary = myObj2.get_summary(full_text)
print (f'\nSummary: {summary}')






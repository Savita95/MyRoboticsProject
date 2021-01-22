# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 02:01:35 2020

@author: savit
"""
import numpy as np
import dialogue_delivery as dd
import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import json
import logging
logging.basicConfig(filename="sample.log", level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

nltk.download('movie_reviews')


def extract_features(word_list):
    return dict([(word, True) for word in word_list])

#
def fn_load_json_file(filename=str):
    with open(filename, "r",encoding="utf8") as f:
        content = json.load(f)
    return content
# if __name__ == '__main__':
    # Load positive and negative reviews
positive_fileids = movie_reviews.fileids('pos')
negative_fileids = movie_reviews.fileids('neg')

features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in positive_fileids]
features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in negative_fileids]

# Split the data into train and test (80/20)
threshold_factor = 0.8
threshold_positive = int(threshold_factor * len(features_positive))
threshold_negative = int(threshold_factor * len(features_negative))

features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]

# print("Number of training datapoints: ", len(features_train))
# print("Number of test datapoints: ", len(features_test))

classifier = NaiveBayesClassifier.train(features_train)
# print("Accuracy of the classifier: ", nltk.classify.util.accuracy(classifier, features_test))

# response = "I dont Understand"


# ["I didnt get you","I couldnt understand you","I dont Understand", "Can you please pardon me","Can you repear","I am not clear on that topic","I understand","I am clear","Yes you can proceed"]

# def is_negative_response(response):
#     wordlist = dd.fn_load_json_file("word_list.json")
#     negative_words=wordlist.get("negation_list")
#     positiveWord_list = wordlist.get("positiveWord_list")
#     # negative_words = ['not', 'no', 'No', 'didnt']
#     if any(item in response.split() for item in negative_words):
#         # len(response.split())<2
#         negs = [w in response for w in negative_words]
#         return sum(negs) > 0
#     elif any(item in response.split() for item in positiveWord_list):
#         return False
#     else:
#         #print("\nReview:", response)
#         probdist = classifier.prob_classify(extract_features(response.split()))
#         pred_sentiment = probdist.max()
#         # print("Predicted sentiment: ", pred_sentiment)
#         # print("Probability: ", round(probdist.prob(pred_sentiment), 2))
#         if np.logical_and(pred_sentiment=="Negative",round(probdist.prob(pred_sentiment), 2) > 0.6):
#             return True
#         # if pred_sentiment=="Negative":
#         #     return True
#         else:
#             return False

response="yes"


def cosine_distance_countvectorizer_method(s1, s2):
    
    # sentences to list
    allsentences = [s1 , s2]
    
    # packages
    from sklearn.feature_extraction.text import CountVectorizer
    from scipy.spatial import distance
    
    # text to vector
    vectorizer = CountVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()
    
    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
#     print('Similarity of two sentences are equal to ',round((1-cosine)*100,2),'%')
    return int(round((1-cosine)*100,2))



# sentence="I couldnt understand you"
#print(wordlist)
#def match_perc (match_perc_neg,match_perc_pos):
#    if sorted(match_perc_neg,reverse=True)>sorted(match_perc_pos,reverse=True):
#        return True
#    else: return 

def match_perc (match_perc_neg,match_perc_pos,match_perc_neu):
    if sorted(match_perc_neg,reverse=True)[0]==0 and sorted(match_perc_pos,reverse=True)[0]==0 and sorted(match_perc_neu,reverse=True)[0]>0:
        return (False,-1)
    elif np.logical_and(sorted(match_perc_neg,reverse=True)[0]>sorted(match_perc_pos,reverse=True)[0],sorted(match_perc_neg,reverse=True)[0]==sorted(match_perc_neu,reverse=True)[0]):
        return (True,-1)
    elif  np.logical_and(sorted(match_perc_neg,reverse=True)[0]>sorted(match_perc_pos,reverse=True)[0],sorted(match_perc_neg,reverse=True)[0]!=sorted(match_perc_neu,reverse=True)[0]):
        return (True,0)
    elif  np.logical_and(sorted(match_perc_pos,reverse=True)[0]>sorted(match_perc_neg,reverse=True)[0],sorted(match_perc_pos,reverse=True)[0]==sorted(match_perc_neu,reverse=True)[0]):
        return (False,1)
    elif np.logical_and(sorted(match_perc_pos,reverse=True)[0]>sorted(match_perc_neg,reverse=True)[0],sorted(match_perc_pos,reverse=True)[0]!=sorted(match_perc_neu,reverse=True)[0]):
        return (False,0)

    # CDC=0
    # print(FileContent[i]+'\t'+FileContent[j]+'\t'+str(CDC))
def is_negative_response(response):
    match_perc_neg=[]
    match_perc_pos=[]
    match_perc_neu=[]

    wordlist =fn_load_json_file("word_list.json")
    negative_words=wordlist.get("negation_list")
    positiveWord_list = wordlist.get("positiveWord_list")
    neutralWord_list=wordlist.get("neutral_list")
    logging.info("inside")

    for i in range(len(negative_words)):
        try:
            CDC=int(cosine_distance_countvectorizer_method(response,negative_words[i]))
            match_perc_neg.append(CDC)
        except ValueError:
            CDC=0
            match_perc_neg.append(CDC)
    for i in range(len(positiveWord_list)):
        try:
            CDC=int(cosine_distance_countvectorizer_method(response,positiveWord_list[i]))
            match_perc_pos.append(CDC)
        except ValueError:
            CDC=0
            match_perc_pos.append(CDC)
        
    for i in range(len(neutralWord_list)):
        try:
            CDC=int(cosine_distance_countvectorizer_method(response,neutralWord_list[i]))
            match_perc_neu.append(CDC)
        except ValueError:
            CDC=0
            match_perc_neu.append(CDC)   
        
    if sorted(match_perc_neg,reverse=True)!=sorted(match_perc_pos,reverse=True):
        logging.info("Using cosine similarity ")
        try:
            bool_,val=match_perc (match_perc_neg,match_perc_pos,match_perc_neu)
            return bool_,val
        except TypeError:
            bool_=False
            val=0
            
        return bool_,val
    else:
        #print("\nReview:", response)
        probdist = classifier.prob_classify(extract_features(response.split()))
        pred_sentiment = probdist.max()
        # print("Predicted sentiment: ", pred_sentiment)
        # print("Probability: ", round(probdist.prob(pred_sentiment), 2))
        if np.logical_and(pred_sentiment=="Negative",round(probdist.prob(pred_sentiment), 2) > 0.6):
            logging.info("Using Naive base for Neg ")

            return True,2
        # if pred_sentiment=="Negative":
        #     return True
        else:
            logging.info("Using Naive base for pos ")
            return False,2
        
        
#bool,val=is_negative_response(response)
#print(bool,val)
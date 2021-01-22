# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:20:25 2020

@author: savit
"""
import dialogue_delivery as dd
import numpy as np

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
    print(type(cosine),"cosine")
    return round((1-cosine)*100,2)


wordlist = dd.fn_load_json_file("word_list.json")
negative_words=wordlist.get("negation_list")
positiveWord_list = wordlist.get("positiveWord_list")
neutralWord_list=wordlist.get("neutral_list")
sentence="I dont understand"
#print(wordlist)
match_perc_neg=[]
match_perc_pos=[]
match_perc_neu=[]
    
for i in range(len(negative_words)):
    try:
        CDC=cosine_distance_countvectorizer_method(sentence,negative_words[i])
        
    # CDC=0
    # print(FileContent[i]+'\t'+FileContent[j]+'\t'+str(CDC))
        print([sentence,negative_words[i],CDC])
    except ValueError:
        CDC=0
    match_perc_neg.append(int(CDC))
for i in range(len(positiveWord_list)):
    CDC=cosine_distance_countvectorizer_method(sentence,positiveWord_list[i])
    match_perc_pos.append(int(CDC))

    # CDC=0
    # print(FileContent[i]+'\t'+FileContent[j]+'\t'+str(CDC))
    print([sentence,positiveWord_list[i],CDC])    

for i in range(len(neutralWord_list)):
    CDC=int(cosine_distance_countvectorizer_method(sentence,neutralWord_list[i]))
    print(type(CDC))
    match_perc_neu.append(int(CDC))

    # CDC=0
    # print(FileContent[i]+'\t'+FileContent[j]+'\t'+str(CDC))
    print([sentence,neutralWord_list[i],CDC])  
#print(sorted(match_perc_neg,reverse=True)[0],"match_perc_neg")
print(type((match_perc_neu)))
def match_perc (match_perc_neg,match_perc_pos,match_perc_neu):
    if sorted(match_perc_neg,reverse=True)[0]==0 and sorted(match_perc_pos,reverse=True)[0]==0 and sorted(match_perc_neu,reverse=True)[0]>0:
        return (False,-1)
    elif np.logical_and(sorted(match_perc_neg,reverse=True)[0]>sorted(match_perc_pos,reverse=True)[0],sorted(match_perc_neg,reverse=True)[0]==sorted(match_perc_neu,reverse=True)[0]):
        return (True,-1)
    elif  np.logical_and(sorted(match_perc_neg,reverse=True)[0]>sorted(match_perc_pos,reverse=True)[0],sorted(match_perc_neg,reverse=True)[0]!=sorted(match_perc_neu,reverse=True)[0]):
        return (True,0)
    elif  np.logical_and(sorted(match_perc_pos,reverse=True)[0]>sorted(match_perc_pos,reverse=True)[0],sorted(match_perc_pos,reverse=True)[0]==sorted(match_perc_neu,reverse=True)[0]):
        print("pos1")
        return (False,1)
    elif np.logical_and(sorted(match_perc_pos,reverse=True)[0]>sorted(match_perc_pos,reverse=True)[0],sorted(match_perc_pos,reverse=True)[0]!=sorted(match_perc_neu,reverse=True)[0]):
        print("pos2")
        return (False,0)
        
#    
#if any(x==nan for x in match_perc_neg):
#        match_perc_neg.remove("nan")
#    if any(x==nan for x in match_perc_pos):
#        match_perc_pos.remove("nan")
#    if match_perc_neg.sort(reverse=True)[0]>match_perc_pos.sort(reverse=True)[0]:
#        return True
##    else: return False
#    elif match_perc_neg.sort(reverse=True)[0]<match_perc_pos.sort(reverse=True)[0]:
#        return False    
    
#Bool,value=match_perc (match_perc_neg,match_perc_pos,match_perc_neu)
#print(Bool,value)
def bool (match_perc_neg,match_perc_pos,match_perc_neu):
    try:
        bool_,val=match_perc (match_perc_neg,match_perc_pos,match_perc_neu)
        return bool_,val
    except TypeError:
        print("here")
        bool_=False
        val=0
        return bool_,val
    
boool,val=bool (match_perc_neg,match_perc_pos,match_perc_neu)  
print(boool,val)  
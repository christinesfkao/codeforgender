# coding=utf-8

import time
import re
import os
import sys
import codecs
import shutil
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer 

def per(msg):
    print(msg, file=sys.stderr)

if __name__ == "__main__":

# 參考資料 http://blog.csdn.net/eastmount/article/details/50473675

    corpus = []

    for line in open('top_1000.txt', 'r').readlines():
        nl = line.split(' ')
        nl.pop(0)
        corpus.append(' '.join(nl))

    per("doc loaded")

    vectorizer = CountVectorizer()

    transformer = TfidfTransformer()

    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()
    print(len(word))

    weight = tfidf.toarray()

    print('Features length: ' + str(len(word)))
    resName = "1000_user_tfidf.txt"
    result = codecs.open(resName, 'w', 'utf-8')
    for j in range(len(word)):
        result.write(word[j] + ' ')
    result.write('\n')

    for i in range(len(weight)):
        for j in range(len(word)):
            result.write(str(weight[i][j]) + ' ')
        result.write('\n')

    result.close()

    print('Start Kmeans:')

    from sklearn.cluster import KMeans
    clf = KMeans(n_clusters=3, n_jobs=-1)
    s = clf.fit(weight)
    print(s)
    print(clf.cluster_centers_)
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i-1])
        i = i + 1

    print(clf.inertia_)  

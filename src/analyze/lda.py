from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

en_stop = ["是","人","啊","沒","吧","啦","去","看","就是","好","新聞","他","她","為","但","為","這","才","又","真的","可以","不是","自己","喔"]

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# compile sample documents into a list
doc_set = []

for line in open('no_username.txt', 'r').readlines():
    doc_set.append(line.strip())

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    tokens = i.split(' ')

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamulticore.LdaMulticore(corpus, workers=23, num_topics=3, id2word = dictionary, passes=20)

print(ldamodel.print_topics(num_topics=3, num_words=5))

ldamodel.save('lda_output')

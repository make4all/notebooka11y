# %% [markdown]
# # code to perform LDA.
# ## imports and setup

# %% [markdown]
# ### pip installs.
# Please uncomment the code in the next cell if running from a jupytor notebook environment.
# I added this cell much later than when I started installing packages so I may have missed a few pip commands. Please update this cell if there are missing install commands.
# %%
# ! pip install nltk gensim wordcloud
# ! pip instal spacy
# !python -m spacy download en_core_web_sm
# %%

from ast import In
import pdb
from pprint import pprint
import string
from matplotlib import pyplot as plt
import numpy as np
import logging
# import nbformat
# import json
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
import spacy
import tqdm
# import pandas as pd
# import pypandoc
from wordcloud import WordCloud
import nltk
import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

logging.basicConfig(filename="log/lda.log", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
text = ''
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
nltk.download('stopwords')
from nltk.corpus import stopwords
# %% [markdown]
# # lambdas.
# Please include lambdas in the cell below. You should run this cell if you add a new lambda.
# %%

# %%
with open('nbText.txt','r') as f:
    text = f.read()
text = text.lower()    
# print(len(text.split()))
# %% [markdown]
# ## wordcloud.
# Here, we will visualize the data using a wordcloud. Please uncomment the code below if running in a notebook environment. It is commented out to save compute time when running in the shell.
# %% 
wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
wordcloud.generate(text)
# Visualize the word cloud
wordcloud.to_image()
wordcloud.to_file('wordcloud.png')
# %% [markdown]
# now perform the LatentDirichletAllocation


# %%

stop_words = stopwords.words('english')
stop_words_extension = ['model','train','test','use','data','matplotlib'] # tweek based on results.
stop_words.extend(stop_words_extension)
def sent_to_words(sentences):
        # deacc=True removes punctuations
        return(gensim.utils.simple_preprocess(sentences, deacc=True))
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def stemWords(texts):
    stemmer = nltk.stem.porter.PorterStemmer()
    return [[stemmer.stem(word) for word in doc] for doc in texts]

# make bigrams
def makeBigrams(texts):
     return [bigram_mod[text] for text in texts]
# make trigrams
def makeTrigrams(texts):
         return [trigram_mod[bigram_mod[doc]] for doc in texts] # I hate this line.... change it once I understand what's going on here.
# lemmatization
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    output = []
    for text in texts:
        doc = nlp(" ".join(text))
        # lematize doc and append to output
        output.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return output


data_words = list(sent_to_words(text))
print("data_words after sent_to_words")
print(data_words[:10])
# build bigram and trigram models. I don't fully understand why we're doing this; following an other tutorial in the hopes of getting useful output from the model
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
print("built bigram and trigram models")
# from what I understand, this probably freezes the model owing to better performance.
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)
print("got frozen bygram and trigram models")
# remove stop words
data_words = remove_stopwords(data_words)
print("removed stop words")

data_bigrams = makeBigrams(data_words)
print("made bigrams from data_words")
print(data_bigrams[:5])
print("lemmatization")
data_lematized = lemmatization(data_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
print("lemmatized data")
print(data_lematized[:1][0][:30])
# stem words
# data_words = stemWords(data_words)
# print("data_words")
# insert a pdb breakpoint
# pdb.set_trace()
# print(data_words[:10])
id2word = gensim.corpora.Dictionary(data_lematized)
texts = data_lematized
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# View
print("corpus")
print(corpus[:1][0][:30])
# %% [markdown]
# the data and the corpus is ready. now train the LDA model!
# %%
# number of topics
num_topics = 10
# build LDA Model  
lda_model = gensim.models.LdaMulticore(corpus=corpus,id2word=id2word,num_topics=num_topics,random_state = 100, chunksize=100,passes=10, per_word_topics= True) 
pprint(lda_model.print_topics())
print("coherence score for base model:")
CoherenceModel(model=lda_model, texts = data_lematized, dictionary = id2word, coherence = 'c_v').get_coherence()
# %% [markdown]
# ## hyperparameter tuning
# Here, we will use the tutorial example to tune the hyperparameters to see if we can get better results. Note that the code from here onwards takes time to run.

# %%
# helper function to compute coherence values.
def computeCoherence(corpus,dictionary,numTopics,a,b,data=data_lematized):
     print("training model with parameters: numTopics = {}, alpha = {}, beta = {}".format(numTopics,a,b))
     ldaModel = gensim.models.LdaMulticore(corpus=corpus,id2word=dictionary,num_topics=numTopics,random_state = 100, chunksize=100,passes=10, alpha=a, eta=b, per_word_topics= True)
     ldaCoherenceModel = CoherenceModel(model=ldaModel, texts = data, dictionary = id2word, coherence = 'c_v')
     print("coherence value is ")
     print(ldaCoherenceModel.get_coherence())
     return ldaCoherenceModel.get_coherence()


# topics range
minTopics = 2
maxTopics = 11
numTopicsRange = range(minTopics,maxTopics,1)
# alpha range
alphaRange = list(np.arange(0.01, 1, 0.3))
alphaRange.append('symmetric')
alphaRange.append('asymmetric')
betaRange = list(np.arange(0.01, 1, 0.3))
betaRange.append('symmetric')
numberOfDocs = len(corpus)
corpusSets = [gensim.utils.ClippedCorpus(corpus, int(numberOfDocs*0.75)),corpus]
corpusTitle = ['75% Corpus', '100% Corpus']
modelResults = {'Validation_Set': [],'topics':[],'alpha':[],'beta':[],'coherence':[]}
bar = tqdm.tqdm(total = len(numTopicsRange)*len(alphaRange)*len(betaRange)*len(corpusSets))
print("parameter tuning for {} corpus sets, for a total of {} alpha, {} beta, and {}k values".format(len(corpusSets),len(alphaRange),len(betaRange),len(numTopicsRange)))
for i in range(len(corpusSets)):
    for k in numTopicsRange:
        for a in alphaRange:
            for b in betaRange:
                print("computing coherence for corpus {}".format(corpusTitle[i]))
                cv = computeCoherence(corpus=corpusSets[i],dictionary=id2word,numTopics=k,a=a,b=b)
                modelResults['Validation_Set'].append(corpusTitle[i])
                modelResults['topics'].append(k)
                modelResults['alpha'].append(a)
                modelResults['beta'].append(b)
                modelResults['coherence'].append(cv)
                bar.update(1)
# %%
# visualize the results and save the plot to a file
df = pd.DataFrame(modelResults)
df.to_csv("modelResults.csv")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['topics'],df['alpha'],df['beta'],c=df['coherence'])
ax.set_xlabel('numTopics')
ax.set_ylabel('alpha')
ax.set_zlabel('beta')
ax.set_title('Coherence Scores')
plt.show()
fig.savefig('modelResults.png')
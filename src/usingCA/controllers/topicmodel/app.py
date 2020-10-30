import os
import io
import sys
import numpy as np

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy
import en_core_web_sm

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
nlp = en_core_web_sm.load()

# Tokenize words and Clean-up text
def sent_to_words(documents):
    for doc in documents:
        yield(gensim.utils.simple_preprocess(str(doc), deacc=True))  # deacc=True removes punctuations
# Remove Stopwords
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
# Lemmatize
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        #texts_out.append([token.lemma_ for token in doc])
    return texts_out
def takeSecond(elem):
    return elem[1]

def flatRecom(seq):
    seen_bl = set()
    seen_add_bl = seen_bl.add
    return [x for x in seq if not (x[0] in seen_bl or seen_add_bl(x[0]))]


def main():
  u_input = sys.argv[1]
  id2word = corpora.Dictionary.load('dict')
  lda_model = gensim.models.ldamodel.LdaModel.load('lda.model')
  corpus = corpora.MmCorpus('corpus.mm')
  data = lemmatization(remove_stopwords(list(sent_to_words([u_input]))), allowed_postags=['NOUN', 'ADJ', 'ADV'])
  new_doc = [id2word.doc2bow(text) for text in data]

  top_topics = sorted(doc_vec[0], key=takeSecond, reverse=True)[:5]
  x = lda_model.show_topics(num_topics=100, num_words=100,formatted=False)
  topics_words = [(tp[0], [[wd[0], wd[1]] for wd in tp[1]]) for tp in x]
  top_words = []
  for topic in top_topics:
      topic_id = topic[0]
      topic_prob = topic[1]
      for w in topics_words[topic_id][1]:
          top_words.append([w[0], w[1]*topic_prob])
  top_words = sorted(top_words, key=takeSecond, reverse=True)
  print({w[0]:w[1] for w in top_words[:10] if w[0] in id2word_key.token2id})

if __name__ == "__main__":
  main()

import pickle
import gensim
import pickle
from gensim import utils,corpora,models,similarities
import nltk
nltk.data.path.append('./nltk_data')
from nltk.corpus import stopwords
import re


# Paths
# model_path = "../../models/"
# data_path = '../../data/'
model_path = "search/models/"
data_path = 'search/data/'


# Files
dictionary_file = 'reuters.dict'
corpus_normailzed_file = 'reuters_corpus.list'
corpus_real_file = 'reuters_sentences.list'
tfidf_model_file = 'reuters.tfidf_model'
lsi_bow_model_file = 'reuters.bow.lsi_model'
lsi_tfidf_model_file = 'reuters.tfidf.lsi_model'
index_bow_file = 'reuters.bow.index'
index_tfidf_file = 'reuters.tfidf.index'


"""
This function normalizes the input text. Steps:
1) Remove white spaces
2) Lower case
3) Remove non alphabetical characters
4) Remove stop words
The boolean clean will dictate in the get_ids whether 
this needs to be done or the data is already preprocessed. 
"""
def normalize_text(text):
	stop_words  = set(stopwords.words('english'))
	punctuation = re.compile(r'[^a-zA-Z]+')
   	lowered_text = [w.lower() for w in text.split() if not re.match(punctuation, w)]
   	text_without_stopwords = [w for w in lowered_text if not w in stop_words]
	return text_without_stopwords


"""
This function returns the ids from the database that match the query according to a semantic
similarity. 
Parameters: 

"""
def get_ids(text, clean = True, method = 'bow', num_ids = 50):
	if clean:
		text = normalize_text(text)
	# dictionary = corpora.Dictionary.load(data_path+dictionary_file)
	dictionary = pickle.load(open(data_path+dictionary_file, "rb"))
	# print text
	if method == 'bow':
		vec = dictionary.doc2bow(text)
		lsi = models.LsiModel.load(model_path+lsi_bow_model_file)
		index = similarities.MatrixSimilarity.load(model_path+index_bow_file)
	
	elif method == 'tfidf':
		vec_bow = dictionary.doc2bow(text)
		tfidf = models.TfidfModel.load(model_path+tfidf_model_file)
		vec = tfidf[vec_bow]
		lsi = models.LsiModel.load(model_path+lsi_tfidf_model_file)
		index = similarities.MatrixSimilarity.load(model_path+index_tfidf_file)
	
	else:
		return []
	
	vec_lsi = lsi[vec]
	# print vec_lsi
	sims = index[vec_lsi]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	return [x[0] for x in sims[:num_ids]]


if __name__ == "__main__" :
	test = "rye"
	ids = get_ids(test)
	# corpus_real = pickle.load(open(data_path+corpus_real_file, "rb"))
	print ids, len(ids)
	# for x in ids:
	# 	print x
	# 	print corpus_real[x]


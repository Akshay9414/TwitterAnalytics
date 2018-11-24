#tokens
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from nltk import WordNetLemmatizer


#named entity
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def getKeywords(text):
	if(text==None):
		return []
	chunked = ne_chunk(pos_tag(word_tokenize(text)))
	prev = None
	continuous_chunk = []
	current_chunk = []
	
	for i in chunked:
		if type(i) == Tree:
			current_chunk.append(" ".join([token for token, pos in i.leaves()]))
		elif current_chunk:
			named_entity = " ".join(current_chunk)
			if named_entity not in continuous_chunk:
				continuous_chunk.append(named_entity)
				current_chunk = []
		else:
			continue

	if(current_chunk):
		named_entity = " ".join(current_chunk)
		if named_entity not in continuous_chunk:
			continuous_chunk.append(named_entity)

	NE = []
	for ne in continuous_chunk:
		NE.extend(ne.split(' '))

	#tokenize
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(text)

	#stopword removal
	stop_words = stopwords.words('english')
	tokens = [token.lower() for token in tokens if (token.lower() not in stop_words and token not in NE and not token.isdigit() and len(token)!=1 )]
	
	#stemming
	# ps = PorterStemmer()
	lemma = nltk.wordnet.WordNetLemmatizer()
	tokens = [lemma.lemmatize(w) for w in tokens]
	tokens = [token for token in tokens if (len(token)!=1 )]


	continuous_chunk.extend(tokens)

	return continuous_chunk



example = "Barack Obama is the husband of Michelle Obama. He lives in New York"
example2 = "AP sources: Prosecutors preparing charges against Cohen"
example3 = "India Inc. doesn’t hire mothers on career break graciously: Survey"
example4 = "SRK-Suhana are the most stylish daddy-daughter duo ever"
example5 = "best good better car cars serie series pencil pencils modify modified modification Dus Ka Dum finale: Salman, Shah Rukh Khan, Rani Mukerji, Sunil Grover wrap up seasons 3 of reality show"
example6 = "Hyundai launches all-new Santro, prices start at ₹3.90 lakh s i n g l e Rs"
print(getKeywords(example6))

# NE = get_continuous_chunks(example4)
# NE2 = []
# for ne in NE:
# 	NE2.extend(ne.split(' '))

# #tokenize
# tokenizer = RegexpTokenizer(r'\w+')
# tokens = tokenizer.tokenize(example4)

# #stopword removal
# stop_words = stopwords.words('english')
# tokens = [token.lower() for token in tokens if (token.lower() not in stop_words and token not in NE2)]
# #stemming
# ps = PorterStemmer()
# tokens = [ps.stem(w) for w in tokens]

# from nltk.stem.snowball import SnowballStemmer
# stemmer = SnowballStemmer('english')
# tokens = [stemmer.stem(w) for w in tokens]

# print(example4)
# NE.extend(tokens)
# print(NE)





# print('')

# NE = get_continuous_chunks(example5)
# NE2 = []
# for ne in NE:
# 	NE2.extend(ne.split(' '))

# #tokenize
# tokenizer = RegexpTokenizer(r'\w+')
# tokens = tokenizer.tokenize(example5)

# #stopword removal
# stop_words = stopwords.words('english')
# tokens = [token.lower() for token in tokens if (token.lower() not in stop_words and token not in NE2)]

# #stemming
# ps = PorterStemmer()
# tokens = [ps.stem(w) for w in tokens]

# print(example5)
# NE.extend(tokens)
# print(NE)






#freq distribution
# pos_freq = nltk.FreqDist(tokens)
# print(pos_freq.most_common(20))
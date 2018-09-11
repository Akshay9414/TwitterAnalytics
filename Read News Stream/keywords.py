#tokens
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


#named entity
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def get_continuous_chunks(text):
	tokenizer = RegexpTokenizer(r'\w+')
	chunked = ne_chunk(pos_tag(tokenizer.tokenize(text)))
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

	named_entity = " ".join(current_chunk)
	if named_entity not in continuous_chunk:
		continuous_chunk.append(named_entity)

	return continuous_chunk



example = "Barack Obama is the husband of Michelle Obama. He lives in New York"
example2 = "AP sources: Prosecutors preparing charges against Cohen"
example3 = "India Inc. doesn’t hire mothers on career break graciously: Survey"

NE = get_continuous_chunks(example3)
NE2 = []
for ne in NE:
	NE2.extend(ne.split(' '))

#tokenize
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(example3)

#stopword removal
stop_words = stopwords.words('english')
tokens = [token.lower() for token in tokens if (token.lower() not in stop_words and token not in NE2)]

#stemming
ps = PorterStemmer()
tokens = [ps.stem(w) for w in tokens]

print(NE2,tokens)






#freq distribution
# pos_freq = nltk.FreqDist(tokens)
# print(pos_freq.most_common(20))
#tokens
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords



example = "Barack Obama is the husband of Michelle Obama j New York . Pakis . India"
example2 = "AP sources: Prosecutors preparing charges against Cohen"


tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(example)

stop_words = stopwords.words('english')
tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
print(tokens)





#named entity
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def get_continuous_chunks(text):
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

    if continuous_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            continuous_chunk.append(named_entity)

    return continuous_chunk


print(get_continuous_chunks(example2))


#freq distribution
# pos_freq = nltk.FreqDist(tokens)
# print(pos_freq.most_common(20))
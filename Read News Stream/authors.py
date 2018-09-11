import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def get_continuous_chunks(text):
    text = text.replace('by','')
    text = text.replace('By','')
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

    named_entity = " ".join(current_chunk)
    if named_entity not in continuous_chunk:
        continuous_chunk.append(named_entity)

    return continuous_chunk

str_arr = ["By JULIET LINDERMAN, Associated Press","By MATTHEW DALY, Associated Press","Tim Kenneally, provided by","Rasul Bailay and Writankar Mukherjee","Mirror Football","By ALEX VEIGA, AP Business Writer"]

for str in str_arr:
    print(get_continuous_chunks(str))
    # print(ne_chunk(pos_tag(word_tokenize(str))))
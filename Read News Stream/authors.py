import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def getAuthors(text):
    # text2 = text.replace('by','')
    # text2 = text2.replace('By','') + "."
    text2 = "By "+text+"."
    chunked = ne_chunk(pos_tag(word_tokenize(text2)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        # print(i)
        if type(i) == Tree:
            # print("Tree")
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

    if not continuous_chunk:
        if(text.isupper()):
            return [text]
        words = text.split(" ")
        for word in words:
            if word.isupper():
                return [word]

    # authors = [author for author in continuous_chunk if author]
    return continuous_chunk

str_arr = ["G. Anand","ET","ET Online","Jonathan Garber","jgarber@businessinsider.com (Jonathan Garber), Jonathan Garber","Anandi Chandrashekhar","ET Online","AFP","Reuters","Rasul Bailay and Writankar Mukherjee","Tim Kenneally, provided by","By JULIET LINDERMAN, Associated Press","By MATTHEW DALY, Associated Press","By ALEX VEIGA, AP Business Writer"]

for str in str_arr:
    print(str)
    # getAuthors(str)
    print(getAuthors(str))
    # print(ne_chunk(pos_tag(word_tokenize(str))))
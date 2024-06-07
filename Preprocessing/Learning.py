from gensim.models import word2vec
import MeCab
import re
import logging
from tqdm import tqdm
from multiprocessing import Pool
import os
os.chdir(os.path.dirname(__file__))
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
with open("wiki.txt", "r", encoding='utf-8') as f:
    text = f.read()
sentences = []
for s in tqdm(re.split("[\n。]", text)):
    s = s.strip()
    if s:
        sentences.append(s + "。")
sentences = list(filter(None, sentences))
print(len(sentences))
def tokenize(text):
    tagger = MeCab.Tagger('-Owakati')
    return tagger.parse(text).strip().split()
def tokenize_list(text_list):
    with Pool() as pool:
        results = list(tqdm(pool.imap(tokenize, text_list), total=len(text_list)))
    return results
w2v_train_data = tokenize_list(sentences)
def save_words_to_file(word_list, filename):
    with open(filename, "w", encoding='utf-8') as file:
        for word in tqdm(word_list):
            file.write(" ".join(word) + "\n")
save_words_to_file(w2v_train_data, 'wiki_wakati.txt')
model = word2vec(w2v_train_data, size=200, window=5, sample=1e-3, negative=5, hs=0)
model.save("word2vec.model")
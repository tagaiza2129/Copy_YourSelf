from gensim.models import word2vec
import MeCab
import re
import logging
from tqdm import tqdm
from multiprocessing import Pool
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
os.environ["MECABRC"] = "/etc/mecabrc"
os.chdir(r"/media/F/wikipedia")

def read_and_process(file_path, chunk_size=5120*5120):
    sentences_data=[]
    with open(file_path, "r", encoding='utf-8') as file:
        data = file.read(chunk_size)
        for s in re.split("[\n。]", data):
            s = s.strip()
            if s:
                sentences_data.append(s + "。") 
    return sentences_data

def tokenize(text):
    tagger = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    return tagger.parse(text).strip().split()

def tokenize_generator(text_list):
    with Pool() as pool:
        results = list(tqdm(pool.imap(tokenize, text_list),total=len(text_list)))
    return results

print("Reading and processing file...")
tokenized_sentences = tokenize_generator(read_and_process("wiki.txt"))
print("Training model...")
model = word2vec.Word2Vec(tokenized_sentences, vector_size=200, window=5, min_count=1, sample=1e-3, negative=5, hs=0, epochs=1000)
model.save("word2vec.model")

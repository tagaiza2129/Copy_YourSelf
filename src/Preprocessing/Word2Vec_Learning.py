from gensim.models import word2vec
import MeCab
import re
import logging
from tqdm import tqdm
from multiprocessing import Pool
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
os.environ["MECABRC"] = "/etc/mecabrc"
#ファイルを読み込んで、文ごとに分割してリスト化して返す
#負荷でKilledされるので、chunk_sizeを小さくし対処
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
#ファイルをリスト化して返す
#正直この程度だったら関数化するまでも無い気がする
def file_setting(file_path):
    os.chdir(file_path)
    file_list=os.listdir(file_path)
    return file_list

def Lerning(Processing_data:str,epoch:int):
    print("Reading and processing file...")
    file_list=file_setting(Processing_data)
    sentences_datas=[]
    for i in range(len(file_list)):
        sentences_datas+=read_and_process(file_list[i])
    tokenized_sentences = tokenize_generator(sentences_datas)
    print("Training model...")
    model = word2vec.Word2Vec(tokenized_sentences, vector_size=200, window=5, min_count=1, sample=1e-3, negative=5, hs=0, epochs=epoch)
    os.chdir(os.path.join(os.path.dirname(__file__), "model"))
    model.save("word2vec.model")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("Processing_data", type=str, help="学習データの場所")
    parser.add_argument("--epoch", type=int, default=10, help="学習回数")
    args = parser.parse_args()
    Lerning(args.Processing_data,args.epoch)

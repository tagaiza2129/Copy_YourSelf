import MeCab
import os
from gensim.models import Word2Vec
import re
from gensim.models import word2vec
import logging
from tqdm import tqdm
from multiprocessing import Pool
def Morphological_analysis(text_list:list):
    Morphological_list=[]
    with tqdm(total=len(text_list)) as pbar:
        for count in range(len(text_list)):
            text=str(text_list[count])
            os.chdir(os.path.dirname(__file__))
            #辞書の位置がDockerで環境を構築されている前提
            tagger = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
            result=tagger.parse(text)
            Morphological_list.append(result)
            progress_percentage = 100 * (pbar.n / len(text_list))
            if progress_percentage < 20.22:
                pbar.colour = "red"
            elif progress_percentage < 80.88:
                pbar.colour = "yellow"
            else:
                pbar.colour = "green"
            pbar.update(1)
    for count in range(len(Morphological_list)):
        Morphological_list[count]=Morphological_list[count].replace("\n","")
        if Morphological_list[count]=="":
            Morphological_list.pop(count)
    return Morphological_list
#単語をベクトル化する関数
#詳しい原理等が分かる動画:https://youtu.be/l8YCKz15Hn8
def vector(text_list:list):
    vector_list=[]
    code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％ ]')
    os.chdir(os.path.dirname(__file__))
    model=Word2Vec.load("word2vec.model")
    with tqdm(total=len(text_list))as pbar:
        for count in range(len(text_list)):
            text=str(text_list[count])
            text=code_regex.sub('',text)
            result=model.wv[text]
            vector_list.append(result)
            progress_percentage = 100 * (pbar.n / len(text_list))
            if progress_percentage < 20.22:
                pbar.colour = "red"
            elif progress_percentage < 80.88:
                pbar.colour = "yellow"
            else:
                pbar.colour = "green"
            pbar.update(1)
    return vector_list

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

#これをメインとして使った場合、Word2Vecの学習する
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("Processing_data", type=str, help="学習データの場所")
    parser.add_argument("--epoch", type=int, default=10, help="学習回数")
    args = parser.parse_args()
    Lerning(args.Processing_data,args.epoch)

import MeCab
import time
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
import os
from gensim.models import Word2Vec
import re
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
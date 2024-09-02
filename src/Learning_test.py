#Rustが書くの面倒になってきたから一旦Pythonで書く
#PyTorchでのチャットボットの学習コード
from Preprocessing import token
from inference import Seq2Seq
import os
import numpy as np
APP_dir =os.path.dirname(os.path.dirname(__file__))
os.chdir(os.path.join(APP_dir,"Learning_File/Learning_test_model/Lerarning"))
with open("input.txt","r",encoding="utf-8") as f:
    input=f.readlines()
with open("output.txt","r",encoding="utf-8") as f:
    output=f.readlines()

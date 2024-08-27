#Rustが書くの面倒になってきたから一旦Pythonで書く
#Tensorflowでのチャットボットの学習コード
from Preprocessing import token
from inference import Seq2Seq
import os
import MeCab
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
APP_dir =os.path.dirname(os.path.dirname(__file__))
os.chdir(os.path.join(APP_dir,"Learning_File/Learning_test_model/Lerarning"))
with open("input.txt","r",encoding="utf-8") as f:
    input=f.readlines()
with open("output.txt","r",encoding="utf-8") as f:
    output=f.readlines()
os.environ["MECABRC"] = "/etc/mecabrc"
tagger = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
inputs=[]
outputs=[]
tokenizer = Tokenizer()
for i in range(len(input)):
    result=tagger.parse(input[i])
    inputs.append(result)
    with open("input_morphological.txt","a",encoding="utf-8") as f:
        f.write(result)
for a in range(len(output)):
    result=tagger.parse(output[a])
    outputs.append(result)
    with open("output_morphological.txt","a",encoding="utf-8") as f:
        f.write(result)
tokens=token.get_token(inputs,outputs)
models=Seq2Seq.Learning(tokens[0],tokens[1],tokens[2],100,"/device:XPU:0")
def decode_sequence(input_seq,encoder_model,decoder_model,tokenizer):
    # エンコーダーで状態を取得
    states_value = encoder_model.predict(input_seq)

    # 開始トークンを使ってシーケンス生成開始
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = tokenizer.word_index['startseq']

    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # 出力トークンを単語に変換
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = tokenizer.index_word[sampled_token_index]
        decoded_sentence += ' ' + sampled_word

        # 終了条件: 最大長さに達するか、終了トークンが生成された場合
        if sampled_word == 'endseq' or len(decoded_sentence) > 50:
            stop_condition = True

        # 更新: 次のターゲットシーケンス
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index

        states_value = [h, c]

    return decoded_sentence
test_input = "Hello"
test_input_seq = tokenizer.texts_to_sequences([test_input])
test_input_seq = pad_sequences(test_input_seq, maxlen=len(tokens[2]), padding='post')

# 応答生成
response = decode_sequence(test_input_seq)

print("Chatbot:", response)

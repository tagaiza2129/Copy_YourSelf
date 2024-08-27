import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore


def get_token(input_texts:list,output_texts:list):
    # トークナイザーの設定
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(input_texts + output_texts)

    # テキストをシーケンスに変換
    input_sequences = tokenizer.texts_to_sequences(input_texts)
    target_sequences = tokenizer.texts_to_sequences(output_texts)

    # パディングを追加（シーケンスを同じ長さに揃える）
    input_sequences = pad_sequences(input_sequences, padding='post')
    target_sequences = pad_sequences(target_sequences, padding='post')

    # 語彙サイズの取得
    vocab_size = len(tokenizer.word_index) + 1
    return [vocab_size,input_sequences,target_sequences]

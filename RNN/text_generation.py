#!/usr/bin/env python
# coding: utf-8

# ##### Copyright 2019 The TensorFlow Authors.

# In[1]:


#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# # RNN によるテキスト生成

# <table class="tfo-notebook-buttons" align="left">
#   <td>
#     <a target="_blank" href="https://www.tensorflow.org/tutorials/text/text_generation"><img src="https://www.tensorflow.org/images/tf_logo_32px.png" />View on TensorFlow.org</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://colab.research.google.com/github/tensorflow/docs-l10n/blob/master/site/ja/tutorials/text/text_generation.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://github.com/tensorflow/docs-l10n/blob/master/site/ja/tutorials/text/text_generation.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
#   </td>
#   <td>
#     <a href="https://storage.googleapis.com/tensorflow_docs/docs-l10n/site/ja/tutorials/text/text_generation.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download notebook</a>
#   </td>
# </table>

# Note: これらのドキュメントは私たちTensorFlowコミュニティが翻訳したものです。コミュニティによる 翻訳は**ベストエフォート**であるため、この翻訳が正確であることや[英語の公式ドキュメント](https://www.tensorflow.org/?hl=en)の 最新の状態を反映したものであることを保証することはできません。 この翻訳の品質を向上させるためのご意見をお持ちの方は、GitHubリポジトリ[tensorflow/docs](https://github.com/tensorflow/docs)にプルリクエストをお送りください。 コミュニティによる翻訳やレビューに参加していただける方は、 [docs-ja@tensorflow.org メーリングリスト](https://groups.google.com/a/tensorflow.org/forum/#!forum/docs-ja)にご連絡ください。

# このチュートリアルでは、文字ベースの RNN を使ってテキストを生成する方法を示します。ここでは、Andrej Karpathy の [The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) からのシェイクスピア作品のデータセットを使います。このデータからの文字列（"Shakespear"）を入力にして、文字列中の次の文字（"e"）を予測するモデルを訓練します。このモデルを繰り返し呼び出すことで、より長い文字列を生成することができます。
# 
# Note: このノートブックの実行を速くするために GPU による高速化を有効にしてください。Colab では、*ランタイム　＞　ランタイムのタイプを変更 ＞ ハードウェアアクセラレータ ＞ GPU* を選択します。ローカルで実行する場合には、TensorFlow のバージョンが 1.11 以降であることを確認してください。
# 
# このチュートリアルには、[tf.keras](https://www.tensorflow.org/programmers_guide/keras) と [eager execution](https://www.tensorflow.org/programmers_guide/eager) を使ったコードが含まれています。下記は、このチュートリアルのモデルを 30 エポック訓練したものに対して、文字列 "Q" を初期値とした場合の出力例です。
# 
# <pre>
# QUEENE:
# I had thought thou hadst a Roman; for the oracle,
# Thus by All bids the man against the word,
# Which are so weak of care, by old care done;
# Your children were in your holy love,
# And the precipitation through the bleeding throne.
# 
# BISHOP OF ELY:
# Marry, and will, my lord, to weep in such a one were prettiest;
# Yet now I was adopted heir
# Of the world's lamentable day,
# To watch the next way with his father with his face?
# 
# ESCALUS:
# The cause why then we are all resolved more sons.
# 
# VOLUMNIA:
# O, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, it is no sin it should be dead,
# And love and pale as any will to that word.
# 
# QUEEN ELIZABETH:
# But how long have I heard the soul for this world,
# And show his hands of life be proved to stand.
# 
# PETRUCHIO:
# I say he look'd on, if I must be content
# To stay him from the fatal of our country's bliss.
# His lordship pluck'd from this sentence then for prey,
# And then let us twain, being the moon,
# were she such a case as fills m
# </pre>
# 
# いくつかは文法にあったものがある一方で、ほとんどは意味をなしていません。このモデルは、単語の意味を学習していませんが、次のことを考えてみてください。
# 
# * このモデルは文字ベースです。訓練が始まった時に、モデルは英語の単語のスペルも知りませんし、単語がテキストの単位であることも知らないのです。
# 
# * 出力の構造は戯曲に似ています。だいたいのばあい、データセットとおなじ大文字で書かれた話し手の名前で始まっています。
# 
# * 以下に示すように、モデルはテキストの小さなバッチ（各100文字）で訓練されていますが、一貫した構造のより長いテキストのシーケンスを生成できます。

# ## 設定

# ### TensorFlow 等のライブラリインポート

# In[2]:


import tensorflow as tf

import numpy as np
import os
import time


# ### シェイクスピアデータセットのダウンロード
# 
# 独自のデータで実行するためには下記の行を変更してください。

# In[3]:


path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')


# ### データの読み込み
# 
# まずはテキストをのぞいてみましょう。

# In[4]:


# 読み込んだのち、Python 2 との互換性のためにデコード
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
# テキストの長さは含まれる文字数
print ('Length of text: {} characters'.format(len(text)))


# In[5]:


# テキストの最初の 250文字を参照
print(text[:250])


# In[6]:


# ファイル中のユニークな文字の数
vocab = sorted(set(text))
print ('{} unique characters'.format(len(vocab)))


# ## テキストの処理

# ### テキストのベクトル化
# 
# 訓練をする前に、文字列を数値表現に変換する必要があります。2つの参照テーブルを作成します。一つは文字を数字に変換するもの、もう一つは数字を文字に変換するものです。

# In[7]:


# それぞれの文字からインデックスへの対応表を作成
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)

text_as_int = np.array([char2idx[c] for c in text])


# これで、それぞれの文字を整数で表現できました。文字を、0 から`len(unique)` までのインデックスに変換していることに注意してください。

# In[8]:


print('{')
for char,_ in zip(char2idx, range(20)):
    print('  {:4s}: {:3d},'.format(repr(char), char2idx[char]))
print('  ...\n}')


# In[9]:


# テキストの最初の 13 文字がどのように整数に変換されるかを見てみる
print ('{} ---- characters mapped to int ---- > {}'.format(repr(text[:13]), text_as_int[:13]))


# ### 予測タスク

# ある文字、あるいは文字列が与えられたとき、もっともありそうな次の文字はなにか？これが、モデルを訓練してやらせたいタスクです。モデルへの入力は文字列であり、モデルが出力、つまりそれぞれの時点での次の文字を予測をするようにモデルを訓練します。
# 
# RNN はすでに見た要素に基づく内部状態を保持しているため、この時点までに計算されたすべての文字を考えると、次の文字は何でしょうか？

# ### 訓練用サンプルとターゲットを作成
# 
# つぎに、テキストをサンプルシーケンスに分割します。それぞれの入力シーケンスは、元のテキストからの `seq_length` 個の文字を含みます。
# 
# 入力シーケンスそれぞれに対して、対応するターゲットは同じ長さのテキストを含みますが、1文字ずつ右にシフトしたものです。
# 
# そのため、テキストを `seq_length+1` のかたまりに分割します。たとえば、 `seq_length` が 4 で、テキストが "Hello" だとします。入力シーケンスは "Hell" で、ターゲットシーケンスは "ello" となります。
# 
# これを行うために、最初に `tf.data.Dataset.from_tensor_slices` 関数を使ってテキストベクトルを文字インデックスの連続に変換します。

# In[10]:


# ひとつの入力としたいシーケンスの文字数としての最大の長さ
seq_length = 100
examples_per_epoch = len(text)//(seq_length+1)

# 訓練用サンプルとターゲットを作る
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

for i in char_dataset.take(5):
  print(idx2char[i.numpy()])


# `batch` メソッドを使うと、個々の文字を求める長さのシーケンスに簡単に変換できます。

# In[11]:


sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

for item in sequences.take(5):
  print(repr(''.join(idx2char[item.numpy()])))


# シーケンスそれぞれに対して、`map` メソッドを使って各バッチに単純な関数を適用することで、複製とシフトを行い、入力テキストとターゲットテキストを生成します。

# In[12]:


def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)


# 最初のサンプルの入力とターゲットを出力します。

# In[13]:


for input_example, target_example in  dataset.take(1):
  print ('Input data: ', repr(''.join(idx2char[input_example.numpy()])))
  print ('Target data:', repr(''.join(idx2char[target_example.numpy()])))


# これらのベクトルのインデックスそれぞれが一つのタイムステップとして処理されます。タイムステップ 0 の入力として、モデルは "F" のインデックスを受け取り、次の文字として "i" のインデックスを予測しようとします。次のタイムステップでもおなじことをしますが、`RNN` は現在の入力文字に加えて、過去のステップのコンテキストも考慮します。

# In[14]:


for i, (input_idx, target_idx) in enumerate(zip(input_example[:5], target_example[:5])):
    print("Step {:4d}".format(i))
    print("  input: {} ({:s})".format(input_idx, repr(idx2char[input_idx])))
    print("  expected output: {} ({:s})".format(target_idx, repr(idx2char[target_idx])))


# ### 訓練用バッチの作成
# 
# `tf.data` を使ってテキストを分割し、扱いやすいシーケンスにします。しかし、このデータをモデルに供給する前に、データをシャッフルしてバッチにまとめる必要があります。

# In[15]:


# バッチサイズ
BATCH_SIZE = 64

# データセットをシャッフルするためのバッファサイズ
# （TF data は可能性として無限長のシーケンスでも使えるように設計されています。
# このため、シーケンス全体をメモリ内でシャッフルしようとはしません。
# その代わりに、要素をシャッフルするためのバッファを保持しています）
BUFFER_SIZE = 10000

dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

dataset


# ## モデルの構築

# `tf.keras.Sequential` を使ってモデルを定義します。この簡単な例では、モデルの定義に3つのレイヤーを使用しています。
# 
# * `tf.keras.layers.Embedding`: 入力レイヤー。それぞれの文字を表す数を `embedding_dim`　次元のベクトルに変換する、訓練可能な参照テーブル。
# * `tf.keras.layers.GRU`: サイズが `units=rnn_units` のRNNの一種（ここに LSTM レイヤーを使うこともできる）。
# * `tf.keras.layers.Dense`: `vocab_size` の出力を持つ、出力レイヤー。

# In[16]:


# 文字数で表されるボキャブラリーの長さ
vocab_size = len(vocab)

# 埋め込みベクトルの次元
embedding_dim = 256

# RNN ユニットの数
rnn_units = 1024


# In[17]:


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
  model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim,
                              batch_input_shape=[batch_size, None]),
    tf.keras.layers.GRU(rnn_units,
                        return_sequences=True,
                        stateful=True,
                        recurrent_initializer='glorot_uniform'),
    tf.keras.layers.Dense(vocab_size)
  ])
  return model


# In[18]:


model = build_model(
  vocab_size = len(vocab),
  embedding_dim=embedding_dim,
  rnn_units=rnn_units,
  batch_size=BATCH_SIZE)


# 1文字ごとにモデルは埋め込みベクトルを検索し、その埋め込みベクトルを入力として GRU を 1 タイムステップ実行します。そして Dense レイヤーを適用して、次の文字の対数尤度を予測するロジットを生成します。
# 
# ![A drawing of the data passing through the model](https://github.com/masa-ita/tf-docs/blob/site_ja_tutorials_text_text_generation/site/ja/tutorials/text/images/text_generation_training.png?raw=1)

# ## モデルを試す
# 
# 期待通りに動作するかどうかを確認するためモデルを動かしてみましょう。
# 
# 最初に、出力の shape を確認します。

# In[19]:


for input_example_batch, target_example_batch in dataset.take(1):
  example_batch_predictions = model(input_example_batch)
  print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")


# 上記の例では、入力のシーケンスの長さは `100` ですが、モデルはどのような長さの入力でも実行できます。

# In[20]:


model.summary()


# モデルから実際の予測を得るには出力の分布からサンプリングを行う必要があります。この分布は、文字ボキャブラリー全体のロジットで定義されます。
# 
# Note: この分布から _サンプリング_ するということが重要です。なぜなら、分布の _argmax_ をとったのでは、モデルは簡単にループしてしまうからです。
# 
# バッチ中の最初のサンプルで試してみましょう。

# In[21]:


sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
sampled_indices = tf.squeeze(sampled_indices,axis=-1).numpy()


# これにより、タイムステップそれぞれにおいて、次の文字のインデックスの予測が得られます。

# In[22]:


sampled_indices


# これらをデコードすることで、この訓練前のモデルによる予測テキストをみることができます。

# In[23]:


print("Input: \n", repr("".join(idx2char[input_example_batch[0]])))
print()
print("Next Char Predictions: \n", repr("".join(idx2char[sampled_indices ])))


# ## モデルの訓練

# ここまでくれば問題は標準的な分類問題として扱うことができます。これまでの RNN の状態と、いまのタイムステップの入力が与えられ、次の文字のクラスを予測します。

# ### オプティマイザと損失関数の付加

# この場合、標準の `tf.keras.losses.sparse_categorical_crossentropy` 損失関数が使えます。予測の最後の次元に適用されるからです。
# 
# このモデルはロジットを返すので、`from_logits` フラグをセットする必要があります。

# In[24]:


def loss(labels, logits):
  return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

example_batch_loss  = loss(target_example_batch, example_batch_predictions)
print("Prediction shape: ", example_batch_predictions.shape, " # (batch_size, sequence_length, vocab_size)")
print("scalar_loss:      ", example_batch_loss.numpy().mean())


# `tf.keras.Model.compile` を使って、訓練手順を定義します。既定の引数を持った `tf.keras.optimizers.Adam` と、先ほどの loss 関数を使用しましょう。

# In[25]:


model.compile(optimizer='adam', loss=loss)


# ### チェックポイントの構成

# `tf.keras.callbacks.ModelCheckpoint` を使って、訓練中にチェックポイントを保存するようにします。

# In[26]:


# チェックポイントが保存されるディレクトリ
checkpoint_dir = './training_checkpoints'
# チェックポイントファイルの名称
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)


# ### 訓練の実行

# 訓練時間を適切に保つために、10エポックを使用してモデルを訓練します。Google Colab を使用する場合には、訓練を高速化するためにランタイムを GPU に設定します。

# In[27]:


EPOCHS=10


# In[28]:


history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])


# ## テキスト生成

# ### 最終チェックポイントの復元

# 予測ステップを単純にするため、バッチサイズ 1 を使用します。
# 
# RNN が状態をタイムステップからタイムステップへと渡す仕組みのため、モデルは一度構築されると固定されたバッチサイズしか受け付けられません。
# 
# モデルを異なる `batch_size` で実行するためには、モデルを再構築し、チェックポイントから重みを復元する必要があります。

# In[29]:


tf.train.latest_checkpoint(checkpoint_dir)


# In[30]:


model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

model.build(tf.TensorShape([1, None]))


# In[31]:


model.summary()


# ### 予測ループ
# 
# 下記のコードブロックでテキストを生成します。
# 
# * 最初に、開始文字列を選択し、RNN の状態を初期化して、生成する文字数を設定します。
# 
# * 開始文字列と RNN の状態を使って、次の文字の予測分布を得ます。
# 
# * つぎに、カテゴリー分布を使用して、予測された文字のインデックスを計算します。この予測された文字をモデルの次の入力にします。
# 
# * モデルによって返された RNN の状態はモデルにフィードバックされるため、1つの文字だけでなく、より多くのコンテキストを持つことになります。つぎの文字を予測した後、更新された RNN の状態が再びモデルにフィードバックされます。こうしてモデルは以前に予測した文字からさらにコンテキストを得ることで学習するのです。
# 
# ![To generate text the model's output is fed back to the input](https://github.com/masa-ita/tf-docs/blob/site_ja_tutorials_text_text_generation/site/ja/tutorials/text/images/text_generation_sampling.png?raw=1)
# 
# 生成されたテキストを見ると、モデルがどこを大文字にするかや、段落の区切り方、シェークスピアらしい書き言葉を真似ることを知っていることがわかります。しかし、訓練のエポック数が少ないので、まだ一貫した文章を生成するところまでは学習していません。

# In[32]:


def generate_text(model, start_string):
  # 評価ステップ（学習済みモデルを使ったテキスト生成）

  # 生成する文字数
  num_generate = 1000

  # 開始文字列を数値に変換（ベクトル化）
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # 結果を保存する空文字列
  text_generated = []

  # 低い temperature　は、より予測しやすいテキストをもたらし
  # 高い temperature は、より意外なテキストをもたらす
  # 実験により最適な設定を見つけること
  temperature = 1.0

  # ここではバッチサイズ　== 1
  model.reset_states()
  for i in range(num_generate):
      predictions = model(input_eval)
      # バッチの次元を削除
      predictions = tf.squeeze(predictions, 0)

      # カテゴリー分布をつかってモデルから返された文字を予測 
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      # 過去の隠れ状態とともに予測された文字をモデルへのつぎの入力として渡す
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])

  return (start_string + ''.join(text_generated))


# In[33]:


print(generate_text(model, start_string=u"ROMEO: "))


# この結果を改善するもっとも簡単な方法は、もっと長く訓練することです（`EPOCHS=30` を試してみましょう）。
# 
# また、異なる初期文字列を使ったり、モデルの精度を向上させるためにもうひとつ RNN レイヤーを加えたり、temperature パラメータを調整して、よりランダム性の強い、あるいは、弱い予測を試してみたりすることができます。

# ## 上級編： 訓練のカスタマイズ
# 
# 上記の訓練手順は単純ですが、制御できるところがそれほどありません。
# 
# モデルを手動で実行する方法を見てきたので、訓練ループを展開し、自分で実装してみましょう。このことが、たとえばモデルのオープンループによる出力を安定化するための _カリキュラム学習_ を実装するための出発点になります。
# 
# 勾配を追跡するために `tf.GradientTape` を使用します。このアプローチについての詳細を学ぶには、 [eager execution guide](https://www.tensorflow.org/guide/eager) をお読みください。
# 
# この手順は下記のように動作します。
# 
# * 最初に、RNN の状態を初期化する。`tf.keras.Model.reset_states` メソッドを呼び出すことでこれを実行する。
# 
# * つぎに、（1バッチずつ）データセットを順番に処理し、それぞれのバッチに対する*予測値*を計算する。
# 
# * `tf.GradientTape` をオープンし、そのコンテキストで、予測値と損失を計算する。
# 
# * `tf.GradientTape.grads` メソッドを使って、モデルの変数に対する損失の勾配を計算する。
# 
# * 最後に、オプティマイザの `tf.train.Optimizer.apply_gradients` メソッドを使って、逆方向の処理を行う。

# In[34]:


model = build_model(
  vocab_size = len(vocab),
  embedding_dim=embedding_dim,
  rnn_units=rnn_units,
  batch_size=BATCH_SIZE)


# In[35]:


optimizer = tf.keras.optimizers.Adam()


# In[36]:


@tf.function
def train_step(inp, target):
  with tf.GradientTape() as tape:
    predictions = model(inp)
    loss = tf.reduce_mean(
        tf.keras.losses.sparse_categorical_crossentropy(
            target, predictions, from_logits=True))
  grads = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(grads, model.trainable_variables))

  return loss


# In[37]:


# 訓練ステップ
EPOCHS = 10

for epoch in range(EPOCHS):
  start = time.time()

  # 各エポックの最初に、隠れ状態を初期化する
  # 最初は隠れ状態は None
  hidden = model.reset_states()

  for (batch_n, (inp, target)) in enumerate(dataset):
    loss = train_step(inp, target)

    if batch_n % 100 == 0:
      template = 'Epoch {} Batch {} Loss {}'
      print(template.format(epoch+1, batch_n, loss))

  # 5エポックごとにモデル（のチェックポイント）を保存する
  if (epoch + 1) % 5 == 0:
    model.save_weights(checkpoint_prefix.format(epoch=epoch))

  print ('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
  print ('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

model.save_weights(checkpoint_prefix.format(epoch=epoch))


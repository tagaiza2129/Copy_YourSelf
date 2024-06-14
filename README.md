# Copy_YourSelf
## Copy_YourSelfとは
Googleが提供している機械学習のためのモジュールであるTensorflowを活用し\
RNN等の手法で自然言語処理を行いユーザーの性格を模したChatAIを作るプロジェクトです
## 使い方(How to Use)
### 学習
```sh
$ python3 main.py 学習させるデータ -m Learning
```
学習させる場合は上記のコマンドで学習させることができます
### 推論
```sh
$ python3 main.py 動かすモデルデータ -m Inference
```
学習したデータで推論するには上記のコマンドで推論することができます
### その他実行する際に使用できる引数等
``` sh
UserName@ComputerName $ python3 main.py -h
usage: python3 main.py <file_Path> <options>

TensorFlow等を活用し、人格形成を学習させたChatBotを作成したいです...

options:
  -h, --help            show this help message and exit
  --processing_data PROCESSING_DATA
                        学習、又は推論に利用するデータを指定します。
  -d DEVICE, --device DEVICE
                        学習に利用するデバイスを指定します。 使用想定デバイス CPU:まあ...そのままの意味 GPU:NVIDIA製のGPUを利用し学習します XPU:intel製のGPUを利用し学習します
  -p PORT, --port PORT  分散学習に利用するサーバーのポートを指定します
  -e EPOCH, --epoch EPOCH
                        何回繰り返し学習させるかを指定します。
  -s SERVER_MULTI_PROCESSING, --server_multi_processing SERVER_MULTI_PROCESSING
                        分散学習を行うかどうかを指定します。
  -m MODE, --mode MODE  学習から推論までのモードを指定します。 学習:学習を行います。 推論:推論を行います。
```
## インストール方法
### WSL、Ubuntu
※純Windowsでは必要なモジュール等がインストールできないため \
　Windws Subsystem for Linux(WSL)をご利用ください \
\
最初に実行するためのPythonの仮想環境を作ります
```sh
$ python3 -m venv Copy_YourSelf_Running
```
python3-venvがインストールされていない場合は以下のコマンドでインストールしてください
```sh
$ sudo apt install python3-venv
```
仮想環境が作れたら以下のコマンドを利用し仮想環境を起動してください
```sh
$ .Copy_YourSelf_Running/bin/activate
```
形態素解析に必要なアプリケーションをインストールします
```sh
$ sudo apt install mecab libmecab-dev mecab-ipadic-utf8
```
形態素解析等に使うPythonモジュールをインストールします \
```sh
$ pip install mecab-python3 
```
形態素解析で使用する辞書をダウンロードします
```sh
$ git clone https://github.com/neologd/mecab-ipadic-neologd.git
```
ダウンロードした辞書をインストールします \
※ インストールするディレクトリ等をデフォルトから変える場合 \
Preprocessingファイルのanalysis.pyの内容を変更してください
```sh
$ cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -n -y
```
機械学習に用いられるPythonモジュールをインストールします。 \
対応GPUはNVIDIAとINTEL GPUの二つでこれらのGPUを使うにはCudaやOneAPI等の別のソフトが必要になるため \
インストール方法については以下のサイトをご覧ください。 \
[NVIDIA_GPU](https://www.tensorflow.org/install/pip?hl=ja) \
[INTEL_GPU](https://github.com/intel/intel-extension-for-tensorflow)
```sh 
$ pip install tensorflow==2.15 
```
その他必要なPythonモジュールをインストールします
```sh
$ pip install wget tqdm gensim flask websockets google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
おめでとうございます！これでインストールが完了しました！ \
楽しい生成AIライフを！
### Dockerによるインストール方法
コンテナアプリケーションであるDockerを使うことでもインストールは可能です。\
おそらくこっちの方が簡単で早いです \
レポジトリのディレクトリに移動し以下のコマンドを利用しDockerイメージを作成します
```sh
$ bash Docker環境構築\build.sh 使用機器(GPU、CPU等)
```
先ほど作ったイメージからコンテナを起動します。
```sh
$ bash Docker環境構築\run.sh 使用機器(GPU、CPU等)
```
Dockerコンテナ内で本プロジェクトをダウンロードします
```sh
$ git clone https://github.com/IT-F-09/Copy_YourSelf.git
```
以上でDockerでのインストールが完了しました！ \
Dockerの詳しい使い方は[こちら](https://docs.docker.jp/)を御覧ください
## 制作者情報
tagaiza2129
## 使用技術,言語等
<img src="https://img.shields.io/badge/-Python-555.svg?logo=python&style=flat">
<img src="https://img.shields.io/badge/-Github-555.svg?logo=Github&style=flat">
<img src="https://img.shields.io/badge/-Docker-555.svg?logo=Docker&style=flat">
<img src="https://img.shields.io/badge/-tensorflow-555.svg?logo=tensorflow&style=flat">
<img src="https://img.shields.io/badge/-websockets-555.svg?logo=tensorflow&style=flat">

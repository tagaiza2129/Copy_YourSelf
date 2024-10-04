# Copy_YourSelf
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ftagaiza2129%2FCopy_YourSelf.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Ftagaiza2129%2FCopy_YourSelf?ref=badge_shield)

<img src="https://img.shields.io/badge/Version-0.0.0-G"> <img src="https://img.shields.io/badge/Python_3.9-support-green"> <img src="https://img.shields.io/badge/Python_3.10-support-green"> <img src="https://img.shields.io/badge/Python_3.11-support-green"> \
## Copy_YourSelfとは

Googleが提供している機械学習のためのモジュールであるPyTorch等を活用し\
Seq2Seq等の手法で自然言語処理を行いユーザーの性格を模したChatAIを作るプロジェクトです
> [!NOTE]  
　このプロジェクトは現在制作中です。温かい目で御覧ください
## 使い方(How to Use)
### 起動方法
```sh
$ Copy_YourSelf
```
学習させる場合は上記のコマンドで学習させることができます
### 推論
```sh
$ python3 main.py 動かすモデルデータ -m Inference
```
学習したデータで推論するには上記のコマンドで推論することができます
### その他実行する際に使用できる引数等
``` sh
UserName@ComputerName:~$ copy_your_self -h
Usage: ./copy_your_self [options]

Options:
    -a, --server_address ADDRESS
                        HTMLサーバーのアドレスを指定します
    -p, --port PORT     webサーバーを立ち上げるポートを指定します
    -k, --open-key KEY  秘密鍵を使ってHTTPサーバーを構築します
    -d, --debug_directory DIRECTORY
                        デバッグ用のディレクトリを指定します
    -h, --help          このメニューを表示します
```
## インストール方法
> [!WARNING]
GPUのインストール手順などを間違えると　\
すごく面倒な事になるのでご注意ください \
\
これで何回OSごとリセットしたか...
### WSL、Ubuntu
> [!TIP]
純Windowsでは必要なモジュール等がインストールできないため \
Windws Subsystem for Linux(WSL)をご利用ください 

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
## 参考にした記事
### Qiita
[【GitHub】バッジを貼って README をおしゃれにする](https://qiita.com/narikkyo/items/98d7c4dbfccf52ec1840) 
### テキストコーパス
[京都大学テキストコーパス ](https://nlp.ist.i.kyoto-u.ac.jp/?%E4%BA%AC%E9%83%BD%E5%A4%A7%E5%AD%A6%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%B3%E3%83%BC%E3%83%91%E3%82%B9) \
[Wikipedia](https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
[JParaCrawl](https://www.kecl.ntt.co.jp/icl/lirg/jparacrawl/release/en/3.0/pretrained_models/en-ja/big.tar.gz)
## 使用技術,言語等
<img src="https://img.shields.io/badge/-Python-555.svg?logo=python&style=flat"> <img src="https://img.shields.io/badge/-Github-555.svg?logo=Github&style=flat"> <img src="https://img.shields.io/badge/-Docker-555.svg?logo=Docker&style=flat"> <img src="https://img.shields.io/badge/-tensorflow-555.svg?logo=tensorflow&style=flat">


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ftagaiza2129%2FCopy_YourSelf.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Ftagaiza2129%2FCopy_YourSelf?ref=badge_large)
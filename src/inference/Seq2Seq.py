import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from tqdm import tqdm
import pandas as pd
import torchtext
import dill
from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
#必要なグローバル変数の宣言
input_field:list
reply_field:list
n_h:int
n_vocab:int
n_emb:int
#対応デバイス(NVIDIA,INTEL,AMD,DirectML,Metal,CPU)
class Encoder(nn.Module):
    def __init__(self, n_h, n_vocab, n_emb, num_layers=1, bidirectional=False, dropout=0):
        super().__init__()
        self.n_h = n_h
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.dropout = dropout
        
        self.embedding = nn.Embedding(n_vocab, n_emb)
        self.embedding_dropout = nn.Dropout(self.dropout)

        self.gru = nn.GRU(
            input_size=n_emb,  #入力サイズ
            hidden_size=n_h,#隠れ層のサイズ（ニューロン数）
            batch_first=True,  #（バッチサイズ、時系列、入力数）
            num_layers=num_layers,
            bidirectional=bidirectional,
        )
    #順伝播の関数を定義
    def forward(self, x):
        index_pad = input_field.vocab.stoi["<pad>"] #"pad"のインデックス取得
        sentence_lengths = x.size()[1] - (x == index_pad).sum(dim=1)   #pad部分を引いて本来の文の長さを得る。

        y = self.embedding(x) #埋め込みベクトル化
        y = self.embedding_dropout(y)#過学習対策

        y = nn.utils.rnn.pack_padded_sequence(
            y,
            sentence_lengths.cpu(),
            batch_first=True,
            enforce_sorted=False
        )                              #rnnに入れるためにpackedsequence型にする。

        y, h = self.gru(y)  #encoderでの出力と隠れ層の値を取得

        y, _ = nn.utils.rnn.pad_packed_sequence(y, batch_first=True)   #テンソルに戻す                  
        if self.bidirectional:
                #会話データにおける最後の重みが大きくなってしまうため
            y = y[:, :, :self.n_h] + y[:, :, self.n_h:]#ここでは出力と隠れ層の値は双方向の時間の値を足したものになる。
            h = h[:self.num_layers] + h[self.num_layers:]

        return y,h

#Decoderクラスを作成します

class Decoder(nn.Module):
    def __init__(self, n_h, n_out, n_vocab, n_emb, num_layers=1, dropout=0):
        super().__init__()

        self.n_h = n_h
        self.n_out = n_out
        self.num_layers = num_layers
        self.dropout = dropout

        self.embedding = nn.Embedding(n_vocab, n_emb)
        self.embedding_dropout = nn.Dropout(self.dropout)

        self.gru = nn.GRU(
            input_size=n_emb,
            hidden_size=n_h,
            batch_first=True,
            num_layers=num_layers,
        )

        self.fc = nn.Linear(n_h*2, self.n_out)  #全結合層の導入



    def forward(self, x, h_encoder, y_encoder):
        y = self.embedding(x)  # 単語をベクトルに変換
        y = self.embedding_dropout(y)
        y, h = self.gru(y, h_encoder) #ここでは出力と最後の時刻の隠れ層の値が渡される

        #  Attention
        y_tr = torch.transpose(y, 1, 2)  # 次元1と次元2を入れ替える
        ed_mat = torch.bmm(y_encoder, y_tr)  # バッチごとに行列積
        attn_weight = F.softmax(ed_mat, dim=1)  # attention weightの計算
        attn_weight_tr = torch.transpose(attn_weight, 1, 2)  # 次元1と次元2を入れ替える
        context = torch.bmm(attn_weight_tr, y_encoder)  # コンテキストベクトルの計算
        y = torch.cat([y, context], dim=2)  # 出力とコンテキストベクトルの合流  
        y = self.fc(y)
        y = F.softmax(y, dim=2)

        return y, h

#seq2seqクラスを作成します

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, input_field:list, reply_field, device="cpu"):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        self.encoder.to(device)
        self.decoder.to(device)

    def forward(self, x_encoder, x_decoder): #順伝播メソッドの設定 訓練時につかう
        x_encoder = x_encoder.to(self.device)
        x_decoder = x_decoder.to(self.device)

        batch_size = x_decoder.shape[0]   #x_decoderは（バッチサイズ,時系列の数,ニューロン数）
        n_time = x_decoder.shape[1]
        y_encoder, h = self.encoder(x_encoder)

        y_decoder = torch.zeros(batch_size, n_time, self.decoder.n_out)   #バッチサイズ*時系列の数*出力数のすべて０のテンソル
        y_decoder = y_decoder.to(self.device)

        #教師強制と呼ばれる方法で各時刻の出力が次の入力に近くなるよう学習していきます。
        for t in range(0, n_time):  #各時刻で処理
            x = x_decoder[:, t:t+1]
            y, h = self.decoder(x, h, y_encoder)
            y_decoder[:, t:t+1, :] = y   #得られた出力ｙを各時刻ごとにy_encoderに格納

            return y_decoder

    def predict(self, x_encoder):    #予測に使用　文章の生成、評価するときに使う
        x_encoder = x_encoder.to(self.device)

        batch_size = x_encoder.shape[0]
        n_time = x_encoder.shape[1]
        y_encoder, h = self.encoder(x_encoder)

        y_decoder = torch.zeros(batch_size, n_time, dtype=torch.long)  #ここではint型を用いるためtorch.long
        y_decoder = y_decoder.to(self.device)

        y = torch.ones(batch_size, 1, dtype=torch.long) * input_field.vocab.stoi["<sos>"]  #予測用では各時刻で処理を行う必要がある。出力が次の入力になるから
        for t in range(0, n_time): 
            x = y     #ここでまえの出力を入力に
            x = x.to(self.device)
            y, h = self.decoder(x, h, y_encoder)
            y = y.argmax(2)   #yの中で最も大きい数値のインデックス得ることで最適な文章が生成
            y_decoder[:, t:t+1] = y

        return y_decoder

#評価関数を定義します
def evaluate(model, iterator,input_field:list,reply_field:list):
    model.eval()  # 評価モードにできる

    batch = next(iter(iterator))
    x = batch.inp_text
    y = model.predict(x)
    for i in range(x.size()[0]):
        inp_text = ""
        for j in range(x.size()[1]):
            word = input_field.vocab.itos[x[i][j]]
            if word=="<pad>":
                break
            inp_text += word

        rep_text = ""
        for j in range(y.size()[1]):
            word = reply_field.vocab.itos[y[i][j]]
            if word=="<eos>":
                break
            rep_text += word

        print("input:", inp_text)
        print("reply:", rep_text)
_Tokenizer = Tokenizer()
def tokenizer(text):
        return [token for token in _Tokenizer.tokenize(text, wakati=True)]
def Learning(inputs:list,outputs:list,device="cpu",batch_size=64,lr=0.001):
    global input_field,reply_field,n_h,n_vocab,n_emb
    inputs = [tokenizer(line) for line in inputs if line.strip()]
    outputs = [tokenizer(line) for line in outputs if line.strip()]

    dialogues_train, dialogues_test = train_test_split(list(zip(inputs, outputs)), shuffle=True, test_size=0.05)

    train_df = pd.DataFrame(dialogues_train, columns=["input_text", "reply_text"])
    test_df = pd.DataFrame(dialogues_test, columns=["input_text", "reply_text"])

    train_df.to_csv("train_data.csv", index=False)
    test_df.to_csv("test_data.csv", index=False)

    input_field = torchtext.data.Field(sequential=True, tokenize=tokenizer, batch_first=True, lower=True)
    reply_field = torchtext.data.Field(sequential=True, tokenize=tokenizer, init_token="<sos>", eos_token="<eos>", batch_first=True, lower=True)

    train_data, test_data = torchtext.data.TabularDataset.splits(path=".",train="train_data.csv",test="test_data.csv",format="csv",fields=[("input_text", input_field), ("reply_text", reply_field)])
    input_field.build_vocab(train_data, min_freq=3)
    reply_field.build_vocab(train_data, min_freq=3)
    torch.save(train_data.examples, "train_examples.pkl", pickle_module=dill)
    torch.save(test_data.examples, "test_examples.pkl", pickle_module=dill)
    torch.save(input_field, "input.pkl", pickle_module=dill)
    torch.save(reply_field, "reply.pkl", pickle_module=dill) 
    train_iterator = torchtext.data.Iterator(train_data,batch_size=batch_size,train=True)
    test_iterator = torchtext.data.Iterator(test_data,batch_size=batch_size,train=False,sort=False)
    n_h = 800   
    n_vocab_inp = len(input_field.vocab.itos)  #入力文の長さ
    n_vocab_rep = len(reply_field.vocab.itos)  #応答文の長さ
    n_emb = 300    #埋め込みベクトルの要素数
    n_out = n_vocab_rep     #出力の数
    early_stop_patience = 5  # 早期終了のタイミング（誤差の最小値が何回更新されなかったら終了か）
    num_layers = 1        #中間層の数
    bidirectional = True
    dropout = 0.1
    clip = 100 
    encoder = Encoder(n_h, n_vocab_inp, n_emb, num_layers, bidirectional, dropout=dropout)
    decoder = Decoder(n_h, n_out, n_vocab_rep, n_emb, num_layers, dropout=dropout)
    seq2seq = Seq2Seq(encoder, decoder, device=device, input_field=input_field, reply_field=reply_field)

    loss_fnc = nn.CrossEntropyLoss(ignore_index=reply_field.vocab.stoi["<pad>"])

    optimizer_enc = optim.Adam(seq2seq.parameters(), lr=lr)
    optimizer_dec = optim.Adam(seq2seq.parameters(), lr=lr)
    record_loss_train = []
    record_loss_test = []
    min_losss_test = 0.0

    # 学習
    for i in tqdm(range(1000)):     #1000epoch 学習
        seq2seq.train()

        loss_train = 0
        for j, batch in enumerate(train_iterator):
            inp, rep = batch.input_text, batch.reply_text
            x_enc = inp
            x_dec = rep[:, :-1]
            y_dec = seq2seq(x_enc, x_dec)

            t_dec = rep[:, 1:]
            t_dec = t_dec.to(device)
            loss = loss_fnc(
                y_dec.view(-1, y_dec.size()[2]),
                t_dec.reshape(-1)
                )
            loss_train += loss.item()
            optimizer_enc.zero_grad()
            optimizer_dec.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(encoder.parameters(), clip)
            nn.utils.clip_grad_norm_(decoder.parameters(), clip)
            optimizer_enc.step()
            optimizer_dec.step()

            if j%1000==0:
                print("batch:", str(j)+"/"+str(len(train_data)//batch_size+1), "loss:", loss.item())
        loss_train /= j+1
        record_loss_train.append(loss_train)

        # 評価モードにします
        seq2seq.eval()

        loss_test = 0
        for j, batch in enumerate(test_iterator):
            inp, rep = batch.inp_text, batch.rep_text
            x_enc = inp
            x_dec = torch.ones(rep.size(), dtype=torch.long) * reply_field.vocab.stoi["<sos>"]
            x_dec[:, 1:] = rep[:, :-1]
            y_dec = seq2seq(x_enc, x_dec)

            t_dec = rep.to(device)
            loss = loss_fnc(
                y_dec.view(-1, y_dec.size()[2]),
                t_dec.view(-1)
                )
            loss_test += loss.item()
        loss_test /= j+1
        record_loss_test.append(loss_test)

        if i%1 == 0:
            print("Epoch:", i, "Loss_Train:", loss_train, "Loss_Test:", loss_test)
            print()

        evaluate(seq2seq, test_iterator)

    #早期終了の設定をします
        latest_min = min(record_loss_test[-(early_stop_patience):])  # 直近の最小値
        if len(record_loss_test) >= early_stop_patience:
            if latest_min > min_loss_test:  # 直近で最小値が更新されていなければ
                print("Early stopping!")
                break
            min_loss_test = latest_min
        else:
            min_loss_test = latest_min
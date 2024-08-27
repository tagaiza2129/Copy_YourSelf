import tensorflow as tf
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding # type: ignore

embedding_dim = 256
lstm_units = 256

def Learning(vocab_size:int,input_sequences,target_sequences,epoch:int,device:str):  
    #GPUのメモリを使い切らないようにする
    gpus = tf.config.experimental.list_physical_devices('XPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
    #エンコードモデルの作成
    with tf.device(device):
        encoder_inputs = Input(shape=(None,))
        encoder_embedding = Embedding(vocab_size, embedding_dim)(encoder_inputs)
        encoder_lstm = LSTM(lstm_units, return_state=True)
        encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
        encoder_states = [state_h, state_c]
        decoder_inputs = Input(shape=(None,))
        decoder_embedding = Embedding(vocab_size, embedding_dim)(decoder_inputs)
        decoder_lstm = LSTM(lstm_units, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
        decoder_dense = Dense(vocab_size, activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)
        model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
        model.summary()
        target_sequences_shifted = target_sequences[:, 1:]
        model.fit([input_sequences, target_sequences[:, :-1]],target_sequences_shifted,batch_size=64,epochs=100)
        model.save("model.h5")
        # デコーダーモデルの定義
        decoder_state_input_h = Input(shape=(lstm_units,))
        decoder_state_input_c = Input(shape=(lstm_units,))
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_outputs, state_h, state_c = decoder_lstm(decoder_embedding, initial_state=decoder_states_inputs)
        decoder_states = [state_h, state_c]
        decoder_outputs = decoder_dense(decoder_outputs)
        decoder_model = Model([decoder_inputs] + decoder_states_inputs,[decoder_outputs] + decoder_states)
        decoder_model.save("decoder_model.h5")
        return [model,decoder_model]
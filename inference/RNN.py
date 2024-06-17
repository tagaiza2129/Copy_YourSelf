import tensorflow as tf

def train_text_generation_model(text_data,device:str,num_epochs=10, batch_size=64, sequence_length=100, embedding_dim=256, rnn_units=1024):
  # Preprocess the text data
  tokenizer = tf.keras.preprocessing.text.Tokenizer()
  tokenizer.fit_on_texts(text_data)
  total_words = len(tokenizer.word_index) + 1
  input_sequences = []
  for line in text_data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
      n_gram_sequence = token_list[:i+1]
      input_sequences.append(n_gram_sequence)
  max_sequence_length = max([len(seq) for seq in input_sequences])
  input_sequences = tf.keras.preprocessing.sequence.pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')
  predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
  label = tf.keras.utils.to_categorical(label, num_classes=total_words)

  # Build the model
  with tf.device(device):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(total_words, embedding_dim, input_length=max_sequence_length-1))
    model.add(tf.keras.layers.GRU(rnn_units, return_sequences=True))
    model.add(tf.keras.layers.GRU(rnn_units))
    model.add(tf.keras.layers.Dense(total_words, activation='softmax'))

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(predictors, label, epochs=num_epochs, batch_size=batch_size)

  return model
# Froked from https://github.com/tensorflow/docs-l10n/blob/master/site/ja/tutorials/images/transfer_learning.ipynb
import argparse
parser = argparse.ArgumentParser(description='TF multi-GPU training')
parser.add_argument('-wi', '--worker-index', choices=[0, 1], type=int, required=True,
                    help='Index of the worker, choose from [0,1] (required)')
parser.add_argument('-e', '--epochs', type=int, default=10,
                    help='Number of epochs, [10] default')
parser.add_argument('-bs', '--batch-size', type=int, default=1024,
                    help='Overall batch size, [1024] default')
parser.add_argument('-lr', '--learning-rate', type=float, default=0.001,
                    help='Learning rate, [0.001] default')
args = parser.parse_args()

import os
import tensorflow as tf
import time
from tensorflow.keras.preprocessing import image_dataset_from_directory # type: ignore
import platform
import time
import os
import json
def build_strategy(worker_index):
    tf_config = {
        'cluster': {
            'worker': ['localhost:12345', 'localhost:23456']
            },
        'task': {'type': 'worker', 'index': worker_index}
        }
    # Set environment variables for multi-worker communication
    os.environ['TF_CONFIG'] = json.dumps(tf_config)
    
    strategy = tf.distribute.MultiWorkerMirroredStrategy()    
    return strategy
start_time = time.time() 
_URL = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
path_to_zip = tf.keras.utils.get_file('cats_and_dogs.zip', origin=_URL, extract=True)
PATH = os.path.join(os.path.dirname(path_to_zip), 'cats_and_dogs_filtered')

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')

BATCH_SIZE = 16
IMG_SIZE = (160, 160)
#use_DEVICE=int(input("1.CPU\n2.GPU(NVIDIAのみ)\n3.GPU\n試験学習に利用する機器を選択してください:"))
use_DEVICE=1
if use_DEVICE==1:
    DEVICE = '/CPU:0'
elif use_DEVICE==2:
    DEVICE="/GPU:0"
else:
    DEVICE="/XPU:0"
with build_strategy(0).scope(DEVICE):
    train_dataset = image_dataset_from_directory(train_dir,
                                                shuffle=True,
                                                batch_size=BATCH_SIZE,
                                                image_size=IMG_SIZE)

    validation_dataset = image_dataset_from_directory(validation_dir,
                                                      shuffle=True,
                                                      batch_size=BATCH_SIZE,
                                                      image_size=IMG_SIZE)

    val_batches = tf.data.experimental.cardinality(validation_dataset)
    test_dataset = validation_dataset.take(val_batches // 5)
    validation_dataset = validation_dataset.skip(val_batches // 5)

    AUTOTUNE = tf.data.AUTOTUNE

    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

    # data_augmentation = tf.keras.Sequential([
    #   tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
    #   # tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
    # ])

    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    # Create the base model from the pre-trained model MobileNet V2
    IMG_SHAPE = IMG_SIZE + (3,)
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                  include_top=False,
                                                  weights='imagenet')

    image_batch, label_batch = next(iter(train_dataset))
    feature_batch = base_model(image_batch)
    print(feature_batch.shape)

    base_model.trainable = True

    # Let's take a look at the base model architecture
    base_model.summary()

    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    feature_batch_average = global_average_layer(feature_batch)
    print(feature_batch_average.shape)

    prediction_layer = tf.keras.layers.Dense(1)
    prediction_batch = prediction_layer(feature_batch_average)
    print(prediction_batch.shape)

    inputs = tf.keras.Input(shape=(160, 160, 3))
    # x = data_augmentation(inputs)
    x = preprocess_input(inputs)
    x = base_model(x, training=False)
    x = global_average_layer(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = prediction_layer(x)
    model = tf.keras.Model(inputs, outputs)

    base_learning_rate = 0.0001
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.summary()

    history = model.fit(train_dataset,
                        epochs=10,
                        validation_data=validation_dataset)

stop_time = time.time()
elapsed_time = stop_time - start_time 
print(f"計測時間:{int(elapsed_time/60)}分{int(elapsed_time%60)}秒")
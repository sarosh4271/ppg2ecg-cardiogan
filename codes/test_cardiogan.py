import numpy as np
import tensorflow as tf
import keras
import cv2
import sklearn.preprocessing as skp
import tflib
import module 
import preprocessing

keras.backend.set_floatx('float64')
tf.autograph.set_verbosity(0)

@tf.function
def sample_P2E(P, model):
    fake_ecg = model(P, training=False)
    return fake_ecg

def process_raw_data(sample_data):
    values_list = list(sample_data.values())
    int_values_list = [float(item) for item in values_list]
    x_ppg = int_values_list

    ecg_sampling_freq = 128
    ppg_sampling_freq = 128
    window_size = 4
    ecg_segment_size = ecg_sampling_freq*window_size
    ppg_segment_size = ppg_sampling_freq*window_size
    model_dir = 'weights'

    Gen_PPG2ECG = module.generator_attention()

    tflib.Checkpoint(dict(Gen_PPG2ECG=Gen_PPG2ECG), model_dir).restore()
    print("model loaded successfully")

    x_ppg = np.array(x_ppg)
    x_ppg = cv2.resize(x_ppg, (1,ppg_segment_size), interpolation = cv2.INTER_LINEAR)

    x_ppg = x_ppg.reshape(1, -1)
    x_ppg = preprocessing.filter_ppg(x_ppg, 128)

    x_ppg = skp.minmax_scale(x_ppg, (-1, 1), axis=1)

    x_ecg = sample_P2E(x_ppg, Gen_PPG2ECG)
    x_ecg = x_ecg.numpy()
    x_ecg = preprocessing.filter_ecg(x_ecg, 128)
    x_ppg = x_ppg.reshape(-1)
    x_ecg = x_ecg.reshape(-1)

    return [x_ecg,x_ppg]

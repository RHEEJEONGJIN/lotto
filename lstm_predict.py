# import json 
# import time
# import math
# import requests
import numpy as np
# import pandas as pd
# from tqdm import tqdm
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone

import tensorflow as tf
from keras import layers
from keras import models
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

# gpu 자동 할당
tf.config.set_soft_device_placement(True)
tf.debugging.set_log_device_placement(True)

from read_database import *


# 번호 뽑기
def gen_numbers_from_probability(nums_prob):

    ball_box = []

    for n in range(45):
        ball_count = int(nums_prob[n] * 100 + 1)
        ball = np.full((ball_count), n+1) #1부터 시작
        ball_box += list(ball)

    selected_balls = []

    while True:
        
        if len(selected_balls) == 6:
            break
        
        ball_index = np.random.randint(len(ball_box), size=1)[0]
        ball = ball_box[ball_index]

        if ball not in selected_balls:
            selected_balls.append(ball)

    return selected_balls


def predict_lstm():
    model = tf.keras.models.load_model("models/lstm.h5")

    xs = x_samples[-1].reshape(1, 1, 45)
    ys_pred = model.predict_on_batch(xs)

    numbers = gen_numbers_from_probability(ys_pred[0])
    numbers.sort()

    print('receive numbers', numbers)

    tf.keras.backend.clear_session()

    return numbers


if __name__ == "__main__":
    predict_lstm()
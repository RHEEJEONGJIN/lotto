import json 
import time
import math
import requests
import psycopg2
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from database_crud import CRUD


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


import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


### TODO: fill out the function below that transforms the input series and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series,window_size):
    # containers for input/output pairs
    X = []
    y = []
    # k .- Beggining of X series, 
    for k in range(len(series) - window_size):
        #Fill X with series element from k to k+window_size
        X.append(series[k:(k+window_size)])
        #Fill X with series element  k+window_size
        y.append(series[k+window_size])
        
    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)
    
    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(step_size, window_size):
    model=Sequential()
    # 1 Layer .- LSTM, 5 hidden units 
    model.add(LSTM(5,input_shape = (window_size,step_size)))
    # 1 Layer .- Dense, 1 units 
    model.add(Dense(1))
    return model

### TODO: list all unique characters in the text and remove any non-english ones
def clean_text(text):
    # find all unique characters in the text
    set(text)

    # remove as many non-english characters and character sequences as you can 
    text = text.replace('é',' ')
    text = text.replace('â',' ')
    text = text.replace('à',' ')
    text = text.replace('è',' ')
    text = text.replace('"',' ')
    text = text.replace('$',' ')
    text = text.replace('%',' ')
    text = text.replace('&',' ')
    text = text.replace('(',' ')
    text = text.replace(')',' ')
    text = text.replace('*',' ')
    text = text.replace('-',' ')
    text = text.replace('/',' ')
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text,window_size,step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    #Number of windows to create
    n_windows=int((len(text) - window_size)/ step_size)
    for j in range(n_windows) :
        # k .- Start index
        k= j * step_size
        inputs.append(text[k:(k+window_size)])
        outputs.append(text[k+window_size])

    return inputs,outputs

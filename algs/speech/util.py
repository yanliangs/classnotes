import pandas as pd
import numpy as np
import tensorflow as tf
import scipy.io.wavfile, zipfile
import io, time, os, random, re

#train_dir = '/home/burak/Downloads/voice_cmd_medium'
train_dir = '/home/burak/Downloads/train'
labels = ['up','down','yes','no']

fs = 16000
all_train_files = []
all_train_files2 = []

for d, r, f in os.walk(train_dir):
    for filename in f:
        all_train_files.append(os.path.join(d,filename))
for x in all_train_files:
    if ".wav" in x: 
       label = re.findall(".*/(.*?)/.*?.wav",x)[0]
       if label in labels: all_train_files2.append(x)

np.random.seed(0)
       
all_train_files2 = np.array(all_train_files2)
idx = np.random.permutation(np.arange(len(all_train_files2)))
N = float(len(idx))
tidx = idx[0:int(N*0.9)]
vidx = idx[int(N*0.9):]
train_files = all_train_files2[tidx]
val_files = all_train_files2[vidx]

np.random.seed()

print 'train', len(train_files), 'val', len(val_files)

def adj_volume(vec):
    vol_multiplier = np.mean(np.abs(vec)) / 500.
    if vol_multiplier == 0: return vec
    vnew = vec.astype(float) / vol_multiplier
    return vnew

def get_minibatch(batch_size, validation=False):
    files = train_files
    bs = batch_size
    if validation:
        files = val_files
        bs = len(val_files)
    res = np.zeros((bs, fs))
    y = np.zeros((bs,len(labels) ))
    for i in range(bs):
    	f = random.choice(files)
	wav = io.BytesIO(open(f).read())
	v = scipy.io.wavfile.read(wav)
	res[i, 0:len(v[1])] = adj_volume(v[1])
        label = re.findall(".*/(.*?)/.*?.wav",f)[0]
	y[i, labels.index(label)] = 1.0

    return res, y

    

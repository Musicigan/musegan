import os
import glob
import pretty_midi
import numpy as np

def split(start, end, num_of_elem):
    step = (end - start)/num_of_elem
    arr = np.empty(num_of_elem)
    arr[0] = start
    for i in range(1, num_of_elem):
        arr[i] = arr[i-1] + step
    return arr

path = 'C:/Users/admin/PycharmProjects/StatML-Project/clean_midi_training'

i = 1
j = 1
myList = []
fin_arr1 = []
np.asarray(fin_arr1)
for filename in os.listdir(path):
    path1 = os.path.join(path, filename)
    print('Folder: ')
    print(i)
    f = 0
    for filename1 in glob.glob(os.path.join(path1, '*.mid')):
        print(filename1)
        pm = pretty_midi.PrettyMIDI(filename1)
        bars_onset1 = pm.get_downbeats()
        bars_onset = np.append(bars_onset1, pm.get_end_time())
        print(len(bars_onset))
        flag = 0
        time_onset = np.zeros((len(bars_onset) - 1, 16))
        if len(bars_onset) > 100:
            flag = 1
            myList.append([os.listdir(path1)[f], len(bars_onset) - 1])
            fin_arr = np.zeros((len(bars_onset) - 1, 16, 128))
            for k in range(0, len(bars_onset) - 1):
                time_onset[k, :] = split(bars_onset[k], bars_onset[k + 1], 16)
                fin_arr[k, :, :] = pm.instruments[0].get_piano_roll(1000, time_onset[k, :]).T
            fin_arr = fin_arr[0:100, :, :]
            fin_arr = np.expand_dims(fin_arr, axis=3)
        if flag == 1:
            fin_arr1.append(fin_arr)
        print(flag)
        print('Midi File: ')
        print(j)
        j = j + 1
        f = f + 1
    i = i+1

print(np.asarray(fin_arr1).shape)

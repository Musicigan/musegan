import os
import numpy as np


INPUT_BASE_DIR = '/media/ashar/Data/lmd_genre/lpd_5/numpy_midi/'
genre_binarylist = [00, 01, 10, 11]


def data_loader(INPUT_BASE_DIR, genre_binarylist):
    full_X = np.array([])
    full_prev_X = np.array([])
    full_label_set = np.array([])

    for genre in genre_binarylist:
        final_out_path = os.path.join(INPUT_BASE_DIR, str(genre))
        if not os.path.exists(final_out_path):
            os.makedirs(final_out_path)
        npy_arr = np.load(final_out_path + '/midi_bars.npy')
        full_X = np.concatenate([full_X, npy_arr], axis=0) if full_X.size else npy_arr

    return full_X

check = 1
    # prev_npy[]



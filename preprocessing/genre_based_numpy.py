import os
import glob
import scipy.sparse
import numpy as np
import pickle
import pandas as pd

LAST_BAR_MODE = 'remove'
MAP_DIR = '/home/ashar/Downloads/'
OUTPUT_BASE_DIR = '/media/ashar/Data/lmd_genre/lpd_5/numpy_musegan_phr/'
map_file_name = MAP_DIR + 'cleansed_genremap.csv'
genre_binarylist = [00, 01, 10, 11]


def csc_to_array(csc, track_id):
    # print csc['pianoroll_%d_csc_shape' % track_id]
    return scipy.sparse.csc_matrix((csc['pianoroll_%d_csc_data' % track_id], csc['pianoroll_%d_csc_indices' % track_id],
                                    csc['pianoroll_%d_csc_indptr' % track_id]), shape=csc['pianoroll_%d_csc_shape' % track_id]).toarray()


def get_bar_piano_roll(piano_roll, bar_size=96, notespan=84, num_tracks = 5):
    if int(piano_roll.shape[0] % bar_size) is not 0:
        if LAST_BAR_MODE == 'fill':
            piano_roll = np.concatenate((piano_roll, np.zeros((bar_size-piano_roll.shape[0] % bar_size, notespan, num_tracks ))), axis=0)
        elif LAST_BAR_MODE == 'remove':
            piano_roll = np.delete(piano_roll,  np.s_[-int(piano_roll.shape[0] % bar_size):], axis=0)
    piano_roll = piano_roll.reshape(-1, bar_size, notespan, num_tracks)
    return piano_roll


csv_file = pd.read_csv(map_file_name)

df_map = pd.DataFrame(csv_file)
df_genre_idx = df_map.set_index("GenreBinary", drop=False)

for genre in genre_binarylist:
    genre_numpy = np.array([])
    song_list = df_genre_idx.loc[genre, "NpzPath"].tolist()
    print 'This is genre--> ' + str(genre)

    for song_path in song_list:
        npz_array = np.load(song_path)

        flag_cleaned = True
        # Dimension Sanity Check for uniform numpy generation
        track_shape = npz_array['pianoroll_0_csc_shape'][0]
        for k in range(5):
            if not npz_array['pianoroll_%d_csc_shape' % k][0] == track_shape:
                flag_cleaned = False

        if flag_cleaned:
            npy_array = np.array([])
            for j in range(5):
                mono_npy = np.expand_dims(csc_to_array(npz_array, j), axis=2)
                npy_array = np.concatenate([npy_array, mono_npy], axis=2) if npy_array.size else mono_npy

            npy_musegan_array = npy_array[:, 8:84+8, :]  # np.expand_dims(, axis=2)
            bar_npy_musegan_array = get_bar_piano_roll(npy_musegan_array, bar_size=384, notespan=84, num_tracks=5)
            genre_numpy = np.concatenate([genre_numpy, bar_npy_musegan_array], axis=0) if genre_numpy.size else bar_npy_musegan_array

            if genre_numpy.shape[0] >= 2000:
                # print 'Max Limit Reached'
                # genre_labels = np.zeros((genre_numpy.shape[0], 4))
                #
                # genre_labels[:, 0:4] = [0, 0, 0, 1]
                # if genre == 1:
                #     genre_labels[:, 0:4] = [0, 0, 1, 0]
                # elif genre == 10:
                #     genre_labels[:, 0:4] = [0, 1, 0, 0]
                # elif genre == 11:
                #     genre_labels[:, 0:4] = [1, 0, 0, 0]
                #
                # final_out_path = os.path.join(OUTPUT_BASE_DIR, str(genre))
                # if not os.path.exists(final_out_path):
                #     os.makedirs(final_out_path)
                # np.save(final_out_path + '/midi_bars.npy', genre_numpy)
                # np.save(final_out_path + '/genre_label.npy', genre_labels)
                #
                # print 'The output shape is ' + str(genre_numpy.shape)
                # print 'The label shape is ' + str(genre_labels.shape)
                break

    genre_labels = np.zeros((genre_numpy.shape[0], 4))

    genre_labels[:, 0:4] = [0, 0, 0, 1]
    if genre == 1:
        genre_labels[:, 0:4] = [0, 0, 1, 0]
    elif genre == 10:
        genre_labels[:, 0:4] = [0, 1, 0, 0]
    elif genre == 11:
        genre_labels[:, 0:4] = [1, 0, 0, 0]

    final_out_path = os.path.join(OUTPUT_BASE_DIR, str(genre))
    if not os.path.exists(final_out_path):
        os.makedirs(final_out_path)
    np.save(final_out_path + '/midi_bars.npy', genre_numpy)
    np.save(final_out_path + '/genre_label.npy', genre_labels)

    print 'The output shape is ' + str(genre_numpy.shape)
    print 'The label shape is ' + str(genre_labels.shape)




check = 1


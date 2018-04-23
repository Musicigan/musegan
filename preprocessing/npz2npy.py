import os
import glob
import scipy.sparse
import numpy as np
import pickle

LAST_BAR_MODE = 'remove'

def csc_to_array(csc, track_id):
    print csc['pianoroll_%d_csc_shape' % track_id]
    return scipy.sparse.csc_matrix((csc['pianoroll_%d_csc_data' % track_id], csc['pianoroll_%d_csc_indices' % track_id],
                                    csc['pianoroll_%d_csc_indptr' % track_id]), shape=csc['pianoroll_%d_csc_shape' % track_id]).toarray()


def get_bar_piano_roll(piano_roll, bar_size=96, notespan=84):
    if int(piano_roll.shape[0] % bar_size) is not 0:
        piano_roll = np.delete(piano_roll,  np.s_[-int(piano_roll.shape[0] % bar_size):], axis=0)
    piano_roll = piano_roll.reshape(-1, bar_size, notespan)
    return piano_roll

# path = '/home/ashar/Documents/ece6254/project/data/lmd_genre/lpd_5/cleansed/'
path = '/media/ashar/Data/lmd_genre/lpd_5/cleansed'

for file_1 in os.listdir(path):
    path_1 = os.path.join(path, file_1)
    for file_2 in os.listdir(path_1):
        path_2 = os.path.join(path_1, file_2)
        for file_3 in os.listdir(path_2):
            path_3 = os.path.join(path_2, file_3)
            full_path = os.path.join(path, path_1, path_2, path_3)
            for track in os.listdir(path_3):
                # if os.path.exists(os.path.join(full_path, track, '*.npz')):
                for name in glob.glob(os.path.join(full_path, track, '*.npz')):
                    npz_array = np.load(name)

                    musegan_path = os.path.join(full_path, track, 'musegan_track')
                    midinet_path = os.path.join(full_path, track, 'midinet_track')

                    if not os.path.exists(musegan_path):
                        os.makedirs(musegan_path)
                    if not os.path.exists(midinet_path):
                        os.makedirs(midinet_path)

                    npy_name = name.split('/')[-1].split('.')[0]

                    musegan_full_name = os.path.join(musegan_path, npy_name) + '.npy'
                    midinet_full_name = os.path.join(midinet_path, npy_name) + '.npy'

                    if (not os.path.exists(musegan_full_name)) or (not os.path.exists(midinet_full_name)):

                        flag_cleaned = True
                        # Dimension Sanity Check
                        track_shape = npz_array['pianoroll_0_csc_shape'][0]
                        for k in range(5):
                            if not npz_array['pianoroll_%d_csc_shape' % k][0] == track_shape:
                                flag_cleaned = False

                        if flag_cleaned:
                            npy_array = np.array([])
                            for j in range(5):
                                mono_npy = np.expand_dims(csc_to_array(npz_array, j), axis=2)
                                npy_array = np.concatenate([npy_array, mono_npy], axis=2) if npy_array.size else mono_npy

                            # Truncating for getting C1 - C8 required in the musegan architecture
                            npy_musegan_array = npy_array[:, 8:92, :]

                            outfile1 = open(midinet_full_name, 'w+b')
                            pickle.dump(npy_array.tolist(), outfile1)
                            outfile1.close()

                            infile1 = open(midinet_full_name, 'r+b')
                            file1 = pickle.load(infile1)  # This is a list
                            infile1.close()

                            numpyArray = np.array(file1)

                            check = 1

                            # Create new directories for storing tracks
                            #
                            # np.save(midinet_full_name, npy_array)
                            # np.save(musegan_full_name, npy_musegan_array)

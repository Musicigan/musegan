# File generates lookup Csv from the available cleansed midi files

# Also Functionality to extract only genre-based files from the lakh-midi matched Dataset.


import os
import glob
import pandas as pd
import numpy as np
import json
import shutil

# path = '/home/ashar/Documents/ece6254/project/data/lmd_matched/'

path = '/home/ashar/Documents/ece6254/project/data/lpd_5/cleansed/'
genre_matched_path = '/home/ashar/Documents/ece6254/project/data/lmd_matched_genre/'
genremap_dir = '/home/ashar/Downloads/'

genre_binary_map = {'Country': '00', 'Pop_Rock': '01', 'Electronic': '10', 'RnB': '10', 'Jazz': '11', 'Blues': '11'}

matched_tracklist_json = []
json_file = open(genremap_dir + 'match_scores.json').read()
matched_json = json.loads(json_file)
matched_tracklist_json = matched_json.keys()

genres_map = pd.read_csv(genremap_dir + 'genremap.csv')
df_genre = pd.DataFrame(genres_map)
df_genre.set_index('TrackID')
genre_tracklist = df_genre.TrackID.T.tolist()
# print len(genre_tracklist)

matched_tracks = list(set(genre_tracklist).intersection(matched_tracklist_json))
print len(matched_tracks)

df_filepath = pd.DataFrame(columns=['TrackID', 'NpzPath', 'Genre', 'GenreBinary'])
df_track_idx = df_genre.set_index("TrackID", drop=False)


for file_1 in os.listdir(path):
    path_1 = os.path.join(path, file_1)
    for file_2 in os.listdir(path_1):
        path_2 = os.path.join(path_1, file_2)
        for file_3 in os.listdir(path_2):
            path_3 = os.path.join(path_2, file_3)
            full_path = os.path.join(path, path_1, path_2, path_3)
            newparts = full_path.split("/")[-4:]
            # new_final_path = os.path.join(genre_matched_path, newparts[1], newparts[2], newparts[3])
            # if not os.path.exists(new_final_path):
            #     os.makedirs(new_final_path)
            for track in os.listdir(path_3):
                if any(track in s for s in matched_tracks):
                    for name in glob.glob(os.path.join(full_path, track, '*.npz')):
                        try:
                            df_filepath = df_filepath.append({'TrackID': track, 'NpzPath': name,
                                                          'Genre': df_track_idx.loc[track, "Genre"],
                                                          'GenreBinary': genre_binary_map[df_track_idx.loc[track, "Genre"]]}, ignore_index=True)
                        except KeyError:
                            print 'This Genre is not Required!'
                    print 'Found the track!'
cross_check = 1
                    # Store only the relevant data
                    # shutil.copytree(os.path.join(full_path, track) , os.path.join(new_final_path, track))

df_filepath.to_csv(genremap_dir + 'cleansed_genremap.csv')


#
# def str_modify(str):   # Remove all characters and spaces except alphabets in input string
#     str = str.replace(" ","")
#     str = str.lower()
#     validletters = "abcdefghijklmnopqlmnoqrstuvwxyz0123456789"
#     newString = ''
#     newString = ''.join([char for char in str if char in validletters])
#     return newString
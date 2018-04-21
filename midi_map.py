import pandas as pd
import os
import glob

midi_dir = '/home/ashar/Documents/ece6254/project/data/clean_midi'
artist_list = []

for filename in os.listdir(midi_dir):
    path1 = os.path.join(midi_dir, filename)
    for filename1 in glob.glob(os.path.join(path1, '*.mid')):
        artist_name = filename1.split('/')[-2]
        artist_list.append(artist_name)

df_artist = pd.DataFrame(artist_list)
# df_artist = df_artist.drop_duplicates()
print df_artist.head()
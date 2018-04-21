# import pandas as pd
# import os
#
#
dir = '/home/ashar/Documents/StatML/'
# filename_original = dir + 'track_songs.csv'
# filename_genremap = dir + 'track_genres.json'
#
filename_output = dir + 'genremap.csv'
#
# orig = pd.read_csv(filename_original)
# df_orig = pd.DataFrame(orig)
#
# genre = pd.read_json(filename_genremap)
# df_genre = pd.DataFrame(genre)
#
# final_map = pd.merge(df_orig, df_genre, on='TrackID', how='inner')
#
# # final_map.to_csv(filename_output)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv(filename_output, encoding='utf-8')
# print df.head()

sns.countplot(df.Genre)
plt.xlabel('Genre')
plt.title('Genre distribution')
plt.grid()
plt.show()


import matplotlib
import matplotlib.pyplot as plt
import json
import sqlite3
import os
import re
import numpy as np
matplotlib.axes.Axes.pie
matplotlib.pyplot.pie


song_names = []
artist_names = []
spotify_popularity = []
youtube_popularity = []
artist_view_percentage = []
artist_spotify_percentage = []

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'spotify.db')
cur = conn.cursor()

cur.execute("SELECT artist, percent_spotifytop100, percent_youtubeviews FROM Artists")
x = cur.fetchall()
artist_name = []
spotify_score = []
youtube_score = []
for artist, spotify, youtube in x:
    artist_name.append(artist)
    spotify_score.append(spotify)
    youtube_score.append(youtube)


labels = tuple(artist_name)
sizes = youtube_score

patches, texts = plt.pie(sizes, startangle=90, radius=1.2)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, sizes)]
sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes), key=lambda x: x[2], reverse=True))
plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.1, 1.), fontsize=8)
plt.savefig('piechart.png', bbox_inches='tight')
plt.show()

cur.execute("SELECT song, spotify_popularity_score, youtube_popularity_score FROM Songs")
y = cur.fetchall()
song_name = []
spotify_pop = []
youtube_pop = []
for song, spotify, youtube in y:
    song_name.append(song)
    spotify_pop.append(spotify)
    youtube_pop.append(youtube)

plt.scatter(youtube_pop, spotify_pop)
plt.title('Correlation between Popularity of Songs on YouTube \nand Popularity of Corresponding Music Videos on Spotify')
plt.xlabel('YouTube Popularity')
plt.ylabel('Spotify Popularity')
plt.show()
# explode = (0, 0.1, 0, 0)
# only "explode" the 2nd slice (i.e. 'Hogs')
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)ax1.axis('equal')

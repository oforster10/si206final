import matplotlib
import matplotlib.pyplot as plt
import json
import sqlite3
import pandas
import os
import re
import numpy as np
matplotlib.axes.Axes.pie
matplotlib.pyplot.pie

# Connect to database and set cur and conn.
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'music.db')
cur = conn.cursor()

#Fetch data from table and assigning to variables.
cur.execute("SELECT artist, percent_youtubeviews FROM ArtistsY")
x = cur.fetchall()
artist_name = []
youtube_score = []
for artist, youtube in x:
    artist_name.append(artist)
    youtube_score.append(youtube)

#Creates YouTube pie chart, showing the percent of YouTube music video views each artist has for their songs on the top 100 Spotify list. 
labels = tuple(artist_name)
sizes = youtube_score

patches, texts = plt.pie(sizes, startangle=90, radius=1.2)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, sizes)]
sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes), key=lambda x: x[2], reverse=True))
plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.1, 1.), fontsize=8)
plt.savefig('piechart.png', bbox_inches='tight')
plt.title("Artist's percent of total YouTube music video views for the top 100 Spotify songs")
plt.show()

#Fetch data from table and assigning to variables. 
cur.execute("SELECT song, spotify_popularity_score, youtube_popularity_score FROM Songs")
y = cur.fetchall()
song_name = []
spotify_pop = []
youtube_pop = []
for song, spotify, youtube in y:
    song_name.append(song)
    spotify_pop.append(spotify)
    youtube_pop.append(youtube)

#Creates a scatterplot showing the correlation (or lack thereof) between Spotify popularity score to Youtube popularity score. 
plt.scatter(youtube_pop, spotify_pop)
plt.title('Correlation between Popularity of Songs on YouTube \nand Popularity of Corresponding Music Videos on Spotify')
plt.xlabel('YouTube Popularity')
plt.ylabel('Spotify Popularity')
plt.show()

#Fetch data from table and assigning to variables.
cur.execute("SELECT artist, percent_spotifytop100 FROM ArtistsS")
x = cur.fetchall()
artist_name = []
spotify_score = []
for artist, spotify in x:
    artist_name.append(artist)
    spotify_score.append(spotify)

#Creates Spotify pie chart, showing the percent of top 100 songs an artist has on Spotify. 
labels = tuple(artist_name)
sizes = spotify_score

patches, texts = plt.pie(sizes, startangle=90, radius=1.2)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, sizes)]
sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes), key=lambda x: x[2], reverse=True))
plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.1, 1.), fontsize=8)
plt.savefig('piechart.png', bbox_inches='tight')
plt.title('Artist Percent of Top 100 Songs on Spotify')
plt.show()

#
df = pandas.DataFrame(dict(graph=artist_name,
                           n=spotify_score, m=youtube_score)) 
ind = np.arange(len(df))
width = 0.2

fig, ax = plt.subplots()
ax.barh(ind, df.m, width, color='red', label='YouTube Popularity Percent of Total Streams')
ax.barh(ind + width, df.n, width, color='green', label='Spotify Popularity Percent of Total Songs')

ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
ax.legend()
plt.tick_params(axis = "y", labelsize = 6)
plt.title('Artist Popularity Percent on YouTube and Spotify')
plt.xlabel('Popularity Percentage (out of 100)')
plt.show()

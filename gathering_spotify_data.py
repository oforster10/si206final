import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
import requests
import re
import os
import csv
import sqlite3
import json

sp = spotipy.Spotify()
cid = 'd1ffc95abeed474dbdcbf9c8b076075f'
secret = 'f7c5e4b25b5d4b1fa26ef7089d57acfa'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

def setUpDatabase(db_name):
    """Takes the name of a database, a string, as an input. Returns the cursor and connection to the database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_spotify_most_streamed():
    """No inputs. Returns a list of tuples in the format (song, artist, popularity) using playlist 'Top 100 Most Streamed Songs on Spotify'."""
    playlist_id = "5ABHKGoOzxkaa28ttQV9sE"
    playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
    tracks = playlist['tracks']['items']
    tracks_info = []
    for item in tracks:
        title = item['track']['name']
        artist = item['track']['album']['artists'][0]['name']
        popularity = int(item['track']['popularity'])
        info = title, artist, popularity
        tracks_info.append(info)
    print(tracks_info)
    return tracks_info

def set_up_tables(cur, conn):
    """ Takes the database cursor and connection as inputs. Returns nothing. Creates two tables, one that will hold artists and their artist_ids, and another that holds the top 100 songs, along with their artist_ids and weeks on chart."""
    #ask if we need to create both tables, unsure about SongIds table
    #cur.execute("CREATE TABLE IF NOT EXISTS SongIds (song_id INTEGER PRIMARY KEY, song TEXT, artist TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (song_id INTEGER PRIMARY KEY, song TEXT, artist TEXT, popularity INTEGER)")
    conn.commit()

def fill_spotify_table(cur, conn):
# """Takes the database cursor and connection as inputs. Does not return anything. Fills in the Spotify table with songs and their artist_ids and the number of streams each song has. The creation_id is each artist's unique identification number."""
    #Calls get_spotify_top_tracks_of_2020() to get the songs off of the Spotify "Top Tracks of 2020 USA" playlist.
    most_streamed = get_spotify_most_streamed()

    cur.execute("SELECT song FROM Spotify")
    song_list = cur.fetchall()
    x = 1
    count = len(song_list)
    for x in range(25):
        x = count
        song_id = count + 1
        song = most_streamed[count][0]
        artist = most_streamed[count][1]
        popularity = most_streamed[count][2]
        x += 1
        cur.execute("INSERT OR IGNORE INTO Spotify (song_id, song, artist, popularity) VALUES (?, ?, ?, ?)", (song_id, song, artist, popularity))
        count += 1
   
    conn.commit()

get_spotify_most_streamed()

cur, conn = setUpDatabase('music.db')
set_up_tables(cur, conn)
fill_spotify_table(cur, conn)
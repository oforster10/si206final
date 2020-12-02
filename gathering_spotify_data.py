import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import re
import os
import csv
import sqlite3
import json

cid = 'd1ffc95abeed474dbdcbf9c8b076075f'
secret = 'f7c5e4b25b5d4b1fa26ef7089d57acfa'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#not sure about the following line
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def setUpDatabase(db_name):
    """Takes the name of a database, a string, as an input. Returns the cursor and connection to the database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_spotify_top_tracks_of_2020():
    """No inputs. Returns a list of tuples in the format (song, artist) using playlist 'Top Tracks of 2020 USA'."""

def get_song_popularity(song, artist):
    """Take song and artist from the previous function as inputs. Go to artist's page on Spotify, find the matching song title, and return a tuple of the (song, artist, number_of_streams)."""

def set_up_tables(cur, conn):
    """ Takes the database cursor and connection as inputs. Returns nothing. Creates two tables, one that will hold artists and their artist_ids, and another that holds the top 100 songs, along with their artist_ids and weeks on chart."""
    #ask if we need to create both tables, unsure about SongIds table
    #cur.execute("CREATE TABLE IF NOT EXISTS SongIds (song_id INTEGER PRIMARY KEY, song TEXT, artist TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (creation_id INTEGER PRIMARY KEY, artist TEXT, song_id INTEGER, number_of_streams INTEGER)")
    conn.commit()

def fill_spotify_table(cur, conn):
"""Takes the database cursor and connection as inputs. Does not return anything. Fills in the Spotify table with songs and their artist_ids and the number of streams each song has. The creation_id is each artist's unique identification number."""
    #Calls get_spotify_top_tracks_of_2020() to get the songs off of the Spotify "Top Tracks of 2020 USA" playlist.
    song, artist = get_spotify_top_tracks_of_2020()
    spotify_list = get_song_popularity(song, artist)
    #Selects songs that are already in the Spotify table and puts them in a list so that we know which songs should not be repeated.
    cur.execute('SELECT song FROM SongIds')
    song_list = cur.fetchall()
    x = 1
    count = len(song_list)
    #Adds songs to the Spotify list that are not already in it, 25 at a time.
    for x in range(25):
        x = count
        #The creation_id is the unique id that identifies a song.
        creation_id = count + 1
        song = spotify_list[count][0]
        streams = spotify_list[count][2]
        x = x + 1
        #In order to save storage space, we are adding in ArtistIds (integers) instead of artists.
        cur.execute('SELECT artist_id, artist FROM ArtistIds')
        artist_ids = cur.fetchall()
        for artist_tup in artist_ids:
            if artist_tup[1] == top_100_list[count][1]:
                artist = artist_tup[0]
                cur.execute("INSERT OR IGNORE INTO Hot100 (creation_id, song, artist_id, weeks_on_chart) VALUES (?, ?, ?, ?)", (creation_id, song, int(artist), weeks))
        count = count + 1
    conn.commit()
import json
import sqlite3
import os
import re

def join_tables(cur, conn):
    """Takes in the database cursor and connection as inputs. Returns a list of tuples in the format (song, artist) where the artist ids are the same."""
    cur.execute('SELECT Spotify.artist, Spotify.popularity, YouTubeViews.views, Spotify.song FROM Spotify LEFT JOIN YouTubeViews ON Spotify.song = YouTubeViews.song')
    results = cur.fetchall()
    conn.commit()
    return results

def artist_percent_of_top_100_songs(cur, conn):
    list_of_tups = join_tables(cur, conn)
    print(list_of_tups)
    artist_dict = {}
    for song in list_of_tups:
        artist = song[0]
        artist_dict[artist] = artist_dict.get(artist, 0) + 1
     
    for artist_name in artist_dict:
        total_songs = artist_dict[artist_name]
        # cur.execute("INSERT INTO ArtistsS VALUES (?, ?)", (artist_name, total_songs))
        # conn.commit()
    return artist_dict
    
    
def artist_percent_of_total_views(cur, conn):
    list_of_tups = join_tables(cur, conn)
    views_dict = {}
    for song in list_of_tups:
        artist = song[0]
        views = song[2]
        views_dict[artist] = views_dict.get(artist, 0) + views
    
    total_views = 0
    for artist in views_dict:
        total_views += views_dict[artist]
    
    percent_views = 0
    artist_percent_views = {}
    for artist_name in views_dict:
        print(artist_name)
        percent_views = views_dict[artist_name] / total_views * 100
        percent_views_float = "{:.2f}".format(percent_views)
        artist_percent_views[artist_name] = percent_views_float
        # cur.execute("INSERT INTO ArtistsY (artist, percent_youtubeviews) VALUES (?, ?)", (artist, percent_views_float))
        # conn.commit()
    return artist_percent_views

def song_percent_of_top_song_views(cur, conn):
    list_of_tups = join_tables(cur, conn)
    sorted_list = sorted(list_of_tups, key = lambda x: x[2], reverse = True)
    top_song_views = sorted_list[0][2]
    youtube_popularity = 0
    song_popularity_dict = {}
    for song in list_of_tups:
        spotify_popularity = song[1]
        views = song[2]
        song_name = song[3]
        youtube_popularity = "{:.2f}".format(views / top_song_views * 100)
        popularity_scores = (spotify_popularity, float(youtube_popularity))
        # cur.execute("INSERT INTO Songs (song, spotify_popularity_score, youtube_popularity_score) VALUES (?, ?, ?)", (song_name, spotify_popularity, youtube_popularity))
        # conn.commit()
        song_popularity_dict[song_name] = popularity_scores
    return song_popularity_dict


def write_data_to_file(filename, cur, conn):
    """Takes in a filename (string) as an input and the database cursor/connection. Returns nothing. Creates a file and writes return value of the function average_popularity() to the file. """

    path = os.path.dirname(os.path.abspath(__file__)) + os.sep

    outFile = open(path + filename, "w")
    
    outFile.write("Popularity Scores of Songs on YouTube and Spotify\n")
    outFile.write("================================================================================================\n\n")
    output1 = (song_percent_of_top_song_views(cur, conn))
    for song in output1:
        spotify_pop = str(output1[song][0])
        outFile.write("For " + song + ", the Spotify popularity score is " + spotify_pop + " and the popularity for the corresponding song's music video on YouTube is " + str(output1[song][1]) + ".\n\n")
   
    outFile.write("================================================================================================\n")
    outFile.write("Artist Percent of YouTube Music Video Views Corresponding to their Top 100 Spotify Songs\n")
    outFile.write("================================================================================================\n")
    output2 = artist_percent_of_total_views(cur, conn)
    for artist in output2:
        outFile.write("Out of the top 100 Spotify songs, " + artist + "'s corresponding music videos have " + str(output2[artist]) + " percent of the total YouTube views for said Spotify songs." + "\n\n")
    
    outFile.write("================================================================================================\n")
    outFile.write("Artist Percent of Top 100 Most Streamed Songs on Spotify\n")
    outFile.write("================================================================================================\n")
    output3 = artist_percent_of_top_100_songs(cur, conn)
    for artist in output3:
        outFile.write(artist + " has written " + str(output3[artist]) + "%" +  " of the top 100 Most Streamed Songs on Spotify." + "\n\n")
    
    outFile.close()

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'music.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ArtistsS (artist TEXT PRIMARY KEY, percent_spotifytop100 INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS ArtistsY (artist TEXT PRIMARY KEY, percent_youtubeviews INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS Songs (song TEXT PRIMARY KEY, spotify_popularity_score INTEGER, youtube_popularity_score INTEGER)")

# song_percent_of_top_song_views(cur, conn)
# artist_percent_of_total_views(cur, conn)

# artist_percent_of_top_100_songs(cur, conn)
write_data_to_file("calculations", cur, conn)
import json
import sqlite3
import os
import re

def read_video_ids():
    f = open("/Users/orliforster/Desktop/Michigan/SI206/project/si206final/music_video_id.html", "r")
    data = f.read()
    d1 = json.loads(data)
    return d1

def read_video_views():
    f = open("/Users/orliforster/Desktop/Michigan/SI206/project/si206final/views.html.txt", "r")
    total_file = f.read()
    lines = total_file.split(";")
    views_list = []
    for line in lines:
        line = line.strip("\u2028")
        line = line.strip("\n")
        data = line.split("=")
        title = data[0]
        string_views = data[1]
        views = string_views.replace(",", "")
        views = views.replace(" views", "")
        views_tup = title, int(views)
        views_list.append(views_tup)   
    print(len(views_list))
    return views_list

def set_up_tables(cur, conn):
    """ Takes the database cursor and connection as inputs. Returns nothing. Creates two tables, one that will hold artists and their artist_ids, and another that holds the top 100 songs, along with their artist_ids and weeks on chart."""
    #ask if we need to create both tables, unsure about SongIds table
    cur.execute("CREATE TABLE IF NOT EXISTS YouTubeIds (song TEXT PRIMARY KEY, video_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS YouTubeViews (song TEXT PRIMARY KEY, views INTEGER)")
    conn.commit()

def fill_youtube_views(cur, conn):
# """Takes the database cursor and connection as inputs. Does not return anything. Fills in the Spotify table with songs and their artist_ids and the number of streams each song has. The creation_id is each artist's unique identification number."""
    #Calls get_spotify_top_tracks_of_2020() to get the songs off of the Spotify "Top Tracks of 2020 USA" playlist.
    views_list = read_video_views()

    cur.execute("SELECT song FROM YouTubeViews")
    song_list = cur.fetchall()
    x = 1
    count = len(song_list)
    print(len(song_list))
    for x in range(25):
        x = count
        song = views_list[count][0]
        views = views_list[count][1]
        x += 1
        cur.execute("INSERT INTO YouTubeViews (song, views) VALUES (?, ?)", (song, views))
        count += 1
    conn.commit()

def fill_youtube_ids(cur, conn):
    ids_dict = read_video_ids()
    ids_list = []
    for song in ids_dict:
        ids_tup = (song, ids_dict[song])
        ids_list.append(ids_tup)

    cur.execute("SELECT song FROM YouTubeIds")
    song_list = cur.fetchall()
    x = 1
    count = len(song_list)
    for x in range(25):
        x = count
        song = ids_list[count][0]
        video_id = ids_list[count][1][0]
        x += 1
        cur.execute("INSERT INTO YouTubeIds (song, video_id) VALUES (?, ?)", (song, video_id))
        count += 1
    conn.commit()

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'music.db')
cur = conn.cursor()
set_up_tables(cur, conn)
# fill_youtube_views(cur, conn)
fill_youtube_ids(cur, conn)


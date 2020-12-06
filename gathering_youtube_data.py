import requests
import pandas as pd
import requests
import re
import os
import csv
import sqlite3
import json
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs

def get_video_ids(cur, conn):

    cur.execute("SELECT song, artist FROM Spotify")
    song_list = cur.fetchall()
    video_dict = {}
    for song in song_list:
        if song not in video_dict:
            title = song[0]
            payload = {'part': 'snippet', 'key': 'AIzaSyCgAi5xftx7uz8369jsMctHo3zschErkvo', 'order':'viewCount', 'q': title, 'maxResults': 1}
            l = requests.Session().get('https://www.googleapis.com/youtube/v3/search', params=payload)    
            resp_dict = json.loads(l.content)
            video_id = resp_dict['items'][0]['id']['videoId']
            video_dict[title] = []
            video_dict[title].append(video_id)
    print(video_dict)
    return video_dict

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'spotify.db')
cur = conn.cursor()

f = open("music_video_id.html", "w")
d = get_video_ids(cur,conn)
result = json.dumps(d)
f.write(result)
f.close()
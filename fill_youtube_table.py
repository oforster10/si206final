import json

def read_video_ids():
    f = open("/Users/orliforster/Desktop/Michigan/SI 206/si206final/music_video_id.html", "r")
    data = f.read()
    d1 = json.loads(data)
    return d1

def read_video_views():
    f = open("/Users/orliforster/Desktop/Michigan/SI206/si206final/music_video_views.html.txt", "r")
    lines = f.readlines()
    views_list = []
    for line in lines:
        data = line.split("=")
        title = data[0]
        string_views = data[1]
        views = string_views[:-6].replace(",", "")
        views_list.append(title, views)
    print(views_list)
    return views_list

def set_up_tables(cur, conn):
    """ Takes the database cursor and connection as inputs. Returns nothing. Creates two tables, one that will hold artists and their artist_ids, and another that holds the top 100 songs, along with their artist_ids and weeks on chart."""
    #ask if we need to create both tables, unsure about SongIds table
    cur.execute("CREATE TABLE IF NOT EXISTS YouTubeIds (song TEXT PRIMARY KEY, id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS YouTubeViews (song TEXT PRIMARY KEY, views INTEGER)")
    conn.commit()

read_video_views()

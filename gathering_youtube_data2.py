from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
import json

def read_file():
    f = open("music_video_id.html", "r")
    data = f.read()
    d = json.loads(data)
    return d


def get_video_views(video_dict):
    f = open("music_video_views.html", "w")
    for song in video_dict:
        page_url = "https://www.youtube.com/watch?v=" + video_dict[song][0]
        session = HTMLSession()
        response = session.get(page_url)
        response.html.render(sleep=1)
        soup = bs(response.html.html, "html.parser")
        open("views.html", "w", encoding='utf8').write(response.html.html)
        try:
            views = soup.find("span", attrs={"class": "view-count"}).text
            print(views)
            f.write(views + ",")
            video_dict[song].append(views)
        except:
            video_dict[song].append("no video")
        
    return video_dict


d = read_file()
print(d)
print("len of file is " + str(len(d)))

d2 = get_video_views(d)
f = open("music_video_views2.html", "w")
result = json.dumps(d2)
f.write(result)
f.close()







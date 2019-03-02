# for getting html + kar
import requests
# beutify
from bs4 import *
import difflib
import re
import google_scrap

root_site = "http://www.karaokeden.com"
links_to_serach = ['/karaoke/browse/English',    
'/karaoke/browse/English-2',    
'/karaoke/browse/English-3', 
'/karaoke/browse/English-4', 
'/karaoke/browse/English-5']

def get_song_links(filename):
    filename = filename.lower().split()
    print(filename)

    song_list = []
    for _ in links_to_serach:
        rep = requests.get(root_site+_)
        html_bs4 = BeautifulSoup(rep.content, 'lxml')
        for a in html_bs4.find_all('a', href=True):
            if 'lyrics' in a.attrs['href']:
                song_name = [_song.lower() for _song in a.attrs['href'].split("/")[-1][:-4].split('+') if _song.isalpha()]
                #print("Song!:", root_site+a.attrs['href'], song_name)
                # if "linkin'" in song_name:
                # print(song_name)
                sm = difflib.SequenceMatcher(None,filename,song_name)
                if sm.ratio() > 0.4:
                    song_list.append([sm.ratio(), root_site+a.attrs['href'], a.attrs['href'].split("/")[-1]])
    
    song_list = sorted(song_list, key = lambda x:x[0], reverse=True)
    return song_list


def download_kar(song_inf):
    print("Downloading:", song_inf)
    _, link, filename = song_inf
    filename = "./temp/"+filename
    # get lyrics
    rep = requests.get(link)
    html_bs4 = BeautifulSoup(rep.content, "lxml")

    lyrics = html_bs4.find_all(id="lyrics")[0]
    for br in lyrics.find_all("br"):
        br.replace_with("\n")
    lyrics = lyrics.text
    lyrics = "\n".join([_.strip() for _ in lyrics.split("\n") if not not _.strip()])

    f = open(filename + ".txt", "w")
    f.write(lyrics)
    f.close()

    # get .kar
    link = link.replace('lyrics', 'download')
    r = requests.get(link)
    # f = open(filename, 'wb')
    with open(filename, 'wb') as sf:
        sf.write(r.content)

import time
def download_video(query):
    links = google_scrap.search_link(query)
    print("Links:", links)
    name, link = links[0]
    print("Downloading:", name, link)
    
    _ = google_scrap.download(name, link)
    while not _:
        time.sleep(15)
        print("retry")

        _ = google_scrap.download(name, "http://" + link)

if __name__ == "__main__":
    songname = str(input("Song name: "))

    file_name = get_song_links(songname)

    download_kar(file_name[0])
    # download_video(songname)
# print (file_name)
# print(file_name)
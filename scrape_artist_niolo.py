from typing import TextIO
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import random
import os
from string import ascii_lowercase


def save_file(path, text, replace=False):
    if not replace:
        if os.path.exists(os.path.relpath(path + ".txt")):
            file=open(path +".txt", 'a')
            file.write(text)
            file.close()
        else:
            file = open(path + ".txt", "w")
            file.write(text)
            file.close()
    else:
        file = open(path + ".txt", "w")
        file.write(text)
        file.close()


def get_lyrics(song_url, save=False, replace=False, folder="songs"):
    song = urlopen(song_url)
    soup = BeautifulSoup(song.read(), "html.parser")
    lyrics = soup.find_all("div")[20].get_text()
    title = soup.find_all("b")[1].get_text().replace('"', '')
    file_title = title.replace(" ", "_")
    album = soup.find_all(class_="songinalbum_title")
    album_name=str(album[0].get_text())[7:]

    if not save:
        return album_name, lyrics
    else:
        if os.path.exists(os.path.relpath(folder + "/albums/" )):
            save_file(folder + "/albums/" + "/" + album_name, text=lyrics, replace=replace)
        else:
            os.makedirs(os.path.relpath(folder + "/albums/" ))
            save_file(folder + "/albums/" , text=lyrics, replace=replace)


def scrape_artist(az_url, sleep="random", replace=False, folder="songs"):
    home = "https://www.azlyrics.com/"
    main_page = urlopen(az_url)
    bs = BeautifulSoup(main_page.read(), "html.parser")
    divs = bs.find_all('div', {"class": "listalbum-item"})
    urls = list()
    for d in divs:
        urls.append(home + d.a['href'].split("/", 1)[1])
    n = len(urls)
    i = 1
    for url in urls:
        get_lyrics(url, save=True, replace=replace, folder=folder)
        if sleep == "random":
            rt = random.randint(5, 15)
            t = 10
        else:
            rt = t = sleep
        print("Songs downloaded:", i, "/", n, " -  ETA:", round(t*(n-i)/60, 2), "minutes")
        i += 1
        time.sleep(rt)  # This is to avoid being recognized as a bot





#scrape_artist("https://www.azlyrics.com/b/beatles.html", sleep="random", replace=False, folder="songs")


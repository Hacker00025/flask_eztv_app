from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.request

app = Flask(__name__)
downloaded = []


@app.route("/")
def home():
    downloaded.clear()
    return render_template("index.html")


@app.route("/dl", methods=["POST"])
def download():
    url = request.form.get("url")
    season = request.form.get("season")
    quality = request.form.get("quality")
    #return render_template("check.html", url=url, season=season, quality=quality)
    torrent_downloader(url, season, quality)
    if not downloaded:
        return render_template("Failed.html")
    else:
        return render_template("Complete.html", list=downloaded)

def torrent_downloader(url,season,quality):
    #fullname = name + ".torrent"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features='html.parser')
    for item_name in soup.findAll('a', {'class': 'download_1'}):
        torrent = str(item_name.get("href"))
        title = str(item_name.get("title"))
        clean_title = title.replace(" Torrent: Download Mirror #1", ".torrent")
        fullname = clean_title
        if season in fullname:
            if quality in fullname:
                #print(fullname)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'CERN-LineMode/2.15 libwww/2.17b3')]
                urllib.request.install_opener(opener)  # NOTE: global for the process
                urllib.request.urlretrieve(torrent, fullname)
                downloaded.append(fullname)
                print(fullname, "File was downloaded")
            if not downloaded:
                pass
            else:
                for episode in downloaded:
                    print(episode, 'was downloaded')
                    #return render_template("Complete.html")
        else:
            print("The requested season/quality was not found,or all possible episodes have been downloaded")


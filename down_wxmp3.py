# -*- coding: UTF-8 -*- 

import os
from time import sleep

import requests
from bs4 import BeautifulSoup


def download(mp3_url, save_url, file_name):
    try:
        if mp3_url is None or save_url is None or file_name is None:
            return None
        folder = os.path.exists(save_url)
        if not folder:
            os.makedirs(save_url)
        res = requests.get(mp3_url, stream=True)
        file_path = os.path.join(save_url, file_name)
        with open(file_path, 'wb') as fd:
            for chunk in res.iter_content():
                fd.write(chunk)
        print(file_name + ' is OK!')
    except:
        print("Error")


def fetch_audio_url(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    html = r.text
    bs = BeautifulSoup(html, 'html.parser')
    title = bs.find(["h1"], attrs={'id': 'activity-name'})
    id = bs.find(['mpvoice'])['voice_encode_fileid']

    audioUrl = "https://res.wx.qq.com/voice/getvoice?mediaid=" + id
    name = title.contents[0].strip() + ".mp3"
    print("name: " + name + "     address: " + audioUrl)
    return audioUrl, name


def plists_detail(source, save_path, tags):
    html = open(source)
    bs = BeautifulSoup(html, 'html.parser')
    tags_list = bs.find_all(tags)
    pages = [tag['data-link'] for tag in tags_list if tag['data-link']]
    for page in pages:
        url, name = fetch_audio_url(page)
        download(url, save_path, name)
        sleep(1)


if __name__ == "__main__":
    plists_detail("./all.html", './tangshi', ['li'])

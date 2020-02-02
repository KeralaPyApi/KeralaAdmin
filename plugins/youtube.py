import keralabot
import logging
import aiohttp
from bs4 import BeautifulSoup
from config import *


def search(query):
    url_base = "https://www.youtube.com/results"
    url_yt = "https://www.youtube.com"
    with aiohttp.ClientSession() as session:
        r = session.get(url_base, params=dict(q=query))
        page = r.text()
    soup = BeautifulSoup(page, "html.parser")
    id_url = None
    list_videos = []
    for link in soup.find_all('a'):
        url = link.get('href')
        title = link.get('title')
        if url.startswith("/watch") and (id_url != url) and (title is not None):
            id_url = url
            dic = {'title': title, 'url': url_yt + url}
            list_videos.append(dic)
        else:
            pass
    return list_videos

@bot.message_handler(commands=['/ytsearch'])
def youtube_search(message):
    res = search(message.text[10:])
    vids = ['{}: <a href="{}">{}</a>'.format(num + 1, i['url'], i['title']) for num, i in enumerate(res)]
    bot.reply_to(message, '\n'.join(vids), parse_mode="HTML")


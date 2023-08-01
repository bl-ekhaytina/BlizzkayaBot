import requests
from bs4 import BeautifulSoup

import bb_info

bot = bb_info.bot


# запостить статью в канал
def post_article(message):
    back_post_id = 0
    while True:
        post_text = parser(back_post_id)
        back_post_id = post_text[1]
        print(back_post_id)
        if post_text[0] != None:
            bot.send_message(message.chat.id, post_text)


# получение информации из статьи
def parser(back_post_id):
    url = "https://habr.com/ru/search/?q=python&target_type=posts&order=date"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("article", class_="tm-articles-list__item", id=True)
    post_id = post["id"]

    if post_id != back_post_id:
        title = post.find("a", class_="tm-title__link").text.strip()
        description = post.find("div",
                                class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text.strip()
        href = post.find("a", class_="tm-article-snippet__readmore", href=True)["href"].strip()

        return f"{title}\n\n{description}\n\nhttps://habr.com{href}"
    else:
        return None, post_id

import requests, time
from bs4 import BeautifulSoup
from datetime import datetime
from elasticsearch_dsl import Text, Keyword, Date
from elasticsearch_dsl.document import Document
from elasticsearch_dsl.connections import connections

class Post(Document):
    original_url = Keyword()
    date = Date()
    title = Text()
    content = Text()

    class Index:
        name = 'mediumposts'

    def save(self, **kwargs):
        # self.created_at = datetime.now()
        return super(Post, self).save(**kwargs)


class MediumCrawler:
    def __init__(self, keyword):
        # connections.create_connection(hosts=['localhost'])

        self.url = "https://medium.com"
        self.keyword = keyword
        self.hdrs = {'User-Agent': 'Mozilla/5.0'}
        self.file = open("content.txt", "w", encoding="utf-8")
        self.count = 1

        self.run()

    def run(self):
        file = open("content.txt", "w", encoding="utf-8")
        r = requests.get(self.url + "/search/tags?q=" + self.keyword)
        root_soup = BeautifulSoup(r.content, 'html.parser')
        items = []
        posts = []
        key = []
        link = []
        item_link = []

        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day

        date_ = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in date_:
            if month == i:
                month = "0" + str(i)

        for i in date_:
            if day == i:
                day = "0" + str(i)

        for i in root_soup.find_all("a", {"class": "link u-baseColor--link"}):
            items.append(i.text)

        for i in items:
            j = str(i)
            key.append(j.replace(" ", "-"))

        for item in key:
            link.append("https://medium.com/tag/" + item + "/archive/" + str(year) + "/" + str(month) + "/" + str(day))
        print(link)

        for item in link:

            content = requests.get(item, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'})
            link_soup = BeautifulSoup(content.content, 'html.parser')
            for i in link_soup.find_all("a", {
                "class": "button button--smaller button--chromeless u-baseColor--buttonNormal"}):
                item_link.append(i.get("href"))

        for item in item_link:

            item_content = requests.get(item, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'})
            content_soup = BeautifulSoup(item_content.content, 'html.parser')
            date = content_soup.find("meta", {"property": "article:published_time"}).get("content")

            tarih = date.split("T")[0]
            date_format = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            ts = time.time()
            now = datetime.fromtimestamp(ts)
            suan = now.strftime('%Y-%m-%d')
            # now.strftime('%Y-%m-%d')

            if tarih == suan:
                print(item)
                print(date_format)

                if content_soup.find("h1") != None:
                    title = content_soup.find("h1").text
                    print(title)
                elif content_soup.find("strong") != None:
                    title = content_soup.find("strong").text
                else:
                    print("TITLE YOK")
                    title = "TITLE YOK"

                article_soup = BeautifulSoup(str(content_soup.find("article")), "html.parser")
                articles = article_soup.findAll("section")
                article = ""
                for i in articles:
                    article += str(i)

                text_soup = BeautifulSoup(article, 'html.parser')

                full_text = text_soup.getText(separator=u' ')
                print(full_text)

                post_medium = Post()
                post_medium.original_url = item
                post_medium.date = date
                post_medium.title = title
                post_medium.content = full_text
                posts.append(post_medium)

        connections.create_connection(hosts=['localhost'])
        Post.init()  # delete
        for post in posts:
            post.save()
        return posts


if __name__ == "__main__":
    MediumCrawler("youtube")

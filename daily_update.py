import requests
import json
from bs4 import BeautifulSoup
import datetime
import os
import time
import traceback
import random
from qcloud_image import Client, CIFile
from qcloud_image import CIUrl, CIFile, CIBuffer
from qcloud_image import CIUrls, CIFiles, CIBuffers
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoBlog.settings')
django.setup()
from blog.models import *
from accounts.models import *


# 百度色情图片鉴定
appid = '1254186078'
secret_id = 'AKIDxnX6Xq9NM8h6LSRahcLuIXebfYFkh82l'
secret_key = 'hDXe6SddT7ZpyvgFcqyudAVhjZCdsHYd'
bucket = 'test'

def getcontent():
    today=str(datetime.datetime.now().strftime('%Y-%m-%d'))
    url = 'https://www.shanbay.com/soup/mobile/quote/'+today+'/?content_id=1676&social_service=x&url_key=8a60bd51c&content_type=quote%3Aquote&track_id=2696e460-11db-11e7-a294-00163e124371'
    response = requests.request(url=url,method="get").text
    html = BeautifulSoup(response,"html.parser")

    try:
        content= html.find_all('div',attrs={"class": "content"})[0]
        content = content.get_text()
    except:
        pass

    try:
        translation = html.find_all('div',attrs={"class": "translation"})[0]
        translation = translation.get_text()
    except:
        pass
    return content,translation


def check_image():
    client = Client(appid, secret_id, secret_key, bucket)
    client.use_http()
    client.set_timeout(30)

    status = True
    while status:

        num = str(int(random.uniform(200000,500000)))
        url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"+num+".jpg"
        result =  client.porn_detect(CIUrls([url]))["result_list"][0]
        if result["message"] == "success":
            if result["data"]["porn_score"] < 1:
                status = False
    return  url, result

def create_article():
    content,translation = getcontent()
    url , result = check_image()

    title = str(datetime.datetime.now().date()) +  " 每日一句"
    body =  "![enter image description here][1]\r\n\r\n\r\n  [1]: %s \r\n\r\n" % str(url) \
            + content + "\r\n\r\n" + translation

    author   = BlogUser.objects.filter(username='李二狗')[0]
    category = Category.objects.filter(name="英语早操")[0]
    order    = Article.objects.all().count()+1
    tag      = Tag.objects.filter(name='英语早操')[0]
    article  = Article.objects.create(
                author = author,
                title = title,
                body  = body,
                category = category,
                article_order = order,
            )
    article.tags.add(tag)
    article.save()

    return None

if __name__ == '__main__':

    '''
    import random
    num = str(int(random.uniform(1,500000)))
    url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"+num+".jpg"
    '''
    # url , result = check_image()
    # print ("可信度：",result["data"]["confidence"],"性感值：",result["data"]["hot_score"],"色情值：",result["data"]["porn_score"])
    # content,translation = getcontent()
    create_article()

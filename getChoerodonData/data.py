#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from os import path
from PIL import Image
import numpy as np
import requests
from io import open
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from bs4 import BeautifulSoup
import json
import re
from collections import Counter
import jieba

def fetch_choerodon_io_comments():
    home_path = 'http:/forum.choerodon.io/'
    comment_path = []
    s = ''
    for i in range(0, 50):
        data = requests.get(
            'http://forum.choerodon.io/latest.json?no_definitions=true&no_subcategories=false&page='
            + str(i) + '&_=1543471691742')
        topic_list = json.loads(data._content)['topic_list']['topics']
        for topic in topic_list:
            s = s + topic['title']
            comment_path.append('http://forum.choerodon.io/t/'+str(topic['id'])+'.json?track_visit=true&forceLoad=true&_=1543479427806')
    for link in comment_path:
        data = requests.get(link)
        topic_list = json.loads(data._content)['post_stream']['posts']
        for topic in topic_list:
            soup = BeautifulSoup(topic['cooked'], 'lxml')
            for content in soup.find_all('p'):
                s = s + content.text
    with open('subjects.txt', 'w', encoding='utf-8') as f:
        f.write(s)


def extract_words():
    with open('subjects.txt', 'r', encoding='utf-8') as f:
        comment_subjects = f.readlines()
    #加载stopword
    stop_words = set(
        line.strip() for line in open('stopwords.txt', encoding='utf-8'))
    commentlist = []
    for subject in comment_subjects:
        if subject.isspace(): continue
        #分词
        word_list = pseg.cut(subject)
        for word, flag in word_list:
            if not word in stop_words:
                commentlist.append(word)
    content = ''.join(commentlist)
    d = path.dirname(__file__)
    alice_coloring = np.array(Image.open(path.join(d, "choerodon.png")))
    # 你可以通过 mask 参数 来设置词云形状
    wc = WordCloud(
        background_color="white",
        font_path=path.join(d, "simfang.ttf"),
        max_words=2000,
        mask=alice_coloring,
        max_font_size=40,
        random_state=42).generate(content)
    # create coloring from image
    image_colors = ImageColorGenerator(alice_coloring)
    # show
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    wc.to_file('test.png')
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    # 我们还可以直接在构造函数中直接给颜色
    # 通过这种方式词云将会按照给定的图片颜色布局生成字体颜色策略
    # plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    # plt.axis("off")
    # plt.figure()
    # plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
def get_words():
    commentlist = []
    with open('subjects.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        seg_list = pseg.cut(txt)
        stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
        for word, flag in seg_list:
            if not word in stop_words:
                commentlist.append(word)
        c = Counter()
        for x in commentlist:
            if len(x)>1 and x != '\r\n':
                c[x] += 1
        print('常用词频度统计结果')
        for (k,v) in c.most_common(100):
            # print(str(k)+"*****"+str(v))
            print('%s %s  %d' % ( k, '**********', v))

if __name__ == "__main__":
    # fetch_choerodon_io_comments()
    # extract_words()
    get_words()
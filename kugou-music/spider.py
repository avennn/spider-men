#! python3
# -*- coding: utf-8 -*-

import re, time, random, requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class KuGouMusic(object):
  def __init__(self):
    self.ORIGIN_URL = 'http://www.kugou.com/yy/singer/index/'
    self.CN_TYPES = [2, 3, 4]
    self.SORTS = [
      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
      'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'null'
    ]
    self.client = MongoClient('mongodb://localhost:27017/')
    self.db = self.client['kugou']
    self.driver = webdriver.PhantomJS()
    self.user_agents = [
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
      'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
      'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
      'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
    ]
    self.pages = {}
    self.page_urls = set()
  def create_path_by_suffix(self, suffix):
    url = self.ORIGIN_URL + suffix + '.html'
    return url
  def create_path_by_keys(self, page, sort, type):
    url = self.ORIGIN_URL + str(page) + '-' + sort + '-' + str(type) + '.html'
    return url
  def get_page_by_url(self, url):
    headers = {'User-Agent': random.choice(self.user_agents)}
    r = requests.get(url, headers=headers, cookies=None)
    return r.text
  def get_singer_urls_by_page(self, url):
    try:
      html = self.get_page_by_url(url)
      bs_obj = BeautifulSoup(html, 'html.parser')
      has_img_elements = bs_obj.find('ul', id='list_head').find_all('strong')
      for ele in has_img_elements:
      # 带有歌手图片的link
        singer_link = ele.find('a')['href']
        print(singer_link)
        self.db.singer_urls.insert_one({'text': singer_link})
      no_img_elements = bs_obj.find('div', id='list1').find_all('a')
      for a in no_img_elements:
        # 不带歌手图片的link
        singer_link = a['href']
        print(singer_link)
        self.db.singer_urls.insert_one({'text': singer_link})
    except ConnectionError as e:
      print(e)
    except AttributeError as e:
      print(e)
  def get_pages_num(self):
    for type in self.CN_TYPES:
      for s in self.SORTS:
        url = self.create_path_by_keys(1, s, type)
        html = self.get_page_by_url(url)
        bs_obj = BeautifulSoup(html, 'html.parser')
        pagers = bs_obj.find('span', id='mypage').find_all(id=re.compile('^page_\d{1,3}$'))
        last_page_num = int(pagers.pop().text)
        key = s + '-' + str(type)
        self.pages[key] = last_page_num
    print(self.pages)
  def get_page_url_set(self):
    for key, value in self.pages.items():
      for i in range(value):
        suffix = str(i + 1) + '-' + key
        url = self.create_path_by_suffix(suffix)
        self.page_urls.add(url)
  def get_singer_urls(self):
    for url in self.page_urls:
      self.get_singer_urls_by_page(url)
  def get_singer_desc(self):
    singer_urls = self.db.singer_urls.find()
    print(singer_urls.count())
    for url in singer_urls:
      if ('singer' not in url.keys()):
        time.sleep(random.randint(60, 90))
        html = self.get_page_by_url(url['text'])
        bs_obj = BeautifulSoup(html, 'html.parser')
        # 60-90s,ok
        # db.getCollection('singer_urls').find({'singer': /.+/}).count()
        # total:11709,now:2295
        try:
          sng_ins = bs_obj.find('div', class_='sng_ins_1')
          singer = sng_ins.find('div', class_='top').find('strong').text
          desc = sng_ins.find('div', id='text').find('div', class_='bordr_cen').text
          print(singer)
          self.db.singer_urls.update_one({'_id': url['_id']}, {
            '$set': {'singer': singer, 'desc': desc}
          }, upsert=False)
        except ConnectionError as e:
          print(e)
        except AttributeError as e:
          print(e)
  def get_album_urls(self):
    singer_urls = self.db.singer_urls.find()
    for url in singer_urls:
      self.driver.get(url['text'])
      try:
        album_ele = self.driver.find_element_by_xpath("//ul[@class='tab clear_fix']/li[2]")
        album_ele.click()
        time.sleep(random.randint(5, 10))
        expect = WebDriverWait(self.driver, 10).until(
          EC.text_to_be_present_in_element((By.XPATH, "//ul[@class='tab clear_fix']/li[2]"), '专辑')
        )
        if expect:
          html = self.driver.page_source
          bs_obj = BeautifulSoup(html, 'html.parser')
          singer = bs_obj.find('div', class_='intro').find('strong').text
          albums = bs_obj.find('ul', id='album_container').find_all('li')
          print('歌手', singer)
          for album in albums:
            album_url = album.find('a', class_='pic')['href']
            album_name = album.find('p').find('a').text
            album_date = album.find('span').text
            print('专辑', album_name)
            print('专辑url', album_url)
            self.db.albums.insert_one({
              'singer': singer,
              'url': album_url,
              'name': album_name,
              'date': album_date
            })
      except ConnectionError as e:
        print(e)
      except AttributeError as e:
        print(e)
    self.driver.close()
  def get_songs(self):
    albums = self.db.albums.find()
    for album in albums:
      url = album['url']
      try:
        html = self.get_page_by_url(url)
        bs_obj = BeautifulSoup(html, 'html.parser')
        time.sleep(random.randint(5, 10))
        l_box = bs_obj.find('div', class_='l')
        # 更新albums表
        raw_album_desc = l_box.find('p', class_="intro").text
        album_desc = raw_album_desc.strip().lstrip('简介：')
        self.db.albums.update_one({'_id': album['_id']}, {
          '$set': {'desc': album_desc}
        })
        # 插值songs表
        detail = l_box.find('p', class_='detail')
        contents = detail.contents
        for i, content in enumerate(contents):
          if (content == '\n') == True:
            contents.pop(i)
        # 专辑
        album = contents[1]
        # 歌手
        singer = contents[4]
        # 发片公司
        company = contents[7]
        # 发行日期
        date = contents[10].strip('\r\n')
        print(album, singer, company, date)
        song_list = bs_obj.find('div', id='songs').find('ul').find_all('li')
        for song in song_list:
          title = song.find('a')['title']
          # 歌曲名称
          song_name = title.split('-')[1].strip()
          self.db.songs.insert_one({
            'singer': singer,
            'album': album,
            'company': company,
            'date': date,
            'name': song_name
          })
      except ConnectionError as e:
        print(e)
      except AttributeError as e:
        print(e)


kugou = KuGouMusic()

# 获取所有华语歌手的首页url并存入mongodb
# kugou.get_pages_num()
# kugou.get_page_url_set()
# kugou.get_singer_urls()

# 获取华语歌手的名称和简介并更新到mongodb
kugou.get_singer_desc()

# 获取歌手的所有专辑的url并存入mongodb
# kugou.get_album_urls()

# 通过专辑获取歌曲名称
# kugou.get_songs()
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import csv

# link html web yang mau di scrap
title = ''
url = 'https://letterboxd.com/film/{}/reviews/page/'.format(title)

# headers supaya web tidak mendeteksi kita sebagai bot tetapi sebagai browser
headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

page_position = 0
df = []
# isi disini mau sampe halaman ke berapa yang diambil
for page in range(1, 21):
    page_position+=1
    print('scrapping page:', page_position)
    # koneksi ke web
    req = requests.get(url+str(page), headers=headers)

    # ubah ke format Beautiful Soup
    soup = BeautifulSoup(req.text, 'html.parser')
    review = soup.findAll('div', 'film-detail-content')

    ## check wether suceed
    # for i in review:
    #   user = i.find('strong', 'name').text.split('\n')
    #   print(user)

    for i in review:
      user = i.find('strong', 'name').text
      tanggal = i.find('span', '_nobr').text
      content = i.find('div', 'body-text -prose collapsible-text').find('p').text
      df.append([user, tanggal, content])

# bikin header kolom file csv
column = ['user', 'comment date', 'review content']

# tambahkan tanggal hari ini sebagai nama file
today = date.today()
file = csv.writer(open('scrap-result/scrap-letterboxd-dunetwo-{}.csv'.format(today), 'w', newline='', encoding='utf-8'))

# overwrite file csv
file.writerow(column)
for x in df:
  file.writerow(x)
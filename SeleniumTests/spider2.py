from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pytube import YouTube
import requests
import shutil
import csv
import os
import time

opt = webdriver.EdgeOptions()
opt.add_experimental_option('detach', True)

url = "https://altnews.in"

driver = webdriver.Edge(options=opt)
driver.get(url)


def download_video(vid_url, p):
    link = YouTube(vid_url)
    video = link.streams.get_lowest_resolution()
    if not os.path.exists(f'{p}\\news_videos'):
        os.makedirs(f'{p}\\news_videos')
    print('Downloading Video...')
    video.download(f'{p}\\news_videos')


def download_image(img_url, name, p):
    if name[0] == 'B' and name[1] == 'Y' and name[2] == ' ':
        n = name
    else:
        icount = 0
        space_count = 0
        n = ''
        while icount < len(name):
            if space_count <= 3:
                if not (name[icount] == '/' or name[icount] == '\\' or name[icount] == ':' or name[icount] == '*' or
                        name[icount] == '?' or name[icount] == '"' or name[icount] == '<' or name[icount] == '>' or
                        name[icount] == '|'):
                    n = n + name[icount]
                if name[icount] == ' ':
                    space_count += 1
            icount += 1

    response = requests.get(img_url, stream=True)
    filename = f'{p}\\news_images\\{n}.jpg'
    if not os.path.exists(f'{p}\\news_images'):
        os.makedirs(f'{p}\\news_images')
    print('Downloading Image...')
    with open(filename, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    del response

# previous_scroll_height = driver.execute_script('return document.body.scrollHeight;')
#
# while True:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#     time.sleep(3)
#     new_scroll_height = driver.execute_script('return document.body.scrollHeight;')
#     if previous_scroll_height == new_scroll_height:
#         break
#     previous_scroll_height = new_scroll_height


path = 'F:\\PyCharm\\DataScience(Dr. Usama)\\WebScrapping\\Alt_News'
element = driver.find_element(By.TAG_NAME, 'body')

for i in range(0, 200):
    element.send_keys(Keys.END)
    print('**************************', i, '*******************************')

if not os.path.exists(path):
    os.makedirs(path)

with open(f'{path}\\news_info.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Quote', 'Author', 'Posted Date', 'Category', 'Author Image Link', 'News Link', 'Image Link'])
    file.close()

video_link = driver.find_element(By.CSS_SELECTOR, 'iframe.youtube-player').get_attribute('src')
print('Video Link', video_link)

div = driver.find_elements(By.CSS_SELECTOR, 'div.vc_row.wpb_row.vc_row-fluid')
div = div[6].find_elements(By.CSS_SELECTOR, 'div.pbs-content')
div = div[0].find_elements(By.CSS_SELECTOR, 'div.pbs-row')

for rows in div:
    cols = rows.find_elements(By.CSS_SELECTOR, 'div.pbs-col')
    for col in cols:
        quote = col.find_element(By.CSS_SELECTOR, 'h4').text
        posted_date = col.find_element(By.CSS_SELECTOR, 'span.posted-on.meta-info').text
        category = col.find_element(By.CSS_SELECTOR, 'span.cat-links.meta-info').text
        try:
            author = col.find_element(By.CSS_SELECTOR, 'span.author.vcard').text
            author_image_link = col.find_element(By.CSS_SELECTOR, 'span.author.vcard')
            author_image_link = author_image_link.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except BaseException as E:
            print(E)
            author = col.find_element(By.CSS_SELECTOR, 'span.co-authors.vcard').text
            author_image_link = col.find_element(By.CSS_SELECTOR, 'span.co-authors.vcard')
            author_image_link = author_image_link.find_element(By.TAG_NAME, 'img').get_attribute('src')
        news_link = col.find_element(By.TAG_NAME, 'a').get_attribute('href')
        image_link = col.find_element(By.TAG_NAME, 'img').get_attribute('src')

        with open(f'{path}\\news_info.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([quote, author, posted_date, category, author_image_link, news_link, image_link])
            file.close()

        download_image(author_image_link, author, path)
        download_image(image_link, quote, path)

        print('Quote:', quote)
        print('Author:', author)
        print('Posted Date:', posted_date)
        print('Category:', category)
        print('Author Image Link:', author_image_link)
        print('News Link:', news_link)
        print('Image Link:', image_link)

download_video(video_link, path)
driver.close()

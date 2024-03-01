from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import shutil
import csv
import os
import time

opt = webdriver.EdgeOptions()
opt.add_experimental_option('detach', True)

url = "https://mastodon.social/explore"

driver = webdriver.Edge(options=opt)
driver.get(url)

path = 'F:\\PyCharm\\DataScience(Dr. Usama)\\WebScrapping\\Mastodon'


def download_image_video(img_url, name, p, file_type):
    if img_url != 'None':
        if file_type != 'videos':
            filename = f'{p}\\posts_{file_type}\\{name}.jpg'
        else:
            filename = f'{p}\\posts_{file_type}\\{name}.mp4'
        response = requests.get(img_url, stream=True)
        if not os.path.exists(f'{p}\\posts_{file_type}'):
            os.makedirs(f'{p}\\posts_{file_type}')
        print(f'Downloading {file_type}...')
        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        del response

if not os.path.exists(path):
    os.makedirs(path)

with open(f'{path}\\posts_info.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Username', 'Display Name', 'Avatar Link', 'Posted Date', 'Replies', 'Boosts', 'Stars', 'Image Link', 'Video Link'])
    file.close()

element = driver.find_element(By.TAG_NAME, 'body')
previous_scroll_height = None
previous_username = None
username = 'nothing'

for i in range(0, 200):
    data_found = True
    while data_found:
        data_found = False
        try:
            username = driver.find_element(By.CSS_SELECTOR, 'span.display-name__account').text
        except BaseException as E:
            data_found = True
    if previous_username != username:
        previous_username = username
        try:
            display_name = driver.find_element(By.CSS_SELECTOR, 'strong.display-name__html').text
        except BaseException as E:
            pass
        try:
            avatar = driver.find_element(By.CSS_SELECTOR, 'div.account__avatar').find_element(By.TAG_NAME,
                                                                                              'img').get_attribute(
                'src')
        except BaseException as E:
            pass
        try:
            date = driver.find_element(By.TAG_NAME, 'time').get_attribute('title')
        except BaseException as E:
            pass
        try:
            content = driver.find_element(By.CSS_SELECTOR,
                                          'div.status__content__text.status__content__text--visible.translate').text
        except BaseException as E:
            pass
        try:
            image = driver.find_element(By.CSS_SELECTOR, 'a.media-gallery__item-thumbnail').get_attribute('href')
        except BaseException as E:
            print("Image:", E)
            image = 'None'
        try:
            video = driver.find_element(By.CSS_SELECTOR, 'video').get_attribute('src')
        except BaseException as E:
            print("Video:", E)
            video = 'None'
        try:
            replies = driver.find_elements(By.CSS_SELECTOR, 'button.status__action-bar__button')[0].text
        except BaseException as E:
            pass
        try:
            boosts = driver.find_elements(By.CSS_SELECTOR, 'button.status__action-bar__button')[1].text
        except BaseException as E:
            pass
        try:
            stars = driver.find_elements(By.CSS_SELECTOR, 'button.status__action-bar__button')[2].text
        except BaseException as E:
            pass

        with open(f'{path}\\posts_info.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [username, display_name, avatar, date, replies, boosts, stars, image, video])
            file.close()

        if not os.path.exists(f'{path}\\posts_content'):
            os.makedirs(f'{path}\\posts_content')

        with open(f'{path}\\posts_content\\{display_name}.txt', 'w', newline='', encoding="utf-8") as file:
            file.write(content)
            file.close()

        download_image_video(avatar, username, path, 'avatars')
        download_image_video(image, username, path, 'images')
        download_image_video(video, username, path, 'videos')

    time.sleep(3)
    element.send_keys(Keys.PAGE_DOWN)
    print('**************************', i, '*******************************')

driver.close()
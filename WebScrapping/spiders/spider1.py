import scrapy
import csv
import os


class Spider1Spider(scrapy.Spider):
    name = "spider1"
    allowed_domains = ["politifact.com"]
    start_urls = ["https://politifact.com"]

    if not os.path.exists('Politifact'):
        os.makedirs('Politifact')

    with open('Politifact/news_info.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Stated Date', 'Quote', 'Published Date', 'Publisher', 'News Link', 'Image Link'])
        file.close()

    def parse(self, response):
        News = response.css('section.o-platform')

        if News.get() is not None:
            next_page = 'https://www.politifact.com' + News[0].css('footer.o-platform__link a::attr(href)').get()
            News = News[0].css('.o-listease__item')
        else:
            News = response.css('.o-listicle__item')
            next_page = response.css('li.m-list__item a::text').get()
            if next_page == 'Previous' and len(response.css('li.m-list__item a::text')) == 2:
                next_page = 'https://www.politifact.com/factchecks/list/' + response.css('li.m-list__item a::attr(href)')[1].get()
            else:
                next_page = 'https://www.politifact.com/factchecks/list/' + response.css('li.m-list__item a::attr(href)').get()

        for news in News:
            title = news.css('div.m-statement__meta a::attr(title)').get()
            dlist = news.css('div.m-statement__desc::text').get().split(' ')[2:5]
            date = dlist[0] + ' ' + dlist[1] + dlist[2]
            quote = news.css('div.m-statement__quote a::text').get().strip()
            publ = news.css('footer.m-statement__footer::text').get().strip().split(' ')
            published_date = publ[len(publ)-3] + ' ' + publ[len(publ)-2] + publ[len(publ)-1]
            publ = news.css('footer.m-statement__footer::text').get().strip().split(' ')
            publisher = publ[1]
            for i in range(2, len(publ) - 4):
                publisher = publisher + ' ' + publ[i]

            news_link = 'https://www.politifact.com' + news.css('div.m-statement__quote a::attr(href)').get()
            image_link = news.css('div.c-image img::attr(src)').get()

            yield scrapy.Request(image_link, meta={'title': title}, callback=self.parse_image)
            yield response.follow(news_link, meta={'quote': quote}, callback=self.parse_news_text)

            yield{
                'title': title,
                'stated_date': date,
                'quote': quote,
                'published_date': published_date,
                'publisher': publisher,
                'news_link': news_link,
                'image_link': image_link,
            }

            with open('Politifact/news_info.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([title, date, quote, published_date, publisher, news_link, image_link])
                file.close()

        if response.css('li.m-list__item a::text').get() == 'Previous' and len(response.css('li.m-list__item a::text')) == 2:
            yield response.follow(next_page, callback=self.parse)
        if response.css('section.o-platform').get() is not None:
            yield response.follow(next_page, callback=self.parse)
        if response.css('li.m-list__item a::text').get() == 'Next':
            yield response.follow(next_page, callback=self.parse)

    def parse_image(self, response):
        title = response.meta.get('title')
        filename = f'Politifact/news_images/{title}.jpg'
        if not os.path.exists('Politifact/news_images'):
            os.makedirs('Politifact/news_images')
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse_news_text(self, response):
        quote = response.meta.get('quote')
        if not os.path.exists('Politifact/news_text'):
            os.makedirs('Politifact/news_text')
        paragraphs = response.css('article.m-textblock p::text')
        for para in paragraphs:
            with open(f'Politifact/news_text/{quote}.txt', 'a', newline='', encoding="utf-8") as file:
                file.write(para.get() + '\n')
                file.close()
            yield{'para': para.get()}

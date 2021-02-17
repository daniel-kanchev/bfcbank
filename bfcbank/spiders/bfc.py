import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bfcbank.items import Article


class BfcSpider(scrapy.Spider):
    name = 'bfc'
    start_urls = ['https://www.bfcbank.co.uk/media-centre/']

    def parse(self, response):
        links = response.xpath('//article//a[@class="button "]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="heading"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="meta-item meta-date"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%B %d, %Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="story post-story"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()

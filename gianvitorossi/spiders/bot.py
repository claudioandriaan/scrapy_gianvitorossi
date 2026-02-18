import scrapy

class BotSpider(scrapy.Spider):
    name = "bot"
    allowed_domains = ["www.gianvitorossi.com"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.gianvitorossi.com/it_it",
            callback=self.parse
        )

    def parse(self, response):
        product_pages = response.xpath('//a[@role="menuitem"]/@href').getall()

        for product_page in product_pages:
            yield scrapy.Request(
                response.urljoin(product_page),
                callback=self.get_product_list
            )

    def get_product_list(self, response):
        product_links = response.xpath('//a[contains(@class,"b-product_tile-image_link")]/@href').getall()

        for link in product_links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.get_product_details
            )

        next_page = response.xpath(
            '//a[@data-event-click.prevent="loadMore"]/@href'
        ).get()

        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.get_product_list
            )

    def get_product_details(self, response):
        name = response.xpath(
            '//h1[contains(@class,"b-product_details-name")]/text()'
        ).get()

        price = response.xpath(
            '//span[contains(@class,"b-price-item")]/text()'
        ).get()

        yield {
            "name": name.strip() if name else '',
            "full_price": price.strip() if price else '',
            "price": price.strip() if price else 0,
            "url": response.url,
        }

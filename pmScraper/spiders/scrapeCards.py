import scrapy

class scrapeCSS(scrapy.Spider):
    name= "cardScraper"
    custom_settings = {'FEED_URI': 'scraped_cards.csv'}
    start_urls = ['http://www.p-memories.com/card_product_list_page?s_flg=on&field_title_nid=&field_type_value=&product_title=&field_color_value=&keyword_card=&button=%E6%A4%9C+%E7%B4%A2']
    def parse (self, response):
        for details_page_link in response.css('#node-1755 > div > div.mainMiddle > div > table > tbody > tr > td:nth-child(2) > span > a::attr(href)').extract():
            link=response.urljoin(details_page_link)
            yield scrapy.Request(link, callback=self.parse_page)

        next_page = response.urljoin(response.css('#node-1755 > div > div.mainMiddle > div > div > div > div > ul > li:nth-last-child(2) > a::attr(href)').extract_first())
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_page(self, response):
        image_urls = []
        
        for card in response.css("#productInfo"):
            image_path = card.css('div.Images_card > img::attr(src)').get()
            image_urls.append('http://www.p-memories.com' + image_path)
            yield {
                'image_urls': image_urls,
                'image_path': '/'.join(image_path.split("/", 3)[-1:]),
                'card_number': card.css('div.cardDetail > dl:nth-child(1) > dd::text').get(),
                'rarity': card.css('div.cardDetail > dl:nth-child(2) > dd::text').get(),
                'series': card.css('div.cardDetail > dl:nth-child(1) > dt::text').get(),
                'name': card.css('div.cardDetail > dl:nth-child(3) > dd::text').get(),
                'card_type': card.css('div.cardDetail > dl:nth-child(5) > dd::text').get(),
                'cost': card.css('div.cardDetail > dl:nth-child(6) > dd::text').get(),
                'color': card.css('div.cardDetail > dl:nth-child(8) > dd::text').get(),
                'source': card.css('div.cardDetail > dl:nth-child(7) > dd::text').get(),
                'traits': card.css('div.cardDetail > dl:nth-child(9) > dd::text').get(),
                'AP': card.css('div.cardDetail > dl:nth-child(10) > dd::text').get(),
                'DP': card.css('div.cardDetail > dl:nth-child(11) > dd::text').get(),
                'is_foil': card.css('div.cardDetail > dl:nth-child(12) > dd::text').get(),
                'text': card.css('div.cardDetail > dl:nth-child(13) > dd::text').get(),
                'flavor': card.css('div.cardDetail > dl:nth-child(14) > dd::text').get()
            }
            
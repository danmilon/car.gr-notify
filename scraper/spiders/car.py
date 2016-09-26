import urllib.parse
import scrapy
import scraper.items


class CarSpider(scrapy.Spider):
    name = "car"
    allowed_domains = ["car.gr"]
    start_urls = [
        # crete fiat punto (all)
        'http://www.car.gr/used-cars/fiat/punto.html?sort=pra&model1=3367&significant_damage=f&rg=4&condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF&registration=2006-2010&offer_type=sale&price=0-5000&make1=124',
        # attiki fiat punto (all)
        'http://www.car.gr/used-cars/fiat/punto.html?sort=pra&model1=3367&significant_damage=f&rg=3&condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF&registration=2006-2010&offer_type=sale&price=0-5000&make1=124',
        # attiki ford fiesta
        'http://www.car.gr/used-cars/ford/fiesta.html?sort=pra&significant_damage=f&rg=3&registration=2006-2010&offer_type=sale&condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF',
        # crete ford fiesta
        'http://www.car.gr/used-cars/ford/fiesta.html?sort=pra&price=0-5000&significant_damage=f&rg=4&registration=2006-2010&offer_type=sale&condition=%CE%9A%CE%B1%CE%B9%CE%BD%CE%BF%CF%8D%CF%81%CE%B9%CE%BF&condition=%CE%9C%CE%B5%CF%84%CE%B1%CF%87%CE%B5%CE%B9%CF%81%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%BF',
    ]

    def parse(self, response):
        for ad in response.xpath('.//*[@itemprop="vehicle"]'):
            ad_url = ad.xpath('..').css('a::attr(href)')[0].extract()
            ad_url = response.urljoin(ad_url)
            yield scrapy.Request(ad_url, callback=self.parse_ad)

        # next page
        try:
            next_url = response.css('ul.pagination')[0].css('li.active + li')[0].css('a::attr(href)')[0].extract()
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
        except IndexError:
            pass

    def parse_ad(self, response):
        url = response.urljoin(response.url)
        path = urllib.parse.urlparse(url).path
        ad_id = path[1:path.index('-')]
        price = response.xpath('.//*[@itemprop="price"]/text()')[0].extract()

        return scraper.items.CarItem(id=ad_id, url=url)

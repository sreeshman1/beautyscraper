import random
import scrapy
import time
import requests
import logging

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
]
# 2Captcha API key
CAPTCHA_API_KEY = 'your_2captcha_api_key'


def solve_captcha(captcha_url):
    captcha_data = {'key': CAPTCHA_API_KEY, 'method': 'get',
                    'url': captcha_url, 'json': 1}
    response = requests.post('https://2captcha.com/in.php', data=captcha_data)
    captcha_id = response.json().get('request')

    solution_data = {'key': CAPTCHA_API_KEY,
                     'action': 'get', 'id': captcha_id, 'json': 1}
    solution = None
    while not solution:
        response = requests.post(
            'https://2captcha.com/res.php', data=solution_data)
        result = response.json()
        if result.get('status') == 1:
            solution = result.get('request')
        else:
            time.sleep(5)

    return solution


class UltaSpider(scrapy.Spider):
    name = 'ulta'
    start_urls = ['https://www.ulta.com/brand/all#A']
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 10, #Modify this to change the number of concurrent requests
        'DOWNLOAD_DELAY': 3,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': False,
        'RETRY_TIMES': 5,
        'USER_AGENT': random.choice(USER_AGENTS),
        'FEED_EXPORT_FIELDS': ['name', 'brand', 'price', 'ingredients', 'images']
    }

    def parse(self, response):
        try:
            if 'captcha_challenge_page' in response.url:
                captcha_url = response.xpath(
                    '//img[@class="captcha-image"]/@src').get()

                captcha_solution = solve_captcha(captcha_url)

                form_data = {'captcha_field_name': captcha_solution}
                yield scrapy.FormRequest.from_response(response, formdata=form_data, callback=self.parse)

            brand_links = response.xpath(
                "//div[contains(@class, 'ShopAllBrands__brandList')]//a[contains(@class, 'Link_Huge')]/@href").getall()

            #Modify this to change the number of brands to scrape
            for i, brand_url in enumerate(brand_links[:3]):
                yield response.follow(brand_url, self.parse_brand)
        except Exception as e:
            logging.error(f"Error in parse: {e}")

    def parse_brand(self, response):
        try:
            product_links = response.xpath(
                "//ul[contains(@class, 'ProductListingResults__productList')]//a[contains(@class, 'Link_Huge')]/@href").getall()

            for product_url in product_links:
                yield response.follow(product_url, self.parse_product)
        except Exception as e:
            logging.error(f"Error in parse_brand: {e}")

    def parse_product(self, response):
        try:
            product_name = response.xpath(
                "//div[contains(@class, 'ProductInformation')]//span[contains(@class, 'Text-ds--title-5')]/text()").get()
            product_brand = response.xpath(
                "//div[contains(@class, 'ProductInformation')]//a[contains(@class, 'Link_Huge--compact')]/text()").get()
            product_price = response.xpath(
                "//div[contains(@class, 'ProductPricing')]//span[contains(@class, 'Text-ds')]/text()").get()

            if product_name and product_brand and product_price:
                product_ingredients = response.xpath(
                    '//div[contains(@class, "ProductDetail__Content")]//details[@aria-controls="Ingredients"]//p/text()').get()
                product_ingredients = product_ingredients.strip().replace(
                    '\n', '') if product_ingredients else ''

                product_images = response.xpath(
                    "//div[contains(@class, 'MediaWrapper')]//source/@srcset").getall()

                item = {
                    'name': product_name.strip(),
                    'brand': product_brand.strip(),
                    'price': product_price.strip(),
                    'ingredients': product_ingredients,
                    'images': product_images
                }
                yield item
        except Exception as e:
            logging.error(f"Error in parse_product: {e}")

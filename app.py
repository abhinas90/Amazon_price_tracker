import re
import time
import requests
import re
from lxml import html
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class Bot(object):
    asin_check = True

    def __init__(self, asin):
        self.amazon_url = "https://www.amazon.com/dp/"
        self.asin = asin
        headers = {"authority": "www.amazon.com",
                   "method": "GET",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}

        r = requests.get(self.amazon_url + self.asin, headers=headers)
        if r.status_code == 200:
            self.trees = html.fromstring(r.content)
        else:
            Bot.asin_check = False

    def get_product_price(self):
        """Gets and cleans product price from Amazon page.
        If HTML attribute priceblock_ourprice or priceblock_dealprice
        is absent, the price is marked as Not Available."""

        price = "0.0000"

        try:
            price = self.trees.get_element_by_id("priceblock_ourprice").text
        except:
            try:
                price = self.trees.get_element_by_id(
                    "price_inside_buybox").text
            except:
                try:
                    price = self.trees.get_element_by_id(
                        "priceblock_dealprice").text
                except:
                    try:
                        price = self.trees.xpath(
                            "//span[@class='a-color-price']/text()")[0]
                    except:
                        try:
                            price = self.trees.xpath(
                                "//span[@class='a-size-base a-color-price']/text()")[0]
                        except:
                            pass

        non_decimal = re.compile(r'[^\d.]+')
        price = non_decimal.sub('', price)

        return round(float(price[0:5]), 2)

    def get_product_name(self):
        """Returns the product name of the Amazon URL."""

        try:
            product_name = self.trees.get_element_by_id("productTitle").text
        except:
            pass
        if product_name is None:
            product_name = "Not available"
        product_name = product_name.replace("\n", "")
        return product_name

    def get_number_of_sellers(self):
        no_of_sellers = 1
        """Gets Number of seller , if not found returns 1"""
        try:
            span = self.trees.xpath(
                "//span[contains(text(),'New') and contains(text(),'from')]/text()")
            if span:
                extract_num = re.compile(r'[^\d.]+')
                no_of_sellers = extract_num.sub('', span[0])
                return int(no_of_sellers)

        except:
            span = self.trees.xpath(
                "//span[contains(text(),'New & Used')]/text()")
            if span:
                extract_num = re.compile(r'[^\d.]+')
                no_of_sellers = extract_num.sub('', span[0])
                return int(no_of_sellers)
            else:
                span = "1"
                return(span)

    def search_items(self):
        if Bot.asin_check:
            print(f"Searching item {self.asin}")
            price = self.get_product_price()
            name = self.get_product_name()
            url = self.amazon_url + self.asin
            num_of_sellers = self.get_number_of_sellers()

            return price, url, name, num_of_sellers
        else:
            return ("Incorrect_ASIN", "Incorrect_ASIN", "Incorrect_ASIN")


if __name__ == "__main__":
    asin = Bot('B07JXP6RW5')
    print(asin.search_items())

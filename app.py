from selenium import webdriver
import re
import time
import warnings
import os
from selenium.common.exceptions import NoSuchElementException
warnings.filterwarnings("ignore", category=DeprecationWarning)

# op=webdriver.ChromeOptions()
# op.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
# op.add_argument("--headless")
# op.add_argument("--no-sandbox")
# op.add_argument("--disavle-dev-sh-usage")
#
# driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH "),chrome_options=op)


class Bot(object):
    asin_check = True

    def __init__(self, asin):
        self.amazon_url = "https://www.amazon.com/dp/"
        self.asin = asin

        op = webdriver.ChromeOptions()
        op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        op.add_argument("--headless")
        op.add_argument("--no-sandbox")
        op.add_argument("--disavle-dev-sh-usage")
        self.driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH "), chrome_options=op)

        try:
            self.driver.get(self.amazon_url + self.asin)
            self.driver.find_element_by_xpath("//h1[@id='title']").text

        except NoSuchElementException:
            Bot.asin_check = False

    def get_product_price(self):
        """Gets and cleans product price from Amazon page.
        If HTML attribute priceblock_ourprice or priceblock_dealprice
        is absent, the price is marked as Not Available."""

        price = "0.0000"

        try:
            price = self.driver.find_element_by_id("priceblock_ourprice").text
        except:
            try:
                price = self.driver.find_element_by_id(
                    "price_inside_buybox").text
            except:
                try:
                    price = self.driver.find_element_by_id(
                        "priceblock_dealprice").text
                except:
                    try:
                        price = self.driver.find_element_by_xpath(
                            "//span[@class='a-color-price']").text
                    except:
                        try:
                            price = self.driver.find_element_by_xpath(
                                "//span[@class='a-size-base a-color-price']").text
                        except:
                            pass

        non_decimal = re.compile(r'[^\d.]+')
        price = non_decimal.sub('', price)

        return round(float(price[0:5]), 2)

    def get_product_name(self):
        """Returns the product name of the Amazon URL."""

        try:
            product_name = self.driver.find_element_by_id("productTitle").text
        except:
            pass
        if product_name is None:
            product_name = "Not available"
        return product_name

    def get_number_of_sellers(self):
        no_of_sellers = 1
        """Gets Number of seller , if not found returns 1"""
        try:
            xpath = "//span[contains(text(),'New & Used')]"
            span = self.driver.find_element_by_xpath(xpath).text
        except NoSuchElementException:
            try:
                xpath = "//span[contains(text(),'New')]"
                span = self.driver.find_element_by_xpath(xpath).text
            except:
                span = "1"
        extract_num = re.compile(r'[^\d.]+')
        no_of_sellers = extract_num.sub('', span)
        return int(no_of_sellers)

    def search_items(self):
        if Bot.asin_check:
            print(f"Searching item {self.asin}")
            price = self.get_product_price()
            name = self.get_product_name()
            url = self.amazon_url + self.asin
            num_of_sellers = self.get_number_of_sellers()
            self.driver.quit()
            return price, url, name, num_of_sellers
        else:
            return ("Incorrect_ASIN", "Incorrect_ASIN", "Incorrect_ASIN")


asin = Bot('B0881WJFKM')
print(asin.search_items())

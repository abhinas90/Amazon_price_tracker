from app import Bot
import send_email
import pandas as pd
import numpy as n
import time
old_df = pd.read_csv("output.csv")
old_df.fillna(0)
items = old_df["asin"].to_list()

prices, urls, names, num_of_sellers = [], [], [], []
for item in items:
    try:
        amazon_bot = Bot(item)
        price, url, name, num_of_seller = amazon_bot.search_items()
        prices.append(price)
        urls.append(url)
        names.append(name)
        num_of_sellers.append(num_of_seller)
        time.sleep(0.5)
    except:
        print('Incorrect Asin,or product not found')
        prices.append(n.nan)
        urls.append(n.nan)
        names.append("Incorrect Asin,or product not found")


def diff(new_p, old_p):
    """This function will take two prices as arguments
    first: New Price from scraped items
    second: old price from output.csv sheet
    and return their difference """

    change = []
    for np, op in zip(new_p, old_p):
        if (np - op) != 0:
            change.append(np - op)
        else:
            change.append(n.nan)

    return [round(c, 3) for c in change]


# Creating new df with new scapared price , old price and difference
df_new = pd.DataFrame({"asin": items, "price": prices, "url": urls,
                       "name": names, "num_of_seller": num_of_sellers})
df_new["change"] = diff(df_new.price, old_df.price)
df_new["old_price"] = old_df["price"]

df_new["change_sellers"] = diff(df_new.num_of_seller, old_df.num_of_seller)
df_new["old_seller"] = old_df["num_of_seller"]

col = ['asin', 'old_price', 'price', 'change',
       "old_seller", "num_of_seller", 'url', 'name']
df_new = df_new[col]
df_new.to_csv("output.csv", index=False)  # Saving the file to "output.csv"

print("File is Ready to View ")

send_email.sendmail("hellodataworld09@gmail.com", "Goodmorning1*",
                    "abhinas_plp@yahoo.com", "Hello_df", df=df_new ,outputfile=None)

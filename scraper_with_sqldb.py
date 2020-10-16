import database
import sqlite3
from app import Bot
import send_email
import pandas as pd
import numpy as n
import time
from datetime import datetime
from pytz import timezone
import pytz
from sqlalchemy import create_engine


def get_pst_time():
    date_format = '%m-%d-%Y-%H-%M'
    utc_dt = pytz.utc.localize(datetime.utcnow())
    pst_tz = timezone('US/Pacific')
    pst_dt = pst_tz.normalize(utc_dt.astimezone(pst_tz))
    return(pst_dt.strftime(date_format))


cnx = sqlite3.connect('database.db')
old_df = pd.read_sql_query("SELECT * FROM asins_table", cnx)
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
        names.append(n.nan)
        num_of_sellers.append(n.nan)
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

outputfile_name = get_pst_time() + ".csv"
df_new.to_csv(outputfile_name, index=False)


database.deleting_table('asins_table')
print("old table dropped successfully")


# Writing New Df to Database:

engine = create_engine('sqlite:///database.db', echo=True)
sqlite_connection = engine.connect()
df_new.to_sql('asins_table', con=sqlite_connection,
              if_exists='replace', index=False,)

# print(engine.execute("SELECT * FROM asins_table").fetchall())
# cnx.close()


df = pd.read_sql_query("SELECT * FROM asins_table", cnx)
print(df)
cnx.close()

send_email.sendmail("hellodataworld09@gmail.com", "Goodmorning1*",
                    "abhinas_plp@yahoo.com", "Hello_df", df=df_new, outputfile=outputfile_name)

send_email.delete_outputfile(outputfile_name)

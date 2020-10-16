import sqlite3
import pandas as pd
from datetime import datetime
from pytz import timezone
import pytz
conn = sqlite3.connect('database.db')


def create_table():
    with conn:
        conn.executescript("""CREATE TABLE IF NOT EXISTS asins_table(
           asin          VARCHAR(10) NOT NULL PRIMARY KEY
          ,old_price     NUMERIC(5,2)  NULL
          ,price         NUMERIC(5,2)  NULL
          ,change        NUMERIC(6,2)
          ,old_seller    INTEGER   NULL
          ,num_of_seller INTEGER   NULL
          ,url           VARCHAR(36) NULL
          ,name          VARCHAR(500) NULL );""")


def insert_entry():
    with conn:
        conn.executescript(
            """INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B07GH953JN',399.9,399.9,NULL,68,68,'https://www.amazon.com/dp/B07GH953JN','LEGO Harry Potter Hogwarts Castle 71043 Castle Model Building Kit With Harry Potter Figures Gryffindor, Hufflepuff, and more (6,020 Pieces)');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B01EIKRP0K',39.99,39.99,NULL,20,20,'https://www.amazon.com/dp/B01EIKRP0K','Harry Potter Hogwarts Battle Cooperative Deck Building Card Game | Official Harry Potter Licensed Merchandise | Harry Potter Board Game | Great Gift for Harry Potter Fans | Harry Potter Movie artwork');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B0827HSQQJ',249.9,249.9,NULL,38,38,'https://www.amazon.com/dp/B0827HSQQJ','LEGO DC Batman 1989 Batmobile 76139 Building Kit, New 2020 (3,306 Pieces)');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B07Q2N1SJV',88.31,87.31,-1.0,107,111,'https://www.amazon.com/dp/B07Q2N1SJV','LEGO Star Wars: Attack of the Clones Yoda 75255 Yoda Building Model and Collectible Minifigure with Lightsaber (1,771 Pieces)');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B07JXP6RW5',148.9,148.9,NULL,31,31,'https://www.amazon.com/dp/B07JXP6RW5','LEGO Creator Expert Ford Mustang 10265 Building Kit (1471 Pieces)');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B00B9X04F8',89.99,0.0,-89.99,6,6,'https://www.amazon.com/dp/B00B9X04F8','Kemet');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B07PZF5F5P',190.7,190.5,-0.2,36,36,'https://www.amazon.com/dp/B07PZF5F5P','LEGO Technic Land Rover Defender 42110 Building Kit (2573 Pieces)');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('1988884047',57.84,57.84,NULL,19,18,'https://www.amazon.com/dp/1988884047','Roxley Games Brass Birmingham Board Games');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B079T64NS7',53.82,53.82,NULL,11,11,'https://www.amazon.com/dp/B079T64NS7','Shadowrun Crossfire Prime Runner Edition');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B01LZXVN4P',100.8,100.8,NULL,56,55,'https://www.amazon.com/dp/B01LZXVN4P','Gloomhaven');
            INSERT INTO asins_table(asin,old_price,price,change,old_seller,num_of_seller,url,name) VALUES ('B000809OAO',100.8,100.8,NULL,56,55,50,NULL);""")


def add_asin(asins, old_price=None, price=None, change=None, old_seller=None, num_of_seller=None, url=None, name=None):
    with conn:
        if isinstance(asins, (list)):
            for asin in asins:
                conn.execute("INSERT INTO asins_table VALUES(?,?,?,?,?,?,?,?);",
                             (asin, old_price, price, change, old_seller, num_of_seller, url, name))
            print(f"added asins {' '.join([asin for asin in asins])}")

        else:
            conn.execute("INSERT INTO asins_table VALUES(?,?,?,?,?,?,?,?);",
                         (asins, old_price, price, change, old_seller, num_of_seller, url, name))
            print(f"added asin {asins}")


def remove_asin(asins):
    with conn:
        if isinstance(asins, (list)):
            for asin in asins:
                conn.execute("DELETE FROM asins_table WHERE asin=?", (asin,))
            print(f"removed asins {' '.join([asin for asin in asins])}")
        else:
            conn.execute("DELETE FROM asins_table WHERE asin=?", (asins,))
            print(f"removed asin {asins}")


def deleting_table(table_name):
    with conn:
        conn.execute(f"DELETE FROM {table_name};")


# deleting_table('asins_table')
# create_table()
# insert_entry()
# #add_asin(['B07GH953JN', 'B07JXP6RW5'])
# remove_asin(['B07GH953JN', 'B01EIKRP0K', 'B079T64NS7', 'B00B9X04F8',
#             'B0827HSQQJ', 'B07Q2N1SJV', 'B07JXP6RW5', 'B07PZF5F5P'])
# deleting_table('asins_table')
#
#
# cnx = sqlite3.connect('database.db')
# df = pd.read_sql_query("SELECT * FROM asins_table", cnx)
# print(df)
# cnx.close()

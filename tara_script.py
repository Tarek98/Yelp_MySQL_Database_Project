# import pandas as pd
from sqlalchemy import create_engine
from os import sys
import numpy as np

#################################################

# database credentials
username = 'lefteris'
password = 'password'
hostname = '127.0.0.1'
database = 'YELP_DB'

# establish connection to mysql database
engine_string = "mysql+pymysql://"+username+":"+password+"@"+hostname+":"+"2522"+"/"+database+"?charset=utf8mb4"
try:
    engine = create_engine(engine_string)
    print("successful")
except Exception as e:
    print("Error connecting to MySQL DB: " +str(e))
    sys.exit()

engine.connect()

#################################################

# df = pd.read_csv('yelp_review.csv', nrows=100)
# df.drop_duplicates(inplace = True)

# df.head(100).to_sql('yelp_review', engine, if_exists='append', index=False)
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:23:00 2021

@author: Elizabeth Shi

!sudo apt-get install python3-dev default-libmysqlclient-dev
!pip install pymysql
"""


from sqlalchemy import create_engine
import sqlalchemy

import pandas as pd

MYSQL_HOSTNAME = '40.121.198.137'
MYSQL_USER = 'dba'
MYSQL_PASSWORD = 'ahi2021'
MYSQL_DATABASE = 'tempdata'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)

print (engine.table_names())

csvfile = pd.read_csv('https://raw.githubusercontent.com/elizabethshi1/E2E-Final-Assignment/main/H1N1_Flu_Vaccines.csv')
csvfile.to_sql('flu_vaccines', con=engine, if_exists='append')

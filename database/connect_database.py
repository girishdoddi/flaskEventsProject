from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import urllib.parse

USERNAME="girish"
PASSWORD=urllib.parse.quote_plus("7416252855aA@@")
HOSTNAME="functionaldatabase.mysql.database.azure.com"
PORT="3306"
DATABASE="authenticationviaotp"
URL=f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
print(URL)

engine = create_engine(URL)

Session = sessionmaker(bind= engine)
session = Session()
metadata = MetaData()
metadata.reflect(bind= engine)
tables = metadata.tables

for table in tables:
    print(table)
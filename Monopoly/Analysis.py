import pyodbc 
import pandas as pd
import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as plt

from sqlalchemy import create_engine,text

server = '(localdb)\MSSQLLocalDB' 
database = 'MonopolyRecord' 
username = 'test' 
password = 'test' 

connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC Driver 18 for SQL Server"

engine = create_engine(connection_string)
with engine.begin() as conn:
    query = text('SELECT * FROM [dbo].[GameResult]')
    df = pd.read_sql_query(query, conn)



df['ConsumedRoundGroup'] = pd.cut(df['CONSUMEDROUND'], bins=range(0, 601, 10), right=False, labels=range(5, 600, 10))
count_by_range = df['ConsumedRoundGroup'].value_counts(sort=False)


count_by_range.plot(kind='bar')


plt.title('Count of Games by Consumed Round')
plt.xlabel('Consumed Round')
plt.ylabel('Count')


plt.show()


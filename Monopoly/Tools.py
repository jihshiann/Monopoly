import json
import configparser
import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine,text

#config
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

def getParaDictByConfig(paraName):
    paraDict = dict(config.items(paraName))
    # 將所有的 value 轉換為 float
    paraDict = {key: float(value) for key, value in paraDict.items()}
    return paraDict

def getParaListByConfig(paraName, paraType):
    objs = []

   # 取得所有的Section名稱
    sections = config.sections()

    for section in sections:
        if section.startswith(paraName):
            obj = paraType((dict(config.items(section))))
            objs.append(obj)

    return objs

def setConfig(section, attr, value):
    config.set(section, attr, str(value))
    with open(configPath, 'w') as config_file:
        config.write(config_file)


#DB
server = '(localdb)\MSSQLLocalDB' 
database = 'MonopolyRecord' 
username = 'test' 
password = 'test' 
dbConn_pyodbc = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC Driver 18 for SQL Server")

def selectDb(sql):
    with dbConn_pyodbc.cursor() as cursor: 
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows

def insertDb(sql,para_list):
    with dbConn_pyodbc.cursor() as cursor: 
        cursor.execute(sql, para_list)
        dbConn_pyodbc.commit()

def selectBySqlalchemy(sql):
    sql = text(sql)
    with engine.begin() as conn:
        sql = sql
        dataFrame = pd.read_sql_query(sql, conn)
    return dataFrame

def selectPlayerLastBatch():
    sql = '''
          SELECT [PLAYERINFO]
          FROM [dbo].[GameResult]
          WHERE [GAMEBATCH] = (SELECT MAX([GAMEBATCH]) FROM [dbo].[GameResult])
          '''
        
    return selectBySqlalchemy(sql)

def selectLandLastBatch():
    sql = '''
          SELECT [LANDINFO]
          FROM [dbo].[GameResult]
          WHERE [GAMEBATCH] = (SELECT MAX([GAMEBATCH]) FROM [dbo].[GameResult])
          '''
        
    return selectBySqlalchemy(sql)

def selectConsumedRoundLastBatch():
    sql = '''
          SELECT [LANDINFO]
          FROM [dbo].[GameResult]
          WHERE [GAMEBATCH] = (SELECT MAX([GAMEBATCH]) FROM [dbo].[GameResult])
          '''
        
    return selectBySqlalchemy(sql)

#string
def objAryToJson(array):
    return json.dumps(array, default=lambda p: p.__dict__)





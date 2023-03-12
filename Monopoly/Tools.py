import json
import configparser
import os
import pyodbc

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

#DB
server = '(localdb)\MSSQLLocalDB' 
database = 'MonopolyRecord' 
username = 'test' 
password = 'test' 
dbConn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)

def selectDb(sql):
    with dbConn.cursor() as cursor: 
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows

def insertDb(sql,para_list):
    with dbConn.cursor() as cursor: 
        cursor.execute(sql, para_list)
        dbConn.commit()

#string
def objAryToJson(array):
    return json.dumps(array, default=lambda p: p.__dict__)





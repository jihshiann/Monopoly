import configparser
import os

# 取得config
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

# FUN:取得玩家人數 by config
def getNumOfPlayer():
    numOfPlayer = config.getint('Number of players', 'default')
    return numOfPlayer

# FUN:取得土地設定 by config
def getLands():
    lands = []

   # 取得所有的Section名稱
    sections = config.sections()

    for section in sections:
        if section.startswith('Land'):
            land_dict = dict(config.items(section))
            lands.append(land_dict)

    return lands
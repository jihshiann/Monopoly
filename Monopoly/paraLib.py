import configparser
import os

# 取得config
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

# FUN:取得各項費率 by config
def getRateDict():
    rate_dict = dict(config.items('Rate'))
    # 將所有的 value 轉換為 float
    rate_dict = {key: float(value) for key, value in rate_dict.items()}
    return rate_dict

#Land obj
class Land:
    def __init__(self, land_dict):
        self.name = land_dict['name']
        self.price = int(land_dict['price'].strip())
        self.owner = land_dict['owner']
        self.level = int(land_dict['level'].strip())
        self.location = int(land_dict['location'].strip())
        self.invest = int(land_dict['invest'].strip())
# FUN:取得土地設定 by config
def getLands():
    lands = []

   # 取得所有的Section名稱
    sections = config.sections()

    for section in sections:
        if section.startswith('Land'):
            land = Land(dict(config.items(section)))
            lands.append(land)

    return lands

#Player obj
class Player:
    def __init__(self, player_dict):
        self.id = int(player_dict['id'].strip())
        self.money = int(player_dict['money'].strip())
        self.status = int(player_dict['status'].strip())
        self.location = int(player_dict['location'].strip())
# FUN:取得所有玩家資料 by config
def getPlayers():
    players = []

   # 取得所有的Section名稱
    sections = config.sections()

    for section in sections:
        if section.startswith('Player'):
            player_dict = Player(dict(config.items(section)))
            players.append(player_dict)

    return players

# ------未實作------
#import enum

## 執行模式
#class ExecutionMode(enum.Enum):
#    fullyAuto = 0 #連同參數設定皆為自動
#    semiAuto = 1 #使用者輸入參數

#_executionMode= ExecutionMode.fullyAuto

# FUN:初始化執行模式
#def initialize():
#    print("選擇執行模式")
#    print(" 0: 全自動模式(包含參數設定)")
#    print(" 1: 由使用者輸入參數")

#    #print("五秒內未輸入則為自動模式")
#    #start_time = time.time()
#    #while (time.time() - start_time) < 5:
#    #    if m:=input("請輸入0 or 1"):
#    #        userInput = m
#    #        break
#    #    else:
#    #        userInput = "0"

#    userInput=input("請輸入0 or 1\n")
#    if userInput == "0":
#        _executionMode = ExecutionMode.fullyAuto
#    elif userInput == "1":
#        _executionMode = ExecutionMode.semiAuto
#    else :
#        print("終止程式")
#        exit()

#    print(_executionMode)

# 初始化
#initialize()
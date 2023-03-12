import configparser
import os
import random
import pyodbc
from py_linq import Enumerable

server = '(localdb)\MSSQLLocalDB' 
database = 'MonopolyRecord' 
username = 'test' 
password = 'test' 
dbConn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)


#取得config
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)
#全域變數
loserCount = 0
global rate_dict 
rate_dict = {key: float(value) for key, value in dict(config.items('Rate')).items()}

#FUN:取得各項費率 by config
def getRateDict():
    rate_dict = dict(config.items('Rate'))
    # 將所有的 value 轉換為 float
    rate_dict = {key: float(value) for key, value in rate_dict.items()}
    return rate_dict

#Land
class Land:
    def __init__(self, land_dict):
        self.name = land_dict['name']
        self.price = int(land_dict['price'].strip())
        self.owner = land_dict['owner']
        self.level = int(land_dict['level'].strip())
        self.location = int(land_dict['location'].strip())
        self.upgradeSpent = int(land_dict['upgradespent'].strip()) #升級花費總額
        self.earn = int(land_dict['earn'].strip()) #過路費總收入

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

#Player
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

#ACTION
#FUN: player move
def playerMove(player, landLen):
    player.location = player.location + random.randint(1, 4)
    if player.location > landLen:
        player.location = player.location % landLen

#FUN: buy or do nothing
def buyOrPass(player, arriveLand):
    cost = arriveLand.price + arriveLand.upgradeSpent
     #判斷現金是否足夠購買
    if player.money >= cost:
        player.money -= cost
        arriveLand.owner = player.id

#FUN: upgrade or do nothing
def upgradeOrPass(player, arriveLand):
    #算式: price * rate * level
    cost = rate_dict['upgrade'] * arriveLand.price * arriveLand.level
    #判斷現金是否足夠升級
    if player.money >= cost:
        player.money -= cost
        arriveLand.level += 1
        arriveLand.upgradeSpent += cost

#FUN: pay toll
def payToll(player, payee, arriveLand, lands):
    #算式: price * rate * level
    toll = rate_dict['toll'] * arriveLand.price * arriveLand.level
    arriveLand.earn += toll
    #現金充足
    if player.money >= toll:
        payee.money += toll
        player.money -= toll
    
    #現金不足
    else:
        #先付清現金
        payee.money += player.money
        toll -=player.money
        player.money = 0
        playerLands = list(filter(lambda l: l.owner == player.id, lands))
        
        #無地則破產
        if playerLands == None:
            lose(player)
            return

        #計算總資產
        playerLands.sort(key = lambda l: l.upgradeSpent + l.price)
        totalPrice = 0
        for land in playerLands:
            totalPrice += (land.upgradeSpent + land.price)

        #不足額則破產
        if totalPrice < toll:
            for land in playerLands:
                land.owner = payee.id
            lose(player)
            return

        #從最便宜地產開始清算以支付費用
        for land in playerLands:
            while player.money < toll:
                land.owner = 'None'
                toll -= (land.upgradeSpent + land.price)
                payee.money += (land.upgradeSpent + land.price)
        if toll < 0:
            player.money += abs(toll)
            payee.money -= abs(toll)

#FUN: go bankrupt
def lose(player):
    player.status = 1
    global loserCount
    loserCount += 1

#FUN: DB
#gameBatch: 第幾批次執行; gameNumber: 同一批次第幾局; consumedRound: 幾回合結束
#playerInfo; 結束時各玩家資訊(json string); landInfo:結束時各土地資訊(json string)
class GameResult:
    def __init__(self, gameBatch=0, gameNumber=0, consumedRound=0, playerInfo='', landInfo=''):
        self.gameBatch = gameBatch
        self.gameNumber = gameNumber
        self.consumedRound = consumedRound
        self.playerInfo = playerInfo
        self.landInfo = landInfo
def insertGameResult(result):
    sql = """
         INSERT INTO GameResult 
            (GAMEBATCH, GAMENUMBER, CONSUMEDROUND, PLAYERINFO, LANDINFO)
            VALUES (?, ?, ?, ?, ?)
         """
    cursor = dbConn.cursor()  
    cursor.execute(sql, (result.gameBatch, result.gameNumber, result.consumedRound, result.playerInfo, result.landInfo))
    dbConn.commit()
    dbConn.close()


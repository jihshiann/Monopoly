import random
from Tools import *


#全域變數
loserCount = 0
global rate_dict; rate_dict = getParaDictByConfig('Rate')

class Land:
    def __init__(self, land_dict):
        self.name = land_dict['name']
        self.price = int(land_dict['price'].strip())
        self.owner = land_dict['owner']
        self.level = int(land_dict['level'].strip())
        self.location = int(land_dict['location'].strip())
        #升級花費總額
        self.upgradeSpent = int(land_dict['upgradespent'].strip()) 
        #過路費總收入
        self.earn = int(land_dict['earn'].strip()) 

# FUN:取得土地設定 by config
def getLands():
    lands =  getParaListByConfig('Land', Land)
    return lands

class Player:
    def __init__(self, player_dict):
        self.id = int(player_dict['id'].strip())
        self.money = int(player_dict['money'].strip())
        self.status = int(player_dict['status'].strip())
        self.location = int(player_dict['location'].strip())
# FUN:取得所有玩家資料 by config
def getPlayers():
    players =  getParaListByConfig('Player', Player)
    return players


#Game action
#FUN: 初始化遊戲參數 by config
def Initialize():
    # 取得所有玩家資料
    players = getPlayers()
    # 取得所有土地資料
    lands = getLands()
    
    global loserCount
    loserCount = 0

    return players, lands, rate_dict

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
def getLoserCount():
    return loserCount

#DB
#每一批次參數相同，一批次跑千局遊戲
class GameSetting:
    def __init__(self, gameBatch=0, rates='', players='', lands=''):
        #第幾批次執行
        self.gameBatch = gameBatch
        #費率設定
        self.rates = rates
        #玩家起始設定
        self.players = players
        #土地起始設定
        self.lands = lands
# Select last batch from gameSetting
def getLastBatchNum():
    sql = """
          SELECT TOP 1 GAMEBATCH
          FROM GAMESETTING
          ORDER BY GAMEBATCH DESC
          """
    row = selectDb(sql)
    batchNum = row[0][0] if row else 0
    return batchNum
#Insert Table(GameResult)
def recordSetting(setting):
    sql = """
         INSERT INTO GAMESETTING 
         (GAMEBATCH, RATES, PLAYERS, LANDS)
         VALUES (?, ?, ?, ?)
         """
    para_list = [setting.gameBatch, setting.rates, setting.players, setting.lands]
    insertDb(sql, para_list)

class GameResult:
    def __init__(self, gameBatch=0, gameNumber=0, consumedRound=0, playerInfo='', landInfo=''):
        #第幾批次執行
        self.gameBatch = gameBatch
        #同一批次第幾局
        self.gameNumber = gameNumber
        #幾回合結束
        self.consumedRound = consumedRound
        #結束時各玩家資訊(json string)
        self.playerInfo = playerInfo
        #結束時各土地資訊(json string)
        self.landInfo = landInfo
#InsertTable(GameResult)
def recordResult(result):
    sql = """
         INSERT INTO GAMERESULT 
            (GAMEBATCH, GAMENUMBER, CONSUMEDROUND, PLAYERINFO, LANDINFO)
            VALUES (?, ?, ?, ?, ?)
         """
    para_list = [result.gameBatch, result.gameNumber, result.consumedRound, result.playerInfo, result.landInfo]
    insertDb(sql, para_list)


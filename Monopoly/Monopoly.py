from Lib import *
from Tools import *
import json

#第幾局遊戲
gameNum = 0
while gameNum < 10000:
    players, lands, rate_dict = Initialize()
    
    if gameNum == 0:
        #取得遊戲批號，同一批代表參數相同
        thisBatch = getLastBatchNum() + 1
        #記錄遊戲起始設定
        setting = GameSetting(thisBatch, json.dumps(rate_dict), objAryToJson(players), objAryToJson(lands))
        recordSetting(setting)

    gameNum += 1
    #第幾輪
    roundCount = 0
    #遊玩中玩家>1位
    while getLoserCount() < len(players)- 1:
        roundCount += 1
        for player in players:
            #1 = lose
            if player.status == 1:
                continue

            #0 = play
            if player.status == 0:
                #向前走1~4步
                playerMove(player, len(lands))
                arriveLand = lands[player.location-1]
            
                #無主地
                if arriveLand.owner == 'None':
                    #買地
                    buyOrPass(player, arriveLand)

                #自有土地
                elif arriveLand.owner == player.id:
                    #升級
                    upgradeOrPass(player, arriveLand)

                #他人土地
                else:
                    #接受過路費對象(地主)
                    payee = players[arriveLand.owner-1] 
                    #繳過路費
                    payToll(player, payee, arriveLand, lands)

    result = GameResult(thisBatch, gameNum, roundCount, objAryToJson(players), objAryToJson(lands)) 
    recordResult(result)
    print(f'gameNum:{gameNum}結束')
    





from Lib import *
import Lib
import json


roundCount = 0
#取得所有玩家資料
players = getPlayers()
#取得所有土地資料
lands = getLands()
#取得各項費率
rate_dict = getRateDict()

#遊玩中玩家>1位
while Lib.loserCount < len(players)- 1:
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

    print(f"round = {roundCount} 結束")
    print(json.dumps(players, default=lambda p: p.__dict__))
    print()
    print(json.dumps(lands, default=lambda p: p.__dict__))

result = GameResult(1, 1, roundCount, json.dumps(players, default=lambda p: p.__dict__), json.dumps(lands, default=lambda p: p.__dict__)) 
insertGameResult(result)
    





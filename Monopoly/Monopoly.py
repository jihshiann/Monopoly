from textwrap import indent
from paraLib import *
import random
import json


#取得所有玩家資料
players = getPlayers()
#取得所有土地資料
lands = getLands()
#取得各項費率
rate_dict = getRateDict()

loserCount = 0
round = 0

#遊玩中玩家>1位
while loserCount < len(players)- 1:
    round += 1
    for player in players:
        #1 = lose
        if player.status == 1:
            continue
        #0 = play
        if player.status == 0:
            #向前走1~4步
            player.location = player.location + random.randint(1, 4)
            if player.location > len(lands):
                player.location = player.location % len(lands)
            arriveLand = lands[player.location-1]
            #判斷土地持有權
            if arriveLand.owner == 'None':
                #判斷現金是否足夠購買
                if player.money >= arriveLand.price:
                    player.money -= arriveLand.price
                    arriveLand.owner = player.id
                    arriveLand.level += 1
                    arriveLand.invest += arriveLand.price
            
            elif arriveLand.owner == player.id:
                #公式: price * rate * level
                upgradeCost = rate_dict['upgrade'] * arriveLand.price * arriveLand.level
                #判斷現金是否足夠升級
                if player.money >= upgradeCost:
                    player.money -= upgradeCost
                    arriveLand.level += 1
                    arriveLand.invest += upgradeCost

            else:
                #公式 price * rate * level
                toll = rate_dict['toll'] * arriveLand.price * arriveLand.level
                payee = players[arriveLand.owner-1] #接受過路費對象(地主)
                #判斷現金是否足夠付過路費
                if player.money >= toll:
                    payee.money += toll
                    player.money -= toll
                else:
                    #先付清現金
                    payee.money += player.money
                    toll -=player.money
                    player.money = 0
                    playerLands = list(filter(lambda l: l.owner == player.id, lands))
                    #無地則破產
                    if playerLands == None:
                        player.status = 1
                        loserCount += 1
                        continue

                    playerLands.sort(key = lambda l: l.invest)
                    totalPrice = 0
                    for land in playerLands:
                        totalPrice += land.invest
                    #判斷持有土地總價是否足夠支付，不夠則全數轉移且破產
                    if totalPrice < toll:
                        for land in playerLands:
                            land.owner = payee.id
                        player.status = 1
                        loserCount += 1
                        continue
                    #賣地給地主
                    for land in playerLands:
                        while player.money < toll:
                            land.owner = payee.id
                            toll -= land.invest
                    if toll < 0:
                        player.money += abs(toll)
                        payee.money -= toll

    print(f"round = {round} 結束")
    print(json.dumps(players, default=lambda p: p.__dict__, indent = 4))
    print()
    print(json.dumps(lands, default=lambda p: p.__dict__, indent = 4))

print(f"Game over, round = {round}")
    





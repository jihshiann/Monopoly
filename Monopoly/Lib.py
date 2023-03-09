import configparser
import os
import random

#���oconfig
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

loserCount = 0
global rate_dict 
rate_dict = {key: float(value) for key, value in dict(config.items('Rate')).items()}

#FUN:���o�U���O�v by config
def getRateDict():
    rate_dict = dict(config.items('Rate'))
    # �N�Ҧ��� value �ഫ�� float
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
        self.upgradeSpent = int(land_dict['upgradespent'].strip()) #�g�a�`�ɯŪ�O
        self.earn = int(land_dict['earn'].strip()) #�g�a�`����O���J

# FUN:���o�g�a�]�w by config
def getLands():
    lands = []

   # ���o�Ҧ���Section�W��
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

# FUN:���o�Ҧ����a��� by config
def getPlayers():
    players = []

   # ���o�Ҧ���Section�W��
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
     #�P�_�{���O�_�����ʶR
    if player.money >= cost:
        player.money -= cost
        arriveLand.owner = player.id

#FUN: upgrade or do nothing
def upgradeOrPass(player, arriveLand):
    #����: price * rate * level
    cost = rate_dict['upgrade'] * arriveLand.price * arriveLand.level
    #�P�_�{���O�_�����ɯ�
    if player.money >= cost:
        player.money -= cost
        arriveLand.level += 1
        arriveLand.upgradeSpent += cost

#FUN: pay for toll
def payForToll(player, payee, arriveLand, lands):
    #���� price * rate * level
    toll = rate_dict['toll'] * arriveLand.price * arriveLand.level
    arriveLand.earn += toll
    #�{���R��
    if player.money >= toll:
        payee.money += toll
        player.money -= toll
    
    #�{������
    else:
        #���I�M�{��
        payee.money += player.money
        toll -=player.money
        player.money = 0
        playerLands = list(filter(lambda l: l.owner == player.id, lands))
        
        #�L�a�h�}��
        if playerLands == None:
            lose(player)
            return

        #�M��a��
        playerLands.sort(key = lambda l: l.upgradeSpent + l.price)
        totalPrice = 0
        for land in playerLands:
            totalPrice += land.upgradeSpent + land.price

        #�a�������B�h�}��
        if totalPrice < toll:
            for land in playerLands:
                land.owner = payee.id
            lose(player)
            return

        #��a���
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


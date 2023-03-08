import configparser
import os

# ���oconfig
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

# FUN:���o�U���O�v by config
def getRateDict():
    rate_dict = dict(config.items('Rate'))
    # �N�Ҧ��� value �ഫ�� float
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

#Player obj
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

# ------����@------
#import enum

## ����Ҧ�
#class ExecutionMode(enum.Enum):
#    fullyAuto = 0 #�s�P�ѼƳ]�w�Ҭ��۰�
#    semiAuto = 1 #�ϥΪ̿�J�Ѽ�

#_executionMode= ExecutionMode.fullyAuto

# FUN:��l�ư���Ҧ�
#def initialize():
#    print("��ܰ���Ҧ�")
#    print(" 0: ���۰ʼҦ�(�]�t�ѼƳ]�w)")
#    print(" 1: �ѨϥΪ̿�J�Ѽ�")

#    #print("��������J�h���۰ʼҦ�")
#    #start_time = time.time()
#    #while (time.time() - start_time) < 5:
#    #    if m:=input("�п�J0 or 1"):
#    #        userInput = m
#    #        break
#    #    else:
#    #        userInput = "0"

#    userInput=input("�п�J0 or 1\n")
#    if userInput == "0":
#        _executionMode = ExecutionMode.fullyAuto
#    elif userInput == "1":
#        _executionMode = ExecutionMode.semiAuto
#    else :
#        print("�פ�{��")
#        exit()

#    print(_executionMode)

# ��l��
#initialize()
import configparser
import os

# ���oconfig
config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

# FUN:���o���a�H�� by config
def getNumOfPlayer():
    numOfPlayer = config.getint('Number of players', 'default')
    return numOfPlayer

# FUN:���o�g�a�]�w by config
def getLands():
    lands = []

   # ���o�Ҧ���Section�W��
    sections = config.sections()

    for section in sections:
        if section.startswith('Land'):
            land_dict = dict(config.items(section))
            lands.append(land_dict)

    return lands
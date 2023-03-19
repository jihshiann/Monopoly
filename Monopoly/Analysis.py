from Tools import *
import pandas as pd
import json
import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as plt
import numpy as np

def countRoundConsumed():
    sql =   '''
            SELECT [CONSUMEDROUND]
            FROM [dbo].[GameResult]
            WHERE [GAMEBATCH] = (SELECT MAX([GAMEBATCH]) FROM [dbo].[GameResult])
            '''
    df = selectBySqlalchemy(sql)

    #��Ƥ���
    df['ConsumedRoundGroup'] = pd.cut(df['CONSUMEDROUND'], bins=range(0, 601, 10), right=False, labels=range(5, 600, 10))
    #�p����ռƶq
    countByRange = df['ConsumedRoundGroup'].value_counts(sort=False)
    return countByRange

def calculateWinRate():
    df = selectPlayerLastBatch()
    
    #�q�Ĥ@���C������ PLAYERINFO ��������a ID
    player_set = {player['id'] for player in json.loads(df.PLAYERINFO.iloc[0])}

    #�p��C�Ӫ��a���ӧQ����; wins = dictionary(player_id, 0)
    wins = {playerId: 0 for playerId in player_set}
    for playerInfo_list in df['PLAYERINFO'].apply(json.loads):
        for player in playerInfo_list:
            if player['status'] == 0:
                wins[player['id']] += 1

    # �إߤ@�� pandas DataFrame�A�s�x�C�Ӫ��a�� ID �M�ӧQ����
    playerWin_df = pd.DataFrame({"player_id": list(wins.keys()), "win_count": list(wins.values())})

    # �p��C�Ӫ��a���Ӳv
    playerWin_df['win_rate'] = playerWin_df['win_count'] / playerWin_df['win_count'].sum()

    # �]�m���Ϫ�����
    labels = [f'Player {id}' for id in playerWin_df['player_id']]
    
    return  playerWin_df['win_rate'], labels
def drawPieChart(df, labels, title):
    colors = plt.cm.Set2(range(len(df)))

    # ø�s����
    fig, ax = plt.subplots()
    ax.pie(df, labels=labels, colors=colors, autopct='%1.1f%%')
    ax.set_title(title)
    plt.show()
def checkWinRate():
    winRate_df, labels = calculateWinRate()
    winRate = {player+1:rate for player,rate in enumerate(winRate_df)}
    avgRate = 1/len(winRate)
    return max(winRate.values()) - min(winRate.values()) <= avgRate / len(winRate)

def calcBankruptcyProbBy():
    df = selectPlayerLastBatch()
    #bankruptcyCount= {location1: count1, location2: count2, ...}
    bankruptcyCount = {}
    for playerInfo_list in df['PLAYERINFO'].apply(json.loads):
        for player in playerInfo_list:
            if player['status'] == 1:
                location = player['location']
                bankruptcyCount[location] = bankruptcyCount.get(location, 0) + 1
    bankruptcy_df = pd.DataFrame({"local_id": list(bankruptcyCount.keys()), "bankruptcy_count": list(bankruptcyCount.values())})
    bankruptcy_df['prob'] = bankruptcy_df['bankruptcy_count'] / len(df)

    return bankruptcy_df
def plotBarChart(df=None, dfx=None, dfy=None, title='', x='', y=''):
    if df is not None:
        df.plot(kind='bar')
    elif dfx is not None and dfy is not None:
        plt.bar(dfx, dfy)
    else:
        raise ValueError("Missing data for the bar chart.")
    
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()
def checkBankruptcyProb(bankruptcy_df):
    bankruptcyProb = {i+1:land for i,land in enumerate(bankruptcy_df)}
    avgRate = 3/len(bankruptcy_df)
    return max( bankruptcy_df['prob']) - min( bankruptcy_df['prob']) <= avgRate / len(bankruptcyProb)

def landInfoStatistic():
    sql =   '''
            SELECT [LANDINFO]
            FROM [dbo].[GameResult]
            WHERE [GAMEBATCH] = (SELECT MAX([GAMEBATCH]) FROM [dbo].[GameResult])
            '''
    land_df = selectBySqlalchemy(sql)
    landInfos = land_df['LANDINFO'].apply(json.loads)

    # �q landInfos �����o���
    landData = {}
    for landInfo in landInfos:
        for land in landInfo:
            location = land['location']
            if location not in landData:
                landData[location] = {
                    'name': f"{location} {land['name']}",
                    'prices': {land['price']},
                    'levels': [],
                    'upgradeSpents': [],
                    'earns': []
                }
            landData[location]['levels'].append(land['level']*10)
            landData[location]['upgradeSpents'].append(land['upgradeSpent'])
            landData[location]['earns'].append(land['earn'])

    # �p��U��������
    prices = []
    avg_levels = []
    avg_upgrades = []
    avg_earns = []
    locationAndName = []
    for location in sorted(landData.keys()):
        prices.append(landData[location]['prices'].pop())
        avg_levels.append(np.mean(landData[location]['levels']))
        avg_upgrades.append(np.mean(landData[location]['upgradeSpents']))
        avg_earns.append(np.mean(landData[location]['earns']))
        locationAndName.append(landData[location]['name'])
    
    landsResultInfo = {}
    landsResultInfo['locationAndName'] = locationAndName
    landsResultInfo['prices'] = prices
    landsResultInfo['avg_levels'] = avg_levels
    landsResultInfo['avg_upgrades'] = avg_upgrades
    landsResultInfo['avg_earns'] = avg_earns
    
    return landsResultInfo

def plotLandsResultBarChart(landsResultInfo):
    # �إ� X �b��� (location + name)
    x_data = np.arange(len(landsResultInfo['locationAndName']))

    # �]�w�Ϫ�j�p
    fig, ax = plt.subplots(figsize=(16, 8))

    # ø�s�U�������Ȫ�������
    width = 0.2
    ax.bar(x_data - 3*width, landsResultInfo['prices'] , width=width, label='Price')
    ax.bar(x_data - 2*width, landsResultInfo['avg_levels'], width=width, label='Avg. Level * 10')
    ax.bar(x_data - 1*width, landsResultInfo['avg_upgrades'], width=width, label='Avg. Upgrade Spent')
    ax.bar(x_data, landsResultInfo['avg_earns'], width=width, label='Avg. Earn')

    # �]�w�Ϫ���D�ζb����
    ax.set_title("Lands for game results", fontsize=18)
    ax.set_xlabel("Land", fontsize=14)
    ax.set_ylabel("Value", fontsize=14)

    # �]�w X �b��׼���
    ax.set_xticks(x_data- 1.5*width)
    ax.set_xticklabels(landsResultInfo['locationAndName'], rotation=90, fontsize=10)

    # �]�w�Ϩ�
    ax.legend()

    # ��ܹϪ�
    plt.show()

def calcNeverEarnedLandProb():
    df = selectLandLastBatch()
    #neverEarnedCount = {location1: count1, location2: count2, ...}
    neverEarnedCount = {}
    for landInfo_list in df['LANDINFO'].apply(json.loads):
        for land in landInfo_list:
            if land['earn'] == 0:
                location = land['location']
                neverEarnedCount[location] = neverEarnedCount.get(location, 0) + 1
    neverEarned_df = pd.DataFrame({"local_id": list(neverEarnedCount.keys()), "neverEarned_count": list(neverEarnedCount.values())})
    neverEarned_df['prob'] = neverEarned_df['neverEarned_count'] / len(df)

    return neverEarned_df
def checkNeverEarnedProb(neverEarned_df):
    neverEarnedProb = {i+1:land for i,land in enumerate(neverEarned_df)}
    avgRate = 1/len(neverEarned_df)
    return max(neverEarned_df['prob']) - min(neverEarned_df['prob']) <= avgRate / len(neverEarnedProb)

##���Ӧ^�X��
#roundConsumed_df = countRoundConsumed()
#plotBarChart(roundConsumed_df, None, None, 'Consumed Rounds Count', 'Consumed Round', 'Count')
##���a�Ӳv
#winRate_df, labels = calculateWinRate()
#drawPieChart(winRate_df, labels, 'Win percentages by player')
##�U�a�}����v
#bankruptcy_df = calcBankruptcyProbBy()
#plotBarChart(None, bankruptcy_df['local_id'], bankruptcy_df['prob'], 'Bankruptcy probability by location', 'location', 'probability')
##�U�a�L���J���v
#neverEarned_df = calcNeverEarnedLandProb()
#plotBarChart(None, neverEarned_df['local_id'], neverEarned_df['prob'], 'Probability of land no income', 'location', 'probability')
###�C�������ɦU�a�ƭȲέp
#landsResultInfo = landInfoStatistic()
#plotLandsResultBarChart(landsResultInfo)
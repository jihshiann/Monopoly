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

    #資料分組
    df['ConsumedRoundGroup'] = pd.cut(df['CONSUMEDROUND'], bins=range(0, 601, 10), right=False, labels=range(5, 600, 10))
    #計算分組數量
    countByRange = df['ConsumedRoundGroup'].value_counts(sort=False)
    return countByRange

def calculateWinRate():
    df = selectPlayerLastBatch()
    
    #從第一場遊戲中的 PLAYERINFO 中獲取玩家 ID
    player_set = {player['id'] for player in json.loads(df.PLAYERINFO.iloc[0])}

    #計算每個玩家的勝利次數; wins = dictionary(player_id, 0)
    wins = {playerId: 0 for playerId in player_set}
    for playerInfo_list in df['PLAYERINFO'].apply(json.loads):
        for player in playerInfo_list:
            if player['status'] == 0:
                wins[player['id']] += 1

    # 建立一個 pandas DataFrame，存儲每個玩家的 ID 和勝利次數
    playerWin_df = pd.DataFrame({"player_id": list(wins.keys()), "win_count": list(wins.values())})

    # 計算每個玩家的勝率
    playerWin_df['win_rate'] = playerWin_df['win_count'] / playerWin_df['win_count'].sum()

    # 設置圓餅圖的標籤
    labels = [f'Player {id}' for id in playerWin_df['player_id']]
    
    return  playerWin_df['win_rate'], labels
def drawPieChart(df, labels, title):
    colors = plt.cm.Set2(range(len(df)))

    # 繪製圓餅圖
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

    # 從 landInfos 中取得資料
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

    # 計算各項平均值
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
    # 建立 X 軸資料 (location + name)
    x_data = np.arange(len(landsResultInfo['locationAndName']))

    # 設定圖表大小
    fig, ax = plt.subplots(figsize=(16, 8))

    # 繪製各項平均值的長條圖
    width = 0.2
    ax.bar(x_data - 3*width, landsResultInfo['prices'] , width=width, label='Price')
    ax.bar(x_data - 2*width, landsResultInfo['avg_levels'], width=width, label='Avg. Level * 10')
    ax.bar(x_data - 1*width, landsResultInfo['avg_upgrades'], width=width, label='Avg. Upgrade Spent')
    ax.bar(x_data, landsResultInfo['avg_earns'], width=width, label='Avg. Earn')

    # 設定圖表標題及軸標籤
    ax.set_title("Lands for game results", fontsize=18)
    ax.set_xlabel("Land", fontsize=14)
    ax.set_ylabel("Value", fontsize=14)

    # 設定 X 軸刻度標籤
    ax.set_xticks(x_data- 1.5*width)
    ax.set_xticklabels(landsResultInfo['locationAndName'], rotation=90, fontsize=10)

    # 設定圖例
    ax.legend()

    # 顯示圖表
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

##消耗回合數
#roundConsumed_df = countRoundConsumed()
#plotBarChart(roundConsumed_df, None, None, 'Consumed Rounds Count', 'Consumed Round', 'Count')
##玩家勝率
#winRate_df, labels = calculateWinRate()
#drawPieChart(winRate_df, labels, 'Win percentages by player')
##各地破產比率
#bankruptcy_df = calcBankruptcyProbBy()
#plotBarChart(None, bankruptcy_df['local_id'], bankruptcy_df['prob'], 'Bankruptcy probability by location', 'location', 'probability')
##各地無收入機率
#neverEarned_df = calcNeverEarnedLandProb()
#plotBarChart(None, neverEarned_df['local_id'], neverEarned_df['prob'], 'Probability of land no income', 'location', 'probability')
###遊戲結束時各地數值統計
#landsResultInfo = landInfoStatistic()
#plotLandsResultBarChart(landsResultInfo)
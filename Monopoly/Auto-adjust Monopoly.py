import Monopoly as Monopoly
import Analysis as Analysis
import Lib as Lib


def balanceWinRate():
    # 調整起始金額
    Lib.adjustPlayersMoney(Lib.getPlayers())
    # 執行遊戲10000局
    Monopoly.play(10000)

def balanceLand():
    # 調整土地金額
    Lib.adjustLandMoney(max(Lib.getLands(), key=lambda l: l.price))
    # 執行遊戲10000局
    Monopoly.play(10000)
    

while True:
    if Lib.getLastBatchNum() == 0:
        Monopoly.play(10000)
    # 檢查各玩家勝率是否異常
    if Analysis.checkWinRate():
        # 檢查無收入機率是否異常
        if Analysis.checkNeverEarnedProb(Analysis.calcNeverEarnedLandProb()):
            # 檢查破產機率是否異常
            if Analysis.checkBankruptcyProb(Analysis.calcBankruptcyProbBy()):
                 # 全部參數都正常，結束流程
                break
            else: 
                print('Bankruptcy Prob abnormal')
                balanceLand()
        else:
            print('Never Earned Prob abnormal')
            balanceLand()
    else:
        print('Win Rate abnormal')
        balanceWinRate()



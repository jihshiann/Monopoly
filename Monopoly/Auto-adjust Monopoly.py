import Monopoly as Monopoly
import Analysis as Analysis
import Lib as Lib


def balanceWinRate():
    # �վ�_�l���B
    Lib.adjustPlayersMoney(Lib.getPlayers())
    # ����C��10000��
    Monopoly.play(10000)

def balanceLand():
    # �վ�g�a���B
    Lib.adjustLandMoney(max(Lib.getLands(), key=lambda l: l.price))
    # ����C��10000��
    Monopoly.play(10000)
    

while True:
    if Lib.getLastBatchNum() == 0:
        Monopoly.play(10000)
    # �ˬd�U���a�Ӳv�O�_���`
    if Analysis.checkWinRate():
        # �ˬd�L���J���v�O�_���`
        if Analysis.checkNeverEarnedProb(Analysis.calcNeverEarnedLandProb()):
            # �ˬd�}�����v�O�_���`
            if Analysis.checkBankruptcyProb(Analysis.calcBankruptcyProbBy()):
                 # �����ѼƳ����`�A�����y�{
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



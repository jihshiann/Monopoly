import Monopoly as Game
import Analysis as Anlys
import Library as Lib


def balanceWinRate():
    # �վ�_�l���B
    Lib.adjustPlayersMoney(Lib.getPlayers())
    # ����C��10000��
    Game.play(10000)

def balanceLand():
    # �վ�g�a���B
    Lib.adjustLandMoney(max(Lib.getLands(), key=lambda l: l.price))
    # ����C��10000��
    Game.play(10000)
    

while True:
    if Lib.getLastBatchNum() == 0:
        Game.play(10000)
    # �ˬd�U���a�Ӳv�O�_���`
    if Anlys.checkWinRate():
        # �ˬd�L���J���v�O�_���`
        if Anlys.checkNeverEarnedProb(Anlys.calcNeverEarnedLandProb()):
            # �ˬd�}�����v�O�_���`
            if Anlys.checkBankruptcyProb(Anlys.calcBankruptcyProbBy()):
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



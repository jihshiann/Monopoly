import enum
from paraLib import *

# 執行模式
class ExecutionMode(enum.Enum):
    fullyAuto = 0 #連同參數設定皆為自動
    semiAuto = 1 #使用者輸入參數

_executionMode= ExecutionMode.fullyAuto

# FUN:初始化執行模式
def initialize():
    print("選擇執行模式")
    print(" 0: 全自動模式(包含參數設定)")
    print(" 1: 由使用者輸入參數")

    #print("五秒內未輸入則為自動模式")
    #start_time = time.time()
    #while (time.time() - start_time) < 5:
    #    if m:=input("請輸入0 or 1"):
    #        userInput = m
    #        break
    #    else:
    #        userInput = "0"

    userInput=input("請輸入0 or 1\n")
    if userInput == "0":
        _executionMode = ExecutionMode.fullyAuto
    elif userInput == "1":
        _executionMode = ExecutionMode.semiAuto
    else :
        print("終止程式")
        exit()

    print(_executionMode)

# 初始化
initialize()
# 取得玩家人數
getNumOfPlayer()
# 取得所有土地資料
getLands()




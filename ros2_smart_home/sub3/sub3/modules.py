import math

def checkCurrStage(stage):
    ret = 0
    while(stage%2!=0):
        ret+=1
        stage = int(stage/2)
    return ret

def getCurrStage(stageNum):
    ret = 0
    idx = 0
    while(stageNum>0):
        ret += int(math.pow(2, idx))
        idx+=1
        stageNum-=1
    return ret

def checkUDPstage(stage):
    ret = 0
    while stage%2==0 :
        ret+=1
        stage = (stage>>1) | (1<<15)
    return ret

def getUDPstage(num):
    ret = ~getCurrStage(num)
    return ret

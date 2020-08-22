import time
import sys, os, re
from datetime import datetime, date
import time

#-------------------------GLOBALS--------------------------#
root = "IPC4100_2"
elapsedTime=[]
#reg expressions used to find specific lines
startTimereg=r"27_\w\tIPC Network Change Reboot\t\d\d:\d\d:\d\d\t\w\w\w\w\w\w"
endPassReg=r"28\tPA Proxy Activate UUT\t\d\d:\d\d:\d\d\tPassed"
endFailReg=r"28\tPA Proxy Activate UUT\t\d\d:\d\d:\d\d\tFailed"
timeOfDayReg=r".\d:\d\d:\d\d \w\w"
timeOnlyReg=r".\d:\d\d:\d\d"
#----------------------------------------------------------#

def readFile(filename):
    filename = os.path.join(root, filename)
    fp = open(filename, encoding='utf-8',errors='ignore')
    data = fp.readlines()
    fp.close()
    return data

def getTime(data,regexp):
    count=-1
    for i in data:
        count=count+1
        timeLine=re.match(regexp,i)
        if timeLine:
            Time=re.findall(timeOfDayReg,data[count])
            Time=str.strip(Time[0])
            Time=str.strip(Time,' PM')
            Time=str.strip(Time,' AM')
            datetime_object=datetime.strptime(Time,"%H:%M:%S")
            return datetime_object

def amountTimeout(data,regexp):
    totalTimeout=0
    for i in data:
        timeLine=re.match(regexp,i)
        if timeLine:
            totalTimeout=totalTimeout+1
    return totalTimeout

def main():
    allList=[]
    failList=[]
    numberTimeout=0
    percentTimeout=0
    totalFiles=0

    for i in os.listdir(root):
        totalFiles=totalFiles+1
        allList.append(i)
        if i.endswith('.FAIL'):
            failList.append(i)
    count=0
    for filename in failList:
        startTime=getTime(readFile(filename),startTimereg)
        endTime=getTime(readFile(filename),endFailReg)
        if ((startTime==None) or (endTime==None)):
            continue   
        else:
            TestElapsedTime=endTime-startTime
            elapsedTime.append(TestElapsedTime)
            count=count+1
 
    total=datetime.strptime("0:00:00","%H:%M:%S")

    for i in elapsedTime:
        total=i+total

    numberTimeout=count
    percentTimeout=numberTimeout/len(failList)
    print("Percent of fails that timed out:", percentTimeout*100,"%")

    totalSeconds=total.hour*60*60+(total.minute*60)+total.second
    avg=(totalSeconds/count)
    m, s = divmod(avg, 60)
    round(s,0)
    print(m, "minutes")
    print(s, "seconds")

if __name__ == "__main__":
    main()
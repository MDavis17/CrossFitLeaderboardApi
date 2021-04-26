import requests
import json
import sys, getopt

def getUrl(competition,year,eventNum,pageNum):
    return "https://games.crossfit.com/competitions/api/v1/competitions/" + competition + "/" + str(year) + "/leaderboards?&sort=" + str(eventNum) + "&page=" + str(pageNum)

def getData(competition,year,eventNum):
    data = json.loads(requests.get(getUrl(competition,year,eventNum,1)).text)
    pageTotal = data["pagination"]["totalPages"]
    for i in range(1,3): # for now, just pages 1 and 2. fix with int(pageTotal+1)
        page = json.loads(requests.get(getUrl(competition,year,eventNum,i)).text)
        data.update(page)
    return data

def getTotalPageCount(competition,year,eventNum,pageNum):
    data = json.loads(requests.get(getUrl(competition,year,eventNum,pageNum)).text)
    return data["pagination"]["totalPages"]

def main(argv):
    comp = ''
    year = ''
    eventnum = 0
    try:
        opts, args = getopt.getopt(argv,"hc:y:e",["comp=","year=","eventnum="])
    except getopt.GetoptError:
        print 'getData.py -c <competition> -y <year> -e <eventnum>'
        sys.exit(2)
    optList = []
    for opt, arg in opts:
        optList.append(opt)
        if opt == '-h':
            print 'getData.py -c <competition> -y <year> -e <eventnum>'
            sys.exit()
        elif opt in ("-c", "--comp"):
            comp = arg
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-e", "--eventnum"):
            eventnum = arg
    if '-c' not in optList:
        print '-c <competition> is a required option'
        sys.exit(2)
    if '-y' not in optList:
        print '-y <year> is a required option'
        sys.exit(2)
    dataFile = open(str(comp)+"_"+str(year)+".txt","w")
    dataFile.write(str(getData(str(comp),year,int(eventnum))))
    dataFile.close()

if __name__ == "__main__":
   main(sys.argv[1:])
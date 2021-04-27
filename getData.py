import requests
import json
import sys, getopt

def getUrl(competition,year,eventNum,pageNum):
    return "https://games.crossfit.com/competitions/api/v1/competitions/" + competition + "/" + str(year) + "/leaderboards?&sort=" + str(eventNum) + "&page=" + str(pageNum)

def getData(competition,year,eventNum):
    allData = []
    data = json.loads(requests.get(getUrl(competition,year,eventNum,1)).text)
    pageTotal = data["pagination"]["totalPages"]
    for i in range(1,3): # for now, just pages 1 and 2. fix with int(pageTotal+1)
        page = json.loads(requests.get(getUrl(competition,year,eventNum,i)).text)
        leaderboardRows = page["leaderboardRows"]
        for row in leaderboardRows:
            rowData = {}
            rowData["entrant"] = row["entrant"]
            rowData["overallRank"] = row["overallRank"]
            rowData["overallScore"] = row["overallScore"]
            allData.append(rowData)
    return allData

def main(argv):
    comp = ''
    year = ''
    eventnum = 0
    try:
        opts, args = getopt.getopt(argv,"hc:y:e:",["comp=","year=","eventnum="])
    except getopt.GetoptError:
        print 'getData.py -c <competition> -y <year> optional: -e <event num>'
        sys.exit(2)
    optList = []
    for opt, arg in opts:
        optList.append(opt)
        if opt == '-h':
            print 'getData.py -c <competition> -y <year> optional: -e <event num>'
            sys.exit()
        elif opt in ("-c", "--comp"):
            if arg not in ["open","regionals","games"]:
                print 'invalid competition argument (open, regionals, games)'
                sys.exit(2)
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
    if comp == "open" and int(year) < 2017 or int(year) > 2020:
        print 'invalid year for the open (valid for 2017-2020)'
        sys.exit(2)
    if comp == "regionals" and int(year) != 2017:
        print 'invalid year for regionals (2017 only)'
        sys.exit(2)
    if comp == "games" and int(year) < 2007 or int(year) > 2020:
        print 'invalid year for the open (valid for 2007-2020)'
        sys.exit(2)

    dataFile = open(str(comp)+"_"+str(year)+".json","w")
    data = getData(str(comp),year,int(eventnum))
    dataFile.write(str(data))
    dataFile.close()

if __name__ == "__main__":
   main(sys.argv[1:])
import requests
import json
import sys, getopt
import unicodedata

def getUrl(competition,year,division,eventNum,pageNum):
    return "https://games.crossfit.com/competitions/api/v1/competitions/" + competition + "/" + str(year) + "/leaderboards" \
           + "?&sort=" + str(eventNum) + "&page=" + str(pageNum) + "&division=" + str(division)

def getData(competition,year,division,eventNum,pages):
    allData = []
    for i in range(1,pages+1):
        if i % 10 == 0:
            print 'page ',i
        page = json.loads(requests.get(getUrl(competition,year,division,eventNum,i)).text)
        leaderboardRows = page["leaderboardRows"]
        for row in leaderboardRows:
            rowData = {}
            entrantData = {}
            for key in row["entrant"]:
                entrantData[str(key)] = str(unicodedata.normalize('NFKD', row["entrant"][key]).encode('ascii', 'ignore'))
            rowData["entrant"] = entrantData
            rowData["overallRank"] = str(row["overallRank"])
            rowData["overallScore"] = str(row["overallScore"])
            allData.append(rowData)
    return allData

def main(argv):
    comp = ''
    year = ''
    eventnum = 0
    pages = 1
    division = 1
    divisions = ["men","women"]
    try:
        opts, args = getopt.getopt(argv,"hp:c:y:e:d:",["pages=","comp=","year=","eventnum=","division="])
    except getopt.GetoptError:
        print 'getData.py -c <competition> -y <year> -d <division> optional: -e <event num> -p <pages>'
        sys.exit(2)
    optList = []
    for opt, arg in opts:
        optList.append(opt)
        if opt == '-h':
            print 'getData.py -c <competition> -y <year> -d <division> optional: -e <event num> -p <pages>'
            sys.exit()
        elif opt in ("-c", "--comp"):
            if arg not in ["open","regionals","games"]:
                print 'invalid competition argument (open, regionals, games)'
                sys.exit(2)
            comp = arg
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-e", "--eventnum"):
            eventnum = int(arg)
        elif opt in ("-p", "--pages"):
            pages = int(arg)
        elif opt in ("-d", "--division"):
            if int(arg) not in range(1,20):
                print "invalid division (1-19). 1: Men, 2: Women"
                sys.exit(2)
            division = int(arg)
    if '-c' not in optList:
        print '-c <competition> is a required option'
        sys.exit(2)
    if '-y' not in optList:
        print '-y <year> is a required option'
        sys.exit(2)
    if '-d' not in optList:
        print '-d <division> is a required option (1-19) 1: Men, 2: Women'
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


    dataFile = open(str(comp)+"_"+str(year)+"_"+divisions[division-1]+".json","w")
    data = {"data": getData(str(comp),year,division,eventnum,pages)}
    dataFile.write(str(data))
    dataFile.close()

if __name__ == "__main__":
   main(sys.argv[1:])
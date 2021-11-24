import requests # in order to work with apis

startdate = input("enter start date: ") # format YYYY-MM-DD
enddate = input("enter end date: ") # format YYYY-MM-DD
rawstartdate = int(startdate[:4] + startdate[5:7] + startdate[8:])
rawenddate = int(enddate[:4] + enddate[5:7] + enddate[8:])
date = rawstartdate
while date <= rawenddate:
    #print(organizeddate)
    organizeddate = (str(date))[:4]+ "-" + (str(date))[4:6]+ "-" + (str(date))[6:]
    url = "https://api.opencovid.ca/timeseries?date=" + organizeddate
    apirequest = requests.get(url).json()
    avaccine = apirequest["avaccine"]
    avaccine2 = avaccine[3]
    print(str(date))
    print(str(avaccine2) + "\n")
    date += 1







#url = "https://api.opencovid.ca/timeseries?stat=cases&date=" + dateinput

#apirequest = requests.get(url).json()

#print(apirequest)
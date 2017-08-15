#!/home/ubuntu/.env/bin/python
# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import MySQLdb
import MySQLdb.cursors
from bs4 import BeautifulSoup

# Light table
def colorcheck(word):
    if(word == "水情正常"):
        return('藍')
    elif(word == "水情稍緊"):
         return("綠")
    elif(word == "一階限水"):
         return("黃")
    elif(word == "二階限水"):
         return("橘")
    elif(word == "三階限水"):
         return("紅")
    else:
        return("?")

# Download open data   
# 1. get json url
try:
    htm = urllib.request.urlopen("https://data.gov.tw/dataset/36695")
    soup = BeautifulSoup(htm, "html.parser")
    json_link = soup.findAll('a')[19]['href']
    print("Get json link","\n",json_link)
except:
    print(json_link)
    print("Can't Connect to the data server. Maybe the site is under maintain.\n", sys.exc_info()[0],"\nCheck the link below.","\nhttps://data.gov.tw/dataset/36695")
    sys.exit()
# 2. get json data
try:
    data_json = urllib.request.urlopen(json_link)
    data = json.loads(data_json.read().decode())
    print("Get json data successfully!")
except:
    print("Can't Connect to the data server. Maybe the site is under maintain.\n", sys.exc_info()[0],"\nCheck the link below.","\n",json_link)
    sys.exit()

end = len(data['DroughtWarning_OPENDATA'])-1

# Connect to database
try:
    conn = MySQLdb.connect(host='localhost',
                            user='demouser',
                            passwd='demo1234',
                            db='demo',
                            charset='utf8')
    print("Connect to mysql through demouser.")
except:
    print("Can't Connect Database via demouser: ", sys.exc_info()[0])
    sys.exit()
    
cursor = conn.cursor()  

# Insert into Database 
for i in range(0,end,1):
    I = '1' #str(i)
    T = data['DroughtWarning_OPENDATA'][i]['DroughtWarningDate'].replace('/','-')
    R = colorcheck(data['DroughtWarning_OPENDATA'][i]['DroughtWarningStage'])
    sql = "INSERT INTO RegionalWaterRegime (C_ID, TimeStamp, ReservoirLightsNow) VALUES(\""+I+"\",\""+T+"\",\""+R+"\");"
    #print(sql)
    cursor.execute(sql)
    conn.commit()


# Close DB link
cursor.close()
conn.close()

#Everything seems like no problem. Can get the data, however, cannot insert into table.
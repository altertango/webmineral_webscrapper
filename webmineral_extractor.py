import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
from googlesearch import search



#### http://webmineral.com/data/Orthoclase.shtml

#search: search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
# query : query string that we want to search for.
# tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
# lang : lang stands for language.
# num : Number of results we want.
# start : First result to retrieve.
# stop : Last result to retrieve. Use None to keep searching forever.
# pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
# Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.


output=[]
f="minerales.csv"
  




with open(f, "rt", encoding="latin1") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for line in reader:
        b = " ".join(line)
        print("searching for mineral " + str(b) + "...")

        query = "site:http://webmineral.com/ "+b

        url=""
        for j in search(query, tld="com", num=5, stop=5, pause=2): 
            if j[-5:] == "shtml" and "webmineral" in j: 
                url=j.replace("www.","")
                break
        aux=[b]
        if url == "":
            aux.append("mineral not found")
        else:
            print(url)
            aux.append(url[-(len(url)-27):-6])
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'dnt': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }
            )

            f = urllib.request.urlopen(req)
            soup = BeautifulSoup(f.read(), 'html.parser')
            
            rows = soup.find_all('tr')
            table=[row.find_all('td') for row in rows]
            
            cf=""
            mw=""
            ef=""
            ro_min=""
            ro_max=""
            ro=""
            cf_bool=False
            ef_bool=False
            ro_bool=False
            for r in table:
                for c in r:
                    ct=c.get_text()
                    
                    #Chemical formula
                    if cf_bool:
                        print(ct)
                        cf_bool=False
                        cf=ct.replace(' ','').replace(',',';')
                    if "Chemical  Formula" in ct:
                        cf_bool=True
                        
                    #Empirical Formula
                    if ef_bool:
                        print(ct)
                        ef_bool=False
                        ef=ct.replace(' ','').replace(',',';')
                    if "Empirical Formula" in ct:
                        ef_bool=True
                        
                    #Molecular weight
                    if "Molecular Weight = " in ct:
                        print(ct)
                        mw=ct[19:-3].replace(' gm','').replace(' ','')
                        
                    #Density
                    if ro_bool:
                        print(ct)
                        ro_bool=False
                        if "-" in ct:
                            ro_min , ro_max=[t.replace(' ','') for t in ct.split(',')[0].split('-')]
                            ro=ct.split(',')[1][13:].replace(' ','')
                        else: ro=ct
                    if ("Density:" in ct) and ("Electron" not in ct):
                        ro_bool=True
                        

            aux=aux+[cf,ef,mw,ro_min,ro_max,ro] 
            print(aux)
                    
            output.append(aux)
        sleep(1)
with open('output.csv', 'wt', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Mineral_search","Mineral_result","Chemical  Formula","Empirical Formula","MW (g/mol)","ro_min (g/cm3)","ro_max (g/cm3)","ro (g/cm3)"])
    for o in output:
        spamwriter.writerow(o)
input("Press Enter to continue...")

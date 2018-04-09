from django.conf import settings

from bs4 import BeautifulSoup as b
import requests
import random


USER_AGENT_CHOICES = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]


def grabProxies():
    site = 'https://free-proxy-list.net/'
    hdr = {'User-Agent': random.choice(USER_AGENT_CHOICES)}
    req = requests.get(site, headers=hdr) # sending requests with headers
    response = req.text                   # opening and reading the source code
    html = b(response, "lxml")                #structuring the source code in proper format
    rows = html.findAll("tr")       #finding all rows in the table if any.
    ips = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text for ele in cols]
        try:
            ipaddr = cols[0]        #ipAddress which presents in the first element of cols list
            portNum = cols[1]       #portNum which presents in the second element of cols list
            proxy = ipaddr+":"+portNum  #concatinating both ip and port
            portName = cols[6]          #portName variable result will be yes / No
            if portName == "no":
                ips.append("http://" + str(proxy)) #if yes then it appends the proxy with https
            else:
                ips.append("https://" + str(proxy)) #if no then it appends the proxy with http
        except:
            pass
    if ips:
        ips = random.sample(ips, k=len(ips))
        with open(settings.PATH_PROXIES, 'w') as f:
            for ip in ips:
                f.write(ip + '\n')
        f.close()
        return True
    else:
        return False

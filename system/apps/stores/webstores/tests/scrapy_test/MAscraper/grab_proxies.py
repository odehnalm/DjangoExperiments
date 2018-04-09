from fake_useragent import UserAgent
from bs4 import BeautifulSoup as b
import requests


def grabProxies():
    site = 'https://free-proxy-list.net/'
    ua = UserAgent(path="fake_useragent.json")
    hdr = {'User-Agent': ua.random}

    # sending requests with headers
    req = requests.get(site, headers=hdr)

    # opening and reading the source code
    response = req.text

    # structuring the source code in proper format
    html = b(response, "lxml")

    # finding all rows in the table if any.
    rows = html.findAll("tr")

    ips = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text for ele in cols]
        try:
            # ipAddress which presents in the first element of cols list
            ipaddr = cols[0]

            # portNum which presents in the second element of cols list
            portNum = cols[1]

            # concatinating both ip and port
            proxy = ipaddr + ":" + portNum

            # portName variable result will be yes / No
            portName = cols[6]

            if portName == "no":
                # if yes then it appends the proxy with https
                ips.append("http://" + str(proxy))
            else:
                # if no then it appends the proxy with http
                ips.append("https://" + str(proxy))
        except:
            pass
    if ips:
        with open('proxies.txt', 'w') as fp:
            for ip in ips:
                fp.write(ip+'\n')

        return True
        print("HECHO")
    else:
        print("NO SE ENCONTRARON IPS")
        return False

grabProxies()

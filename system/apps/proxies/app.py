from django.apps import apps
from django.conf import settings

from fake_useragent import UserAgent
from bs4 import BeautifulSoup as b
import requests

from .models import Proxy


def grabProxies():

    print("Almacenando en DB IPs de proxies"
          " habilitadas para todas las tiendas...")

    try:
        model = apps.get_model(
            app_label=settings.WEBSITES_APP,
            model_name=settings.WEBSITES_MODEL)
    except LookupError:
        raise LookupError("Defina correctamente "
                          "el valor de 'WEBSITES_APP' o "
                          "de 'WEBSITES_MODEL'")

    site = 'https://free-proxy-list.net/'
    ua = UserAgent(path=settings.PATH_FAKE_USER_AGENT)
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

        for ip in ips:

            p, created = Proxy.objects.get_or_create(
                ip_proxy=ip
            )
            if created:
                instances = model.objects.all()
                for instance in instances:
                    p.websites.add(instance)
        return True
        print("HECHO")
    else:
        print("NO SE ENCONTRARON IPS")
        return False

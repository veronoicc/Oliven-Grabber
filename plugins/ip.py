import requests


def getipv4():
    reqv4 = requests.get('https://api.ipify.org/')
    publicipv4 = reqv4.text
    return publicipv4


def getipv6():
    reqv6 = requests.get('https://api64.ipify.org/')
    publicipv6 = reqv6.text
    return publicipv6


def getipinfo():
    ipdetai = requests.get('https://ipinfo.io/' + publicipv4 + '')
    ipdetail = ipdetai.json()
    return ipdetail


def ips():
    ipdetail = getipinfo()
    ipv6 = getipv6()
    ipv4 = getipv4()
    return ipdetail, ipv6, ipv4


publicipv4 = getipv4()

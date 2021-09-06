import os


def findminecraft():
    appdatapath = os.getenv('APPDATA')
    minecraftpath = os.path.join(appdatapath, '.minecraft')
    return minecraftpath

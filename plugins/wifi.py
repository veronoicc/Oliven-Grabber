import subprocess


def grabpassword(command):
    output = subprocess.Popen(command)


def getpassword(name):
    command = "sudo security find-generic-password -l" + \
              name + " -D 'AirPort network password' -w"
    output = grabpassword(command)


def wifiloop():
    try:
        wifis = subprocess.check_output(["netsh", "wlan", "show", "network"])
        wifis = wifis.decode("ascii")  # needed in python 3
        wifis = wifis.replace("\r", "")
        ls = wifis.split("\n")
        ls = ls[4:]
        ssids = []
        x = 0
        while x < len(ls):
            if x % 5 == 0:
                ssids.append(ls[x])
            x += 1
        if not ssids:
            return 'No Wifis Found'
        else:
            return ssids
    except Exception as e:
        return 'Error: ' + str(e)


result = wifiloop()
print(result)

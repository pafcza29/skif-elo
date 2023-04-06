import nextcord
from nextcord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if ("waltuh") in message.content:
            await message.channel.send("Did someone say my name?")
            embed = nextcord.Embed(title="Waltuh")
            embed.set_image(url="https://compote.slate.com/images/fb69a16d-7f35-4103-98c1-62d466196b9a.jpg?crop=590%2C375%2Cx0%2Cy0&width=1280")
            await message.channel.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))

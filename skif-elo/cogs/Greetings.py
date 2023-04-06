import nextcord
from nextcord.ext import commands

class Greetings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

    @commands.command()
    async def bye(self, ctx):
        await ctx.send("Goodbye!")

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.User):
        guild = member.guild
        if guild.system_channel is not None:
            msg = f"Welcome {member.mention} to {guild.name}"
            await guild.system_channel.send(msg)

def setup(client):
    client.add_cog(Greetings(client))

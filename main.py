import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("\n----------------------------")
    print("The bot is now ready for use")
    print("----------------------------")

initial_extentions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extentions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extentions:
        client.load_extension(extension)

client.run(DISCORD_TOKEN)
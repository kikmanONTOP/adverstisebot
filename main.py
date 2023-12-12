import discord
from discord.ext import commands
import json
import random
from colorama import Fore

ascii = '''                                                   
 ***** ***** ***** ***** ***** ***** ***** ***** *****
///// ///// ///// ///// ///// ///// ///// ///// /////                                                       
'''

#settings
prefix = "!"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
bot_token = 'bot token'
target_channel_id = #
allowed_user_id = #
json_file = 'servers.json'
promo_channel_id = #
@client.event
async def on_ready():
    print(Fore.GREEN + ascii)
    print(Fore.RED + f"bot is ready as {client.user}")
    print(Fore.GREEN + ascii)
@client.command()
async def promo(ctx, *, message=None):
    if ctx.channel.id == promo_channel_id:
        if message:
            sent_message = await client.get_channel(target_channel_id).send(message)
            
            add_to_json(sent_message.id, message)
            await ctx.send("Done. now wait.")
        else:
            await ctx.send("You must provide the text of the message for advertising.")
    else:
        await ctx.send("This command can only be used in the specified channel.")

@client.command()
async def accept(ctx, message_id: int):
    if ctx.author.id == allowed_user_id:
        try:
            message = await client.get_channel(target_channel_id).fetch_message(message_id)
            
            add_to_json(message.id, message.content)
            await ctx.send("Promo added to the databse!")
        except discord.NotFound:
            await ctx.send("A message with this ID was not found.")
    else:
        await ctx.send("You do not have permission to use this command.")

@client.command()
async def servers(ctx):
    messages = load_from_json()
    
    if messages:
        random_message = random.choice(messages)
        embed = discord.Embed(title="Server:", description=random_message, color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No messages available.")

def add_to_json(message_id, content):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    data.append({"id": message_id, "content": content})

    with open(json_file, 'w') as file:
        json.dump(data, file)


def load_from_json():
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        return [message["content"] for message in data]
    except FileNotFoundError:
        return []


client.run(bot_token)
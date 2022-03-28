import math

import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import Bot
import string
import datetime
# import psycopg2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import asyncio
import itertools
import ChessEngine2

matrix = np.array([[], []])
intents = discord.Intents.default()
intents.members = True
intents.messages = True
Bot = commands.Bot(command_prefix = "$:", intents=intents, guild_subscriptions=True, help_command=None)
# conn = psycopg2.connect(
#     host="localhost",
#     database="test",
#     user="postgres",
#     password="ktfm48tm956mif_2005",
#     port='5432',
# )
token = 'NzY3NzE0NjE5NTc3NDY2ODkx.X4179A.DCxho027iK6rwWq2WP93weyOnmo'
client = discord.Client()

chessboard = ChessEngine2.ChessBoard
chessboard.fill_board(chessboard)
chessboard.import_game(chessboard, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")


def odd_numders(to_num):
    array = []
    for i in range(1, to_num):
        if i % 2:
            array.append(i)
    return array
def start(arg1):
    matrix.resize((arg1, arg1), refcheck=False)
    for i in range(arg1):
        for j in range(arg1):
            matrix[i, j] = 0
    for i in range(arg1):
        for j in range(arg1):
            if random.randint(1, 12) == 1:
                matrix[i, j] = 1
def delmo(arg1):
    tmp = ''
    for a in str(arg1):
        if a != "@" and a != '&' and a != '<' and a != '>' and a != '!' and a !='#':
            tmp += a
    return tmp
def to_upper(argument):
    return string.ascii_uppercase(argument)

@Bot.event
async def on_ready():
    print(f'Bot is now working, {Bot.user}. {len(Bot.guilds)} And right now i see {len(Bot.users)} humans and girls')
    for server in Bot.guilds:
        print(server.name)
        server_channels = server.channels
        is_chanel = True
        for channel in server_channels:
            if 'admin' == channel.name:
                is_chanel = False
        if is_chanel == True:
            try:
                await server.create_text_channel('admin', position=0)
            except:
                print(f'Permission denied for server: {server.name}')

    await Bot.change_presence(activity=discord.Game(name=f'$:help | {len(Bot.users)} members'))
@Bot.event
async def on_voice_state_update(member, before, after):
    if member.guild.id != 336642139381301249:
        server_channels = member.guild.channels

        for channel in server_channels:
            if 'admin' == channel.name:
                admin_channel = member.guild.get_channel(int(delmo(channel.id)))
                break

        if after.channel != before.channel:
            embed = discord.Embed(title='Server Log', description='Voice chat join log.',
                                  color=discord.Color.dark_green())
            if str(after.channel) != 'None':
                embed.add_field(name=f'Member {member} joined channel:', value=f'*{after.channel.name}*')
            else:
                embed.add_field(name=f'Member {member} leave voice chat.', value=f'Channel: {before.channel.name}')
                embed.color = discord.Color.dark_red()
            await admin_channel.send(embed=embed)
@Bot.event
async def on_message(message):
    await Bot.process_commands(message)
    if message.guild.id != 336642139381301249:
        if message.author != Bot.user:
            if "siea" in message.content:
                await message.channel.send('Hi')
            if message.content.startswith('2137'):
                print(message.guild.id)
                await message.channel.send('Papież polak pog 👍')
                await message.channel.send(f'===> {message.channel}')
@Bot.event
async def on_member_remove(member):
    if member.guild.id != 336642139381301249:
        embed = discord.Embed(title='Member leave the server', description='', color=discord.Color.red())
        embed.add_field(name='', value='')
        embed.add_field(name='', value='')
        embed.add_field(name='', value='')
        embed.add_field(name='', value='')
@Bot.event
async def on_message_edit(before, after):
    if after.guild.id != 336642139381301249:
        server_channels = after.guild.channels
        for channel in server_channels:
            if 'admin' == channel.name:
                admin_channel = after.guild.get_channel(int(delmo(channel.id)))
                break
        if before.author != Bot.user:
            embed = discord.Embed(title='Message edited', description='', color=discord.Color.orange())
            embed.add_field(name='Message before:', value=f'|{before.content}')
            embed.add_field(name='Message after:', value=f'|{after.content}')
            embed.add_field(name='Sender:', value=f'|@{after.author}')
            embed.add_field(name='Channel:', value=f'|{after.channel}, *{after.channel.id}*')
            embed.add_field(name='Changed at:',
                            value=f"|{datetime.datetime.strftime(after.created_at, '%Y-%m-%d %H:%M:%S')}")
            if before.content != after.content:
                await admin_channel.send(embed=embed)
@Bot.event
async def on_message_delete(message):
    if message.guild.id != 336642139381301249:
        server_channels = message.guild.channels
        for channel in server_channels:
            if 'admin' == channel.name:
                admin_channel = message.guild.get_channel(int(delmo(channel.id)))
                break
        strs = ''
        embed = discord.Embed(title='Message deleted', description='', color=discord.Color.red())
        embed.add_field(name='Message:', value=f'[{message.content}]')
        embed.add_field(name='Sender:', value=f'|{message.author}')
        embed.add_field(name='Channel:', value=f'|{message.channel}, {message.channel.id}')
        embed.add_field(name='Created at:',
                        value=f"|{datetime.datetime.strftime(message.created_at, '%Y-%m-%d %H:%M:%S')}")
        for i in message.reactions:
            strs += f'{i} '
        embed.add_field(name='Reactions on this message:', value=f'|{strs}')
        await admin_channel.send(embed=embed)
@Bot.command()
async def serverInfo(ctx, *args):
    guild = ctx.guild
    roles = ctx.guild.roles
    members = guild.members
    id = 0
    if args[0] == 'channels':
        if len(args) == 1:
            embed = discord.Embed(title="Server Channels", description="", color=discord.Color.green())
            if (len(guild.text_channels) + len(guild.voice_channels)) > 20:
                embed.add_field(name=f'There are more than 20 channels on this server', value=f'>>> *return lists*')
                ids = 0
                strs = ''
                for channel in guild.text_channels:
                    if id <= 20:
                        strs += f'{channel.name}, '
                    else:
                        id = 0
                        ids += 1
                        embed.add_field(name=f'{ids}', value=f'|{strs}')
                        strs = ''
                    id += 1
                if strs != 0:
                    id = 0
                    embed.add_field(name=f'{ids + 1}', value=f'|{strs}')
                strs = ''
                for channel in guild.voice_channels:
                    if id <= 20:
                        strs += f'{channel.name}'
                    else:
                        id = 0
                        ids += 1
                        embed.add_field(name=f'{ids}', value=f'[Voice] {strs}')
                        strs = ''
                    id += 1
                if strs != 0:
                    id = 0
                    embed.add_field(name=f'{ids + 1}', value=f'[Voice] {strs}')
            else:
                id = 0
                for channel in guild.text_channels:
                    embed.add_field(name=f'{channel.name}', value=f"ID: [{id}]")
                    id += 1
                for channel in guild.voice_channels:
                    embed.add_field(name=f'[Voice] {channel.name}', value=f"ID: [{id}]")
                    id += 1
        else:
            strs = ''
            channel = guild.get_channel(int(delmo(args[1])))
            embed = discord.Embed(title=f'Information about "{channel}" channel', description='', color=discord.Color.dark_blue())
            embed.add_field(name='Channel category:', value=f'|{channel.category}')
            embed.add_field(name='Created at:', value=f"|{datetime.datetime.strftime(channel.created_at, '%Y-%m-%d %H:%M:%S')}")
            async for message in channel.history(limit=5):
                strs += f'[{message.content}],\n *id: {message.id}* \n'
            embed.add_field(name='Last 5 messages:',
                            value=f'|{strs}')
    elif args[0] == 'members':
        if len(args) == 1:
            embed = discord.Embed(title="Server Members", description="", color=discord.Color.green())
            if len(members) > 20:
                embed.add_field(name=f'There are more than 20 members on this server',value=f'>>> *return lists*')
                strs = ''
                ids = 0
                for member in members:
                    if id <= 20:
                        strs += f'{member}, \n'
                    else:
                        id = 0
                        ids += 1
                        embed.add_field(name=f'{ids}', value=f'{strs}')
                        strs = ''
                    id += 1
                if strs != '':
                    id = 0
                    embed.add_field(name=f'{ids+1}', value=f'{strs}')
            else:
                for member in members:
                    strs = ''
                    for role in member.roles:
                        strs += f'{role}, '
                    embed.add_field(name=f'{member.name}', value=f"ID: [{id}], Roles: {strs}")
                    id += 1
        else:
            member = guild.get_member(int(delmo(args[1])))
            pfp = member.avatar_url
            embed = discord.Embed(title=f"{member.name} Profile", description="", color=discord.Color.blurple())
            embed.add_field(name=f'Server Nickname:', value=f'*{member.nick}*', inline=True)
            embed.add_field(name=f'Real Nickname', value=f'*{member}*', inline=True)
            embed.add_field(name=f'ID', value=f'*{member.id}*', inline=True)
            embed.add_field(name=f'Bot', value=f'*{member.bot}*', inline=True)
            embed.add_field(name=f'Account Created', value=f"*{datetime.datetime.strftime(member.created_at, '%Y-%m-%d %H:%M:%S')}*", inline=True)
            #embed.add_field(name='Member Permissions', value=f'{member.guild_permissions}')
            for permission in member.guild_permissions:
                print(permission)
            strs = ''
            for role in member.roles:
                strs += f'{role}, '
            embed.add_field(name=f'{member}', value=f"Roles: {strs}")
            embed.set_image(url=pfp)
    elif args[0] == 'roles':
        if len(args) == 1:
            embed = discord.Embed(title="Server Roles", description="", color=discord.Color.green())
            for role in roles:
                strs = ''
                for permission in role.permissions:
                    if permission[1] == True:
                        strs += f'{permission[0]}, '
                embed.add_field(name=f'{role}', value=f"ID: [{id}]")
                id += 1
        else:
            strs = ''
            strs2 = ''
            role = guild.get_role(int(delmo(args[1])))
            embed = discord.Embed(title=f"Role: '{role}' Info", description="", color=role.color)
            for permission in role.permissions:
                if permission[1] == True:
                    strs += f'{permission[0]}, '

            for member in role.members:
                    strs2 += f'|**{member}** '
            embed.add_field(name=f'Role permissions: ', value=f"[{strs}]")
            embed.add_field(name=f'Members with "{role}" role:', value=f'[{strs2}]')
            embed.add_field(name=f'Created: "{role}" role:', value=f"{datetime.datetime.strftime(role.created_at, '%Y-%m-%d %H:%M:%S')}")
    else:
        embed = discord.Embed(title='Error', description='{arg1} is null or does not exist.', color=discord.Color.red())
        embed.add_field(name=f'Use $:help', value='to get help XD')
    await ctx.send(embed=embed)
@Bot.command()
async def draw(ctx, *args):
    if len(args) == 1:
        if int(args[0]) <= 500:
            start(int(args[0]))
        else:
            await ctx.send('Size must be smaller than 500')
    else:
        start(250)
    if len(matrix) != 2:
        if len(matrix) != 555:
            image = Image.fromarray((matrix * 255).astype(np.uint8))
            image.save('image.png')
            embed = discord.Embed(title='Just image from random numpy array.',
                                  description=f'Size of picture: {len(matrix)}', color=discord.Color.dark_magenta())
            await ctx.send(embed=embed)
            await ctx.send(file=File('image.png'))
@Bot.command() #clear command
async def clear(ctx, *args): # arg = amount msg to clear
    if len(args) == 1:
        await ctx.channel.purge(limit=int(args[0]) + 1)  # limit is amount o msg to clear
        embed = discord.Embed(title=str(args[0]) + " 🗑",
                              description="Massages were deleted.")  # embed, style to make msg look more attractive
        await ctx.send(embed=embed)
        await asyncio.sleep(2)
        def is_me(m):
            return m.author == Bot.user
        await ctx.channel.purge(limit=1, check=is_me)
@Bot.command()
async def help(ctx):
    embed = discord.Embed(title='Hi, Plane bot is now in developing :))', description='Bot creator: TUHNN#9437/alermgm@gmail.com', color=discord.Color.green())
    embed.add_field(name='Command list', value='*More commands going to be added*')
    embed.add_field(name=f'$:serverInfo members', value='Returns list of all server members')
    embed.add_field(name=f'$:serverInfo members @member/member ID', value='Returns member profile information')
    embed.add_field(name=f'$:serverInfo channels', value='Returns list of all server channels')
    embed.add_field(name=f'$:serverInfo channels #channel/channel ID', value='Returns channel information')
    embed.add_field(name=f'$:serverInfo roles', value='Returns list of all server roles')
    embed.add_field(name=f'$:serverInfo roles @role/role ID',
                    value='Returns role information and list of members with this role')
    embed.add_field(name=f'$:member_move #channel/channel ID', value='Moves member to voice channel.')
    embed.add_field(name=f'$:send_message', value='Sends the same message')
    embed.add_field(name=f'$:draw 1-500', value='Just test image')
    embed.add_field(name=f'$:clear [int]', value='Delete messages in the channel')
    await ctx.send(embed=embed)
@Bot.command()
async def member_move(ctx, *args):
    sender = ctx.author
    channel = ctx.guild.get_channel(int(args[0]))

    await sender.move_to(channel=channel)
@Bot.command()
async def send_message(ctx, *args):
    if len(args) == 2:
        server_channels = ctx.guild.channels
        for channel in server_channels:
            if delmo(args[0]) == channel.name or int(delmo(args[0])) == channel.id:
                need_channel = ctx.guild.get_channel(int(delmo(channel.id)))
                break
        await need_channel.send(args[1])
    else:
        print(args[0])
        await ctx.send(args[0])
@Bot.command()
async def grole(ctx, role1, member: discord.Member=None):
    role = discord.utils.get(ctx.guild.roles, name = role1)
    await member.add_roles(role, member)

@Bot.command()
async def chess(ctx, *args):

    if len(args[0]) == 4:
        try:
            response = chessboard.make_move(chessboard, str(args[0]))
            await ctx.send(response)

        except:
            await ctx.send("Invalid move format, use UCI: `d5f3`")





    background = Image.open("chessboard1.png").resize((1050,1050), Image.ANTIALIAS) #1050x1050

    drw = ImageDraw.Draw(background, 'RGBA')

    black_pawn = Image.open("Chess_pdt60.png").resize((100, 100), Image.ANTIALIAS)
    white_pawn = Image.open("Chess_plt60.png").resize((100, 100), Image.ANTIALIAS)
    black_rook = Image.open("Chess_rdt60.png").resize((100, 100), Image.ANTIALIAS)
    white_rook = Image.open("Chess_rlt60.png").resize((100, 100), Image.ANTIALIAS)
    black_bishop = Image.open("Chess_bdt60.png").resize((100, 100), Image.ANTIALIAS)
    white_bishop = Image.open("Chess_blt60.png").resize((100, 100), Image.ANTIALIAS)
    black_knight = Image.open("Chess_ndt60.png").resize((100, 100), Image.ANTIALIAS)
    white_knight = Image.open("Chess_nlt60.png").resize((100, 100), Image.ANTIALIAS)
    black_quine = Image.open("Chess_qdt60.png").resize((100, 100), Image.ANTIALIAS)
    white_quine = Image.open("Chess_qlt60.png").resize((100, 100), Image.ANTIALIAS)
    black_king = Image.open("Chess_kdt60.png").resize((100, 100), Image.ANTIALIAS)
    white_king = Image.open("Chess_klt60.png").resize((100, 100), Image.ANTIALIAS)

    id = 0
    for x in range(1, 9):
        for y in range(1, 9):
            y_cord = math.floor((1000*(x/8))-87)
            x_cord = math.floor((1000*(y/8))-90)

            if chessboard.squares[id][2] == "p":
                background.paste(black_pawn, (x_cord, y_cord), black_pawn)
            if chessboard.squares[id][2] == "b":
                background.paste(black_bishop, (x_cord, y_cord), black_bishop)
            if chessboard.squares[id][2] == "n":
                background.paste(black_knight, (x_cord, y_cord), black_knight)
            if chessboard.squares[id][2] == "r":
                background.paste(black_rook, (x_cord, y_cord), black_rook)
            if chessboard.squares[id][2] == "q":
                background.paste(black_quine, (x_cord, y_cord), black_quine)
            if chessboard.squares[id][2] == "k":
                background.paste(black_king, (x_cord, y_cord), black_king)
            if chessboard.squares[id][2] == "P":
                background.paste(white_pawn, (x_cord, y_cord), white_pawn)
            if chessboard.squares[id][2] == "B":
                background.paste(white_bishop, (x_cord, y_cord), white_bishop)
            if chessboard.squares[id][2] == "N":
                background.paste(white_knight, (x_cord, y_cord), white_knight)
            if chessboard.squares[id][2] == "R":
                background.paste(white_rook, (x_cord, y_cord), white_rook)
            if chessboard.squares[id][2] == "Q":
                background.paste(white_quine, (x_cord, y_cord), white_quine)
            if chessboard.squares[id][2] == "K":
                background.paste(white_king, (x_cord, y_cord), white_king)


            id += 1
    # drw.polygon(xy=[(50, 0)], fill=(255, 0, 0, 125))

    background.save("temp.png")

    file = discord.File('temp.png')





    await ctx.send(file=file)


Bot.run(str(token))


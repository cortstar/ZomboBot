import discord
import ZomboCommand
import zomboData
import asyncio
import random
import os

client = discord.Client()
command_prefix = '~'



inspirational_quotes_directory = "resources/inspire"
welcome_quotes_directory = "resources/welcome"
full_Zombo_directory = "resources/full"

zomboQuotes = []

with open("resources/zombo_quotes.txt") as file:
    # noinspection PyRedeclaration
    zomboQuotes = file.readlines()
    file.close()

zomboEmojiUnicode = ['\U0001F1FF', '\U0001F1F4', '\U0001F1F2', '\U0001F1E7', '\U0001F17E']


async def Info(command):
    command = command #type: ZomboCommand.ZomboCommand
    await client.send_message(
        command.channel,
        "Your username is {} and you joined the server at {}.".format(command.sender, command.sender.joined_at))
    await client.send_message(
        command.channel,
        "My username is ZomboBot. I make anything possible. Type ~help to find out what."
    )


async def Inspire(command):
    command = command #type: ZomboCommand.ZomboCommand
    if (len(command.mentions) > 0):
        vc = await get_voice_channel_from_user(command.mentions[0])
        if vc is not None:
            await play_clips_to_voice_channel(vc, get_filepath_of_random_file(inspirational_quotes_directory))
        else:
            await client.send_message(command.channel, "{} isn't in a voice channel, mon.".format(command.mentions[0]))


async def Welcome(command):
    command = command #type: ZomboCommand.ZomboCommand
    if len(command.mentions) > 0:
        vc = await get_voice_channel_from_user(command.mentions[0])
        if vc is not None:
            await play_clips_to_voice_channel(vc, get_filepath_of_random_file(welcome_quotes_directory))
        else:
            await client.send_message(command.channel, "{} isn't in a voice channel, mon.".format(command.mentions[0]))


async def ZomboBomb(command):
    command = command #type: ZomboCommand.ZomboCommand
    if len(command.mentions) > 0:
        vc = await get_voice_channel_from_user(command.mentions[0])
        if vc is not None:
            await play_clips_to_voice_channel(vc, get_filepath_of_random_file(full_Zombo_directory))
        else:
            await client.send_message(command.channel, "{} isn't in a voice channel, mon.".format(command.mentions[0]))

async def ZomboTTS(command):
    command = command #type: ZomboCommand.ZomboCommand
    lines = 1
    if len(command.kwargs) > 0:
        try:
            lines = int(command.kwargs[0])
        except ValueError:
            lines = 1

    if lines < 1:
        lines = 1
    elif lines > 10:
        await client.send_message(command.channel, "Maximum number of lines is 10, mon.")
        lines = 10

    messages = []
    for i in range(0, lines):
        messages.append(random.choice(zomboQuotes))

    await client.send_message(command.channel, " ".join(messages), tts=True)

async def ZomboReact(command):
    command = command #type: ZomboCommand.ZomboCommand
    try:
        messages = []
        async for m in client.logs_from(command.channel, limit=2):
            messages.append(m)

        for reaction in zomboEmojiUnicode:
            await client.add_reaction(messages[1], reaction)
    except discord.Forbidden as e:
        print("{}: ZomboCom needs permission to do that.".format(str(e)))



async def help(command):
    command = command #type: ZomboCommand

    description = ''
    if len(command.kwargs) > 0:
        description = zomboData.get_command_description(command.kwargs[0])
        await client.send_message(command.channel, description)
    else:
        await client.send_message(command.channel, ",".join(commandMap.keys()))

commandMap = {
    'info': Info,
    'inspire': Inspire,
    'welcome': Welcome,
    'zombobomb': ZomboBomb,
    'zombotts': ZomboTTS,
    'zomboreact':ZomboReact,
    'help': help}


@client.event
async def on_ready():
    print("Welcome to ZomboBot.")
    print("You can do anything, with ZomboBot.")
    print("ZomboBot runs with discord.py version {} made by Rapptz.".format(discord.__version__))


@client.event
async def on_message(message):
    if message.content.startswith('{}'.format(command_prefix)):
        command = ZomboCommand.ZomboCommand(message.content[1:], message.channel, message.author, message.mentions) #type: ZomboCommand
        TryRunCommand(command)


def TryRunCommand(command):
    print("Try run command")
    command = command #type: ZomboCommand.ZomboCommand
    client.loop.create_task(commandMap[command.command](command))


async def play_clips_to_voice_channel(channel, path):
    voice_client = channel.server.voice_client  # type: discord.VoiceClient
    player = voice_client.create_ffmpeg_player(path)
    player.start()
    while (player.is_playing()):
        await asyncio.sleep(.2)
    await voice_client.disconnect()


async def get_voice_channel_from_user(user):
    voice_channel = None
    try:
        voice_channel = user.voice.voice_channel
        await client.join_voice_channel(voice_channel)
    except discord.InvalidArgument as e:
        print("{} isn't in a voice channel!".format(str(user)))
        return
    except asyncio.TimeoutError:
        print("Timed out connecting to {}".format(voice_channel))
        return
    except discord.ClientException:
        return
    except discord.OpusNotLoaded as e:
        print(str(e))
        return
    return voice_channel


def get_filepath_of_random_file(directory):
    directory = directory #type: str
    return "{}/{}".format(directory, random.choice(os.listdir(directory)))

client.run('MzczMTkxNDYzNzgzMjM1NTg2.DTbQzQ.xKJ9KXZ64SIIvEnxJVMWWLQnce0')




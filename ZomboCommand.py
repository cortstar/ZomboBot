import discord

class ZomboCommand:

    command = ''
    kwargs = []
    mentions = []

    channel = None
    sender = None

    def __init__(self, commandString, channel, sender, mentions):
        parsed = commandString.lower().split() #type: List[str]

        self.command = parsed[0]
        self.kwargs = parsed[1:]
        self.channel = channel
        self.sender = sender
        self.mentions = mentions
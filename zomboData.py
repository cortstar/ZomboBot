version = 1.1

# todo: move to config files.

command_descriptions = {
    'info': 'Syntax: ~info. Provides information about ZomboBot.',
    'inspire': 'Syntax: ~inspire @[username]. Joins the user\'s channel and inspires them.',
    'zombobomb': 'Syntax: ~zombobomb @[username]. Joins the user\'s '
                 'channel and gives them the FULL ZOMBO TREATMENT.',
    'welcome': 'Syntax: ~welcome @[username]. Joins the user\'s channel and welcomes them.',
    'zombotts': 'Syntax: ~zomboTTS [optional: number] sends 1 or number if specified lines of Zombo Text-To-Speech.',
    'zomboreact': 'Syntax: ~zomboReact. Zombobot will react to the previous message.',
    'help': 'Syntax: ~help [command]. Reveals hidden ZomboInformation about a command.'
}


def get_startup_text():
    return "ZomboBot version {} loaded.".format(version)


def get_joined_text():
    return "I'm here, mon. You can do anything... with ZomboBot."


def get_command_description(command_name):
    return command_descriptions.get(command_name, "That's not a command, mon.")

help_text = \
'''How to use me:
     /chefit *help*: Shows this text
     /chefit *hello*: Tells you Hi!
     /chefit *orders*: '''

def process_command(command):
    if 'hello' == command:
        return {
            'response_type': 'ephemeral',
            'text': 'Hi, I\'m new here!'
        }

    elif 'help' in command:
        return {
            'response_type': 'ephemeral',
            'text': help_text
        }

    elif 'orders' == command:
        return {
            'response_type': 'in_channel',
            'text': 'Coming soon!'
        }
    else:
        return None

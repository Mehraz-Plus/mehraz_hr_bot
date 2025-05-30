from telethon import Button

def get_start_buttons(msg, config, is_admin=False):
    buttons = []
    buttons.append([Button.inline(msg.get('send_cv'), b'send_cv')])
    buttons.append([Button.inline(msg.get('start_soft_interview'), b'start_soft_interview')])
    buttons.append([Button.inline(msg.get('start_technical_interview'), b'start_technical_interview')])
    return buttons
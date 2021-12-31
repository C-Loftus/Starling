import pyautogui
import enum

class mode(enum.Enum):
    COMMAND = 1
    DICTATION = 2
    SHELL = 3
    SLEEP = 4

modifiers = ['ctrl', 'alt', 'shift', 'super']

def handle_transcription(transcription, current_mode):
    # Only use the first index since we are only parsing one wav file
    transcription = transcription[0]

    changed, switched_mode = _check_switch_request(transcription, current_mode)

    if changed is True:
        current_mode = switched_mode
    else:
        if current_mode == mode.COMMAND:
            _run_command(transcription)
        elif current_mode == mode.DICTATION:
            _run_dictation(transcription)
        elif current_mode == mode.SHELL:
            _run_shell(transcription)
        elif current_mode == mode.SLEEP:
            pass
        else:
            print("Invalid mode")
    
    return current_mode

def _check_switch_request(transcription, curr_mode):
    changed = True
    if 'command mode' in transcription:
        switch = mode.COMMAND
    elif 'dictation mode' in transcription:
        switch = mode.DICTATION
    elif 'shell mode' in transcription:
        switch = mode.SHELL
    elif 'sleep mode' in transcription:
        return mode.SLEEP
    else:
        changed = False
        switch = curr_mode

    return changed, switch

def _run_dictation(transcription):
    pyautogui.typewrite(transcription)

# Runs a default shell with the given command
# -i -c allows for system aliases
def _run_shell(transcription):
    import subprocess
    from os import environ
    shell = environ['SHELL']
    subprocess.call([shell, '-i', '-c', transcription])


def _run_command(transcription):
    for key in modifiers:
        if key in transcription:
            pass
    for word in transcription:
        if word in alphabet:
            pass    
    

if __name__ == '__main__':
    print(_run_dictation("command mode"))
    print(_run_dictation("test command"))
    print(_run_shell("shell mode"))

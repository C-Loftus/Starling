import pyautogui
import enum

class mode(enum.Enum):
    COMMAND = 1
    DICTATION = 2
    SHELL = 3

modifiers = ['ctrl', 'alt', 'shift', 'super']

def handle_transcription(transcription, current_mode):
    # Only use the first index since we are only parsing one wav file
    transcription = transcription[0]

    if current_mode == mode.COMMAND:
        _run_command(transcription)
    elif current_mode == mode.DICTATION:
        _run_dictation(transcription)
    elif current_mode == mode.SHELL:
        _run_shell(transcription)
    else:
        print("Invalid mode")

def _run_dictation(transcription):
    current_mode = mode.DICTATION
    if 'command mode' in transcription:
        current_mode = mode.COMMAND
    elif 'shell mode' in transcription:
        current_mode = mode.SHELL
    else:
        pyautogui.typewrite(transcription)
    return current_mode

# subprocess.call(['/bin/bash', '-i', '-c', command])
def _run_shell(transcription):
    pass

def _run_command(transcription):
    pass

if __name__ == '__main__':
    print(_run_dictation("command mode"))
    print(_run_dictation("test command"))

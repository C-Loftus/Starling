import multiprocessing
import subprocess
import pyautogui
import enum
from typing import List

class mode(enum.Enum):
    COMMAND = 1
    DICTATION = 2
    SHELL = 3
    SLEEP = 4

# command category
class category(enum.Enum):
    ALPHABET = 1
    MODIFIER = 2
    ACTION = 3
    NATURAL = 4
    APPLICATION = 5

KEY_INDEX = 0
DESCRIPTION_INDEX = 1

def handle_transcription(transcription, current_mode, CONF):
    # Only use the first index since we are only parsing one wav file
    transcription = transcription[0]

    changed, switched_mode = _check_switch_request(transcription, current_mode)

    if changed is True:
        current_mode = switched_mode
    else:
        if current_mode == mode.COMMAND:
            _run_command(transcription, CONF)
        elif current_mode == mode.DICTATION:
            _run_dictation(transcription, CONF)
        elif current_mode == mode.SHELL:
            _run_shell(transcription, CONF)
        elif current_mode == mode.SLEEP:
            pass
        else:
            raise Exception("Invalid mode") 
    
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
        switch =  mode.SLEEP
    # don't change anything if no switch is requested
    else:
        changed = False
        switch = curr_mode

    return changed, switch

def _run_dictation(transcription):
    pyautogui.typewrite(transcription)


def _run_shell(transcription, CONF):
    
    '''
    it is dangerous to run shell commands based off voice input.
    However, it is also very useful since the user can run any command
    in their .basrc/config.fish/etc. This is very convenient

    it is impossible to check every unsafe command in the shell since the 
    user can alias commands and what exactly is not safe  depends on the user's
    machine. The best way is to automatically create a nonblocking pop up, 
    that if not interacted with, will automatically close and execute the command.  
      
    If you need low latency, just using the terminal may be preferred.

    If you want convenience and safety, this may be better. 
    '''

    import time
    import subprocess
    from multiprocessing import Process
    from os import environ
    from threading import Thread

    safety_time = CONF.get_safety_time()

    shell = environ['SHELL']
    message = 'Are you sure you want to run command \'{}\' in current shell {}?\n\
         Unless canceled, the command will be run automatically {} seconds after this window first appeared'\
         .format(transcription, shell, safety_time)

    q = multiprocessing.Queue()

    alert_thread = Process(target=_alert_wrapper, args=(message, q))
    alert_thread.start()
    
    # needs to be wrapped in order to sleep without blocking
    def cmd_wait_wrapper():
    
        # wait until the safety time is over
        time.sleep(safety_time)

        alert_thread.terminate()

        # check to see if the queue returned a message that would indicate a cancel
        try:
            result = q.get(block=False)
            #  we only need to check for cancel since that is the only thing it can return
            if result == 'CANCEL':
                print(f'Cancelled command: {transcription}')
        # An exception means the queue was empty and the user did not cancel
        except:
            subprocess.call([shell, '-i', '-c', transcription])

    
    cmd_wait_thread = Thread(target=cmd_wait_wrapper, args=())
    cmd_wait_thread.start()

# Wrapper needed because alert is blocking
def _alert_wrapper(message, q):
    result = pyautogui.alert(text=message, title='Safety Check Shell Command', button='CANCEL')
    q.put(result)

def _run_command(transcription, CONF):
    #  xdotool getwindowfocus getwindowname
    p = subprocess.Popen(['xdotool', 'getwindowfocus', 'getwindowname'], stdout=subprocess.PIPE)
    context = p.stdout.read()

    context_cmds = CONF.try_get_context(context)

    alphabet = CONF.get_alphabet()
    result = _parse_command(transcription, alphabet)

    natural_command = ""

    for command in result:

        for key in command:
            if key[DESCRIPTION_INDEX] == category.NATURAL:
                natural_command += key[KEY_INDEX]

            elif key[DESCRIPTION_INDEX] == 'modifier' or key[DESCRIPTION_INDEX] == 'alphabet':
                pyautogui.keyDown(key[KEY_INDEX])

            if key[DESCRIPTION_INDEX] == "action":
                if key[KEY_INDEX] == 'focus':
                    subprocess.call(['xdotool', 'search', '--class', 'kitty', 'windowactivate'])
                
def _parse_command(transcription, alphabet):

    '''
    Command Format:
    ((modifiers)* (alphabet)*) || ((focus/close/open) (editor/terminal/browser))
    '''

    modifiers = {'ctrl', 'alt', 'shift', 'super'}
    window_actions = {'focus', 'open', 'close'}
    applications = {'editor', 'terminal', 'browser'}
    
    cmdList: List[List[str]] = []
    currCmd: List[(str, str)] = []

    for index, word in enumerate(transcription.split()):

        try:
            lastTerm = currCmd[-1]
        except:
            lastTerm = None

        # modifiers only begin cmds or follow other modifiers
        if word in modifiers:

            if (lastTerm is None or lastTerm not in modifiers) and index != 0:
                cmdList.append(currCmd)
                currCmd = []

            currCmd.append((word, category.MODIFIER))

        # There can only be one cmd term for every cmd
        # i.e. it doesn't make sense to have 'close focus browser'
        # thus you always break it off to its own cmd
        elif word in window_actions:
            cmdList.append(currCmd)
            currCmd = []
            currCmd.append((word, category.ACTION))

        elif word in alphabet:
            currCmd.append((alphabet[word], category.ALPHABET))

        elif word in applications:
            if (lastTerm is not None):
                # only append applications when the last word was an action
                # doesn't make sense to make a command like 'shift super firefox'
                if lastTerm[DESCRIPTION_INDEX] == 'action':
                    currCmd.append((word, category.APPLICATION))

        # handle natural speech commands
        else:
            if index != 0:
                if (lastTerm is None):
                    cmdList.append(currCmd)
                    currCmd = []
                elif (lastTerm[DESCRIPTION_INDEX] != category.NATURAL):
                    cmdList.append(currCmd)
                    currCmd = []
            
            currCmd.append((word, category.NATURAL))
            

    # add last command to list. Not handled otherwise
    if currCmd != []:
        cmdList.append(currCmd)

    return cmdList


class command_list:
    current_command = []
    command_list = []

    def __init__(self):
        return

    def add_to_current_command(self, command: str):
        self.current_command.append(command)  

    def finish_this_command(self, command: str):
        self.command_list.append(command)
        self.current_command = []


if __name__ == '__main__':
    # print(_run_dictation("command mode"))
    # print(_run_dictation("test command"))
    # _run_shell("echo test", safety_time=10)Hello world!
    print(_parse_command("shift super b b b b c super", alphabet={"a": "a", "b": "b", "c": "c"}))
    print("\n")
    print(_parse_command("shift super b b focus editor focus alg volume down", alphabet={"a": "a", "b": "b", "c": "c"}))
    print("\n")
    print(_parse_command("shift down super a editor escape a a shift b b", alphabet={"a": "a", "b": "b", "c": "c"}))
    print("\n")
    print(_parse_command("volume down super c volume up", alphabet={"a": "a", "b": "b", "c": "c"}))

    import os, sys
    # getting the name of the directory
    # where the this file is present.
    current = os.path.dirname(os.path.realpath(__file__))
    
    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)
    
    # adding the parent directory to 
    # the sys.path.
    sys.path.append(parent)
    
    import setup_conf

    CONF = setup_conf.application_config("config.yaml")

    _run_command("super cap", CONF=CONF)

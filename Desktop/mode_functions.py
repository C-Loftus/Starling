import multiprocessing
import subprocess
import pyautogui
import enum
from typing import List, final
import time
import subprocess
from multiprocessing import Process
from os import environ
from threading import Thread

# python hacky fix to import up a directory
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import setup_conf

# entire application mode
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

# gets it into the format for pyautogui
def _join_cmd_words(cmd_words):
    WORD_INDEX = 0
    ACTION_INDEX = 1
    if cmd_words[0][ACTION_INDEX] == category.NATURAL:
        result = ""
        for word in cmd_words:
            result += word[WORD_INDEX] + " "
        return result.strip()
    else:
        result = []
        for word in cmd_words:
            result.append(word[WORD_INDEX])
        return result
        

def _run_command(transcription, CONF):

    context = get_focused_window_name()
    context_cmds = CONF.get_context_cmds(context)

    alphabet = CONF.get_alphabet()
    result = _parse_command(transcription, alphabet)

    ACTION_INDEX = 1

    for command in result:
        print("running", command)
        # first index enough to tell type of full cmd
        typeOfAction = command[0][ACTION_INDEX]

        final_cmd = _join_cmd_words(command)

        if typeOfAction == category.NATURAL:
            try:
                decode_cmd = context_cmds[final_cmd]
                pyautogui.hotkey(*decode_cmd.split())
            except:
                print(f'Could not find natural command \'{command}\'\
                in context {context} with commands {context_cmds}')
        
        elif typeOfAction == category.ACTION:
            pass

        elif typeOfAction == category.ALPHABET or typeOfAction == category.MODIFIER:
            pyautogui.hotkey(*final_cmd)


def _parse_command(transcription, alphabet):

    '''
    Command Format:
    ((modifiers)* (alphabet)*) || ((focus/close/open) (editor/terminal/browser))
    '''

    modifiers = {'ctrl', 'alt', 'shift', 'super', 'win'}
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
            #pyauto gui only uses win not super
            if word == 'super':
                word = 'win'

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


def get_focused_window_name():
    import re

    def xprop():
        with subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE) as toplevel:
            for line in toplevel.stdout:
                line = str(line, encoding="UTF-8")

                m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
                if m is not None:
                    id_ = m.group(1)
                    with subprocess.Popen(['xprop', '-id', id_, 'WM_NAME'],
                            stdout=subprocess.PIPE) as id_w:
                        for line in id_w.stdout:
                            line = str(line, encoding="UTF-8")
                            match = re.match("WM_NAME\(\w+\) = \"(?P<name>.+)\"$",
                                            line)
                        if match is not None:
                            return match.group("name")
                    break
        return None

    output = xprop()

    try: 
        output.strip()
        output = (re.split('- |_  |— |\*|\n',output)[-1])
    except:
        output = ""
        
    return output





if __name__ == '__main__':

    # # print(_run_dictation("command mode"))
    # # print(_run_dictation("test command"))
    # # _run_shell("echo test", safety_time=10)Hello world!
    # print(_parse_command("shift super b b b b c super", alphabet={"a": "a", "b": "b", "c": "c"}))
    # print("\n")
    # print(_parse_command("shift super b b focus editor focus alg volume down", alphabet={"a": "a", "b": "b", "c": "c"}))
    # print("\n")
    # print(_parse_command("shift down super a editor escape a a shift b b", alphabet={"a": "a", "b": "b", "c": "c"}))
    # print("\n")
    # print(_parse_command("volume down super c volume up", alphabet={"a": "a", "b": "b", "c": "c"}))


    print(get_focused_window_name())
    CONF = setup_conf.application_config("config.yaml")

    # print(_parse_command("super cap", alphabet=CONF.get_alphabet()))
    # _run_command("super cap", CONF=CONF)
    _run_command("new bookmark super cap", CONF=CONF)


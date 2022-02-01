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
try:
    import xdotool_wrappers
except:
    from . import xdotool_wrappers

# python way to import up a directory
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import setup_conf

# current mode that the application is running in
class mode(enum.Enum):
    COMMAND = enum.auto()
    DICTATION = enum.auto()
    SHELL = enum.auto()
    SLEEP = enum.auto()

# command category
class category(enum.Enum):
    ALPHABET = enum.auto()
    MODIFIER =enum.auto()
    ACTION =enum.auto()
    NATURAL =enum.auto()
    APPLICATION =enum.auto()
    NULL = enum.auto()

TERM_INDEX = 0
DESCRIPTION_INDEX = 1

def handle_transcription(transcription, current_mode, CONF):

    changed, switched_mode = _check_switch_request(transcription, current_mode)

    if changed is True:
        current_mode = switched_mode
    else:
        if current_mode == mode.COMMAND:
            _run_command(transcription, CONF)
        elif current_mode == mode.DICTATION:
            _run_dictation(transcription)
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
    # only need first item to determine if it is natural
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
        

def _run_command(transcription, CONF):\

    # check special cases
    if transcription.partition(' ')[0] == 'sentence':
        everything_but_sentence = transcription.partition(' ')[2]
        _run_dictation(everything_but_sentence)
        return

    context = xdotool_wrappers.get_focused_window_name()
    context_cmds = CONF.get_context_cmds(context)

    result: cmdList = _parse_command(transcription, CONF)

    for command in result.get_cmd_list():

        print("running", command)

        # first term in command enough to tell type of full cmd
        typeOfAction = command[0][DESCRIPTION_INDEX]

        final_cmd = _join_cmd_words(command)

        if typeOfAction == category.NATURAL:
            try:
                decode_cmd = context_cmds[final_cmd]
                pyautogui.hotkey(*decode_cmd.split())
            except:
                print(f'Could not find natural command {command} in context {context} with commands {context_cmds}')
        
        elif typeOfAction == category.ACTION:
            _handle_action(final_cmd, CONF)

        elif typeOfAction == category.ALPHABET or typeOfAction == category.MODIFIER:
            try:
                pyautogui.hotkey(*final_cmd)
            except:
                print(f'final_cmd: {final_cmd} is not made up of valid pyautogui hotkeys')
        else:
            # ignore commands that start with applications.
            # just saying 'Chrome' doesn't mean anything. 
            # Must have an action before it
            pass
    return

def _handle_action(final_command: List[str], CONF):

    if len(final_command) > 2:
        print("too many arguments")
        return

    action= final_command[0]
    application= final_command[1]
    
    app_id=xdotool_wrappers.get_id_from_name(application)
    print(f'action: {action}, app_id: {app_id}, application: {application}')

    if action == 'focus':
        xdotool_wrappers.focus_window_by_id(app_id)
    elif action == 'close':
        xdotool_wrappers.close_window_by_id(app_id)
    elif action == 'minimize':
        xdotool_wrappers.minimize_window_by_id(app_id)
    elif action == 'maximize':
        xdotool_wrappers.maximize_window_by_id(app_id)
    elif action == 'start':
        # Start a process on the system
        try:
            application_path = CONF.get_path(application)
            subprocess.Popen(application_path)
        except:
            print(f'Could not start {application} with path {application_path}')
    else:
        print(f'Unrecognized action: {action}')

class cmdList():
    def __init__(self):
        self.cmds: List[List] = []
        self.curr_cmd: List = []

    def add_to_curr_cmd(self, cmd, type):
        self.curr_cmd.append((cmd, type))
    
    def finish_and_add_to_list(self):
        if len(self.curr_cmd) > 0:
            self.cmds.append(self.curr_cmd)
            self.curr_cmd = []

    def get_curr_cmd(self):
        return self.curr_cmd

    def get_cmd_list(self):
        return self.cmds

    def get_previous_element(self):
        # previous element is the last one in the curr cmd
        try:
            return self.get_curr_cmd()[-1]
        except:
            return ("", category.NULL)


def _parse_command(transcription, CONF):

    '''
    Command Format:
    ((modifiers)* (alphabet)*) || ((focus/close/start) (editor/terminal/browser))
    '''

    modifiers = {'ctrl', 'alt', 'shift', 'super', 'win'}
    window_actions = {'focus', 'start', 'close', 'maximize', 'minimize'}
    applications = {'editor', 'terminal', 'browser', 'this'}

    alphabet = CONF.get_alphabet()

    cmd_list = cmdList()

    for index, word in enumerate(transcription.split()):

        previousElement = cmd_list.get_previous_element()
        previousDescription = previousElement[DESCRIPTION_INDEX]

        word = format_keys(word)
        
        # modifiers only begin cmds or follow other modifiers
        if word in modifiers:
            if (previousDescription != category.MODIFIER) and index != 0:
                cmd_list.finish_and_add_to_list()
            #pyauto gui only uses win not super
            cmd_list.add_to_curr_cmd(word, category.MODIFIER)

        # There can only be one cmd term for every cmd
        # i.e. it doesn't make sense to have 'close focus browser'
        # thus you always break it off to its own cmd
        elif word in window_actions:
            cmd_list.finish_and_add_to_list()
            cmd_list.add_to_curr_cmd(word, category.ACTION)

        # alphabet terms never end commands. Can be indefinitely long
        elif word in alphabet:
            cmd_list.add_to_curr_cmd(alphabet[word], category.ALPHABET)

        elif word in applications:
            # only append applications when the previous word was an action
            # doesn't make sense to make a command like 'shift super firefox'
            if previousDescription == category.ACTION:
                decodedApplication = decode_application(word, CONF)
                if decode_application != None:
                    cmd_list.add_to_curr_cmd(decodedApplication, category.APPLICATION)

        # handle natural speech commands
        else:
            if (previousDescription != category.NATURAL) and (previousDescription != category.ACTION):
                cmd_list.finish_and_add_to_list()
            cmd_list.add_to_curr_cmd(word, category.NATURAL)

    # Ad last command at the end of loop
    cmd_list.finish_and_add_to_list()

    return cmd_list

def decode_application(application: str, CONF):
    '''
    Decodes the application name from the config file
    '''
    if application == "this":
        return xdotool_wrappers.get_focused_window_name()
    else:
        try:
            return CONF.get_config()[application]
        except:
            return None

def format_keys(word):
    if word == 'super':
        return 'win'
    if word == "control":
        return 'ctrl'
    return word

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


    # print(get_focused_window_name())
    CONF = setup_conf.application_config("config.yaml")

    # print(_parse_command("focus editor focus editor focus mozilla firefox focus super cap focus editor mozilla firefox", CONF).get_cmd_list())
    # print(_parse_command("super cap super bat", CONF).get_cmd_list())

    # _run_command("new bookmark super cap", CONF=CONF)

    # test = [("start", None),('firefox', None)]
    test = ["start", "Mozilla Firefox"]
    _handle_action(test, CONF)


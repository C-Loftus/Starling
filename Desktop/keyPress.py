import multiprocessing
from threading import Thread
from numpy import result_type
import pyautogui
import enum

class mode(enum.Enum):
    COMMAND = 1
    DICTATION = 2
    SHELL = 3
    SLEEP = 4

modifiers = {'ctrl', 'alt', 'shift', 'super'}

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
        return mode.SLEEP
    # don't change anything if no switch is requested
    else:
        changed = False
        switch = curr_mode

    return changed, switch

def _run_dictation(transcription):
    pyautogui.typewrite(transcription)


def _run_shell(transcription, safety_time=10):
    import time
    import subprocess
    from multiprocessing import Process
    from os import environ
    shell = environ['SHELL']
    message = 'Are you sure you want to run command \'{}\' in current shell {}? \n \
         Running command automatically in {} seconds'.format(transcription, shell, safety_time)

    q = multiprocessing.Queue()

    alert_thread = Process(target=_alert_wrapper, args=(message, q))
    alert_thread.start()

    # wait until the safety time is over
    time.sleep(safety_time)

    alert_thread.terminate()
    # check to see if the queue returned a message that would indicate a cancel
    try:
        result = q.get(block=False)
        #  we only need to check for cancel since that is the only thing it can return
        if result == 'CANCEL':
            print(f'Cancelled command: {transcription}')
            return
    # An exception means the queue was empty and the user did not cancel
    except:
        subprocess.call([shell, '-i', '-c', transcription])
         

# This has to be wrapped in a process because alert is blocking
def _alert_wrapper(message, q):
    result = pyautogui.alert(text=message, title='Error', button='CANCEL')
    q.put(result)

def _run_command(transcription):
    for key in modifiers:
        if key in transcription:
            pass
    for word in transcription:
        if word in alphabet:
            pass    
    

if __name__ == '__main__':
    # print(_run_dictation("command mode"))
    # print(_run_dictation("test command"))
    _run_shell("echo test", safety_time=3)

# python way to import up a directory
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.AppIndicator import gtk_indicator
from src.AppIndicator import socket_fns

from time import sleep
from multiprocessing import Process

def set_icon_to_red():
    p = Process(target=gtk_indicator.ProgramIndicator, args=(10,))
    p.start()
    sleep(2)
    s = socket_fns.ClientSocket()
    s.check_to_send("old", "new", "command mode")
    sleep(2)
    s.check_to_send("old", "new", "quit application")
    ## process should have closed

def end_app_through_menu():
    p = Process(target=gtk_indicator.ProgramIndicator, args=(10,))
    p.start()
    print("here")
    sleep(2)
    s = socket_fns.ClientSocket()
    p.terminate()
    assert(s.s is None)
    
    

if __name__ == "__main__":
    p = Process(target= set_icon_to_red)
    p.start()
    p.join()
    # end_app_through_menu()
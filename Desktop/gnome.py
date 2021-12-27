import gi, os, sys
import time 
from multiprocessing import Process, Lock
from threading import Thread
from playsound import playsound
gi.require_version('Notify', '0.7')
from gi.repository import Notify

def timer_wait(lock, title, message=None, extra=None, seconds=None):
    with lock:
        Notify.init("Hello world")
        n=Notify.Notification.new( title,
                                    message,
                                    extra)
        # n.set_timeout(0)
        print(f'Starting timer for {seconds} seconds')

        time.sleep(seconds)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "bowl.mp3")

        sound_thread = Thread(target=playsound, args=(filename,))
        sound_thread.start()

        n.show()


def make_gnome_timer(lock, title=None, message=None, extra=None, seconds=None):
    p = Process(target=timer_wait, args=(lock, title, message, extra, seconds))
    p.start()
    return p

def default_timer_conf():
    timer_lock = Lock()
    seconds = 60 * 5
    message, extra, = None, None
    if len(sys.argv) > 1:
        minutes = sys.argv[1]
        seconds = int(minutes) * 60

    while True:
        for i in range(0,2):
            if i == 1:
                title = "Break"
                message = "take a break for {} minutes".format(minutes)
                extra = "Break"
            else:
                title = "Timer"
                meesage= "Timer for {} minutes".format(minutes)
                extra = "timer"
            p = make_gnome_timer(timer_lock, title="Timer", message=message, extra=extra, seconds=seconds)
            print("change")
            p.join()


if __name__ == "__main__":
    default_timer_conf()


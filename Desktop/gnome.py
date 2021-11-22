import gi
from threading import Thread
import time 
from multiprocessing import Process, Lock
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
        playsound("Assets/Sounds/bowl.mp3")
        n.show()


def make_gnome_timer(lock, title=None, message=None, extra=None, seconds=None):
        p = Process(target=timer_wait, args=(lock, title, message, extra, seconds))
        p.start()
        return p


if __name__ == "__main__":
    make_gnome_timer("timer", seconds=5)
    print("test")


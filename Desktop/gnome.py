import gi, os, sys
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
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "bowl.mp3")

        playsound(filename)
        n.show()


def make_gnome_timer(lock, title=None, message=None, extra=None, seconds=None):
        p = Process(target=timer_wait, args=(lock, title, message, extra, seconds))
        p.start()
        return p


if __name__ == "__main__":
    timer_lock = Lock()
    seconds = 60 * 5
    if len(sys.argv) > 1:
        minutes = sys.argv[1]
        seconds = int(minutes) * 60

    while True:
        p = make_gnome_timer(timer_lock, title="Timer", seconds=seconds)
        print("mainthread")
        p.join()


from pynput import keyboard, mouse
 
 # echo Hello | osd_cat -p bottom -A center -o -80

# sudo apt install libxosd2 xosd-bin

# osd_cat -A center --pos bottom --color white -u transparent -f "-*-*-medium-*-*-*-*-*-*-*-*-120-*-*" token

# font is in the X font format
import os
from threading import Thread

def screen_print(message, font="-*-*-medium-*-*-*-*-*-*-*-*-120-*-*"):

    thread = Thread(target=os.system, \
        args=("echo {} | osd_cat \
             -A center --pos bottom --color white -u transparent -f {}"
             .format(message, font),)
        )
    thread.start()

    return thread

# detect how long user has been working on the keyboard
def detect_time_for_break(min_until_break):
    from datetime import time, datetime
    import time as t

    def idle_time():
        #xprintidle
        import subprocess
        p = subprocess.Popen(["xprintidle"], stdout=subprocess.PIPE)
        out = p.stdout.read()
        return int(out)

    def work_time():
        time = 0
        while True:
            # We can use slow polling since only long breaks matter
            t.sleep(30)
            time += 30
            # 5 min in milliseconds
            # If this is true then that means the user took a break 
            # and thus don't need to take another one
            print(idle_time())
            if idle_time() > 300000:
                time = 0
                print("break detected")
            elif (time / 60) > (min_until_break):
                screen_print("Time to take a break!")

    thread = Thread(target=work_time)
    thread.start()

    return thread


if __name__ == '__main__':
    screen_print('Hello')
    detect_time_for_break(1)
    print("mainthread")
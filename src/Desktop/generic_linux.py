 # echo Hello | osd_cat -p bottom -A center -o -80

# osd_cat -A center --pos bottom --color white -u transparent -f "-*-*-medium-*-*-*-*-*-*-*-*-120-*-*" token

# font is in the X font format
import os
from threading import Thread
from multiprocessing import Process
from turtle import pos

def screen_print(message,  delay=2, font="-*-*-medium-*-*-*-*-*-*-*-*-120-*-*", position="bottom"):

    thread = Thread(target=os.system, \
        args=("echo {} | osd_cat --delay={} \
             -A center --pos {} --color white -u blue -O 2 -f {}"
             .format(message, delay, position, font),)
        )
    thread.start()

# detect how long user has been working on the keyboard
def timer_create(min_until_break, delay):
    import time as t
    seconds_until_break = min_until_break * 60

    screen_print("Timer starting with {} min intervals".format(min_until_break), delay)

    def idle_time():
        #xprintidle
        import subprocess
        p = subprocess.Popen(["xprintidle"], stdout=subprocess.PIPE)
        out = p.stdout.read()
        return float(out) / 1000 / 60

    def work_time():
        time = 0
        while True:
            # We can use slow polling since only long breaks matter
            t.sleep(30)
            time += 30
            # 5 min in milliseconds
            # If this is true then that means the user took a break 
            # and thus don't need to take another one

            # round to 4 decimal places
            print(f'Idle time = {round(idle_time(), 4)} minutes')

            if idle_time() > 5.0:
                time = 0
                print("break detected")
            elif (time) > (seconds_until_break):
                screen_print('Time to take a break!', delay=delay)

    p = Process(target=work_time)
    p.start()

    return p


if __name__ == '__main__':
    from time import gmtime, strftime
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    screen_print("Starting", delay=5, position="middle")
    print("starting")
    timer_create(30, delay=5)
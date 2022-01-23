 # echo Hello | osd_cat -p bottom -A center -o -80

# osd_cat -A center --pos bottom --color white -u transparent -f "-*-*-medium-*-*-*-*-*-*-*-*-120-*-*" token

# font is in the X font format
import os
from threading import Thread

def screen_print(message,  delay=2, font="-*-*-medium-*-*-*-*-*-*-*-*-120-*-*"):

    thread = Thread(target=os.system, \
        args=("echo {} | osd_cat --delay={} \
             -A center --pos bottom --color white -u blue -O 2 -f {}"
             .format(message, delay, font),)
        )
    thread.start()

# detect how long user has been working on the keyboard
def timer_create(min_until_break):
    from datetime import time, datetime
    import time as t
    seconds_until_break = min_until_break * 60

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
                screen_print('Time to take a break! You have idled for {} minutes'.format(int(time)))

    thread = Thread(target=work_time)
    thread.start()

    return thread


if __name__ == '__main__':
    from time import gmtime, strftime
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    screen_print("Starting", delay=10)
    print("starting")
    timer_create(30)
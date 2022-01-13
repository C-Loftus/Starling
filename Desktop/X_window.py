import subprocess, psutil, re

def get_focused_window_name():
    # xdotool getactivewindow getwindowname
    p = subprocess.Popen(['xdotool', 'getactivewindow', 'getwindowname'], stdout=subprocess.PIPE)
    name = (p.stdout.read().decode('utf-8'))
    name.strip()
    name = (re.split('- |_  |— |\*',name)[-1])
    return name.rstrip()

def close_process(pid):
    process = psutil.Process(pid)
    process.kill()

def close_window_by_id(id):
    #  xdotool windowclose id
    p = subprocess.Popen(['xdotool', 'windowclose', id], stdout=subprocess.PIPE)

def get_id_from_name(name):
    s = subprocess.Popen(['xdotool', 'search', '--onlyvisible', '--name', name], stdout=subprocess.PIPE)
    return s.stdout.read().decode('utf-8').rstrip()

def get_focused_window_pid():
    # xdotool getactivewindow getwindowpid
    p = subprocess.Popen(['xdotool', 'getactivewindow', 'getwindowpid'], stdout=subprocess.PIPE)
    pid = p.stdout.read().decode('utf-8')
    return int(pid)

if __name__ == "__main__":
    from time import sleep
    w = get_focused_window_name()
    print(w)
    sleep(3)
    close_window_by_id(get_id_from_name("Visual Studio Code"))

    # close_process(get_focused_window_pid())
   
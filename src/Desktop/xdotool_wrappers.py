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
    try:
        return s.stdout.read().decode('utf-8').rstrip().split()[-1]
    except:
        return ""

def get_focused_window_pid():
    # xdotool getactivewindow getwindowpid
    p = subprocess.Popen(['xdotool', 'getactivewindow', 'getwindowpid'], stdout=subprocess.PIPE)
    pid = p.stdout.read().decode('utf-8{')
    return int(pid)

def focus_window_by_id(id):
    # xdotool windowactivate id
    p = subprocess.Popen(['xdotool', 'windowactivate', id], stdout=subprocess.PIPE)

def minimize_window_by_id(id):
    # xdotool windowminimize id
    p = subprocess.Popen(['xdotool', 'windowminimize', id], stdout=subprocess.PIPE)

def maximize_window_by_id(id):
    # xdotool windowmaximize id
    p = subprocess.Popen(['xdotool', 'windowsize', id, '100%', '100%'], stdout=subprocess.PIPE)

if __name__ == "__main__":
    from time import sleep
    w = get_focused_window_name()
    print(w)

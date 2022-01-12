import subprocess, psutil, re

# def get_focused_window_name():
#     def xprop():
#         with subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE) as toplevel:
#             for line in toplevel.stdout:
#                 line = str(line, encoding="UTF-8")

#                 m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
#                 if m is not None:
#                     id_ = m.group(1)
#                     with subprocess.Popen(['xprop', '-id', id_, 'WM_NAME'],
#                             stdout=subprocess.PIPE) as id_w:
#                         for line in id_w.stdout:
#                             line = str(line, encoding="UTF-8")
#                             match = re.match("WM_NAME\(\w+\) = \"(?P<name>.+)\"$",
#                                             line)
#                         if match is not None:
#                             return match.group("name")
#                 break
#         return None

#     output = xprop()

#     try: 
#         output.strip()
#         output = (re.split('- |_  |— |\*|\n',output)[-1])
#     except:
#         output = ""

#     return output

def get_focused_window_name():
    # xdotool getactivewindow getwindowname
    p = subprocess.Popen(['xdotool', 'getactivewindow', 'getwindowname'], stdout=subprocess.PIPE)
    name = (p.stdout.read().decode('utf-8'))
    name.strip()
    name = (re.split('- |_  |— |\*',name)[-1])
    return name

def close_process(pid):
    process = psutil.Process(pid)
    process.kill()

def get_id_from_name(name):
    s = subprocess.Popen(['xdotool', 'search', '--onlyvisible', '--name', name], stdout=subprocess.PIPE)
    return s.stdout.read().decode('utf-8')

def get_focused_window_pid():
    # xdotool getactivewindow getwindowpid
    p = subprocess.Popen(['xdotool', 'getactivewindow', 'getwindowpid'], stdout=subprocess.PIPE)
    pid = p.stdout.read().decode('utf-8')
    return int(pid)

if __name__ == "__main__":
    from time import sleep
    print(get_focused_window_name())
    # print(get_id_from_name("Google Chrome"))
    # sleep(3)
    # close_process(get_focused_window_pid())
   
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.vosk_bindings.decoder import VoskModel as v



d= v()
t=d.run_inference("command_mode",None)
print(t)




# if __name__ == '__main__':
    
#     # # print(_run_dictation("command mode"))
#     # # print(_run_dictation("test command"))
#     # # _run_shell("echo test", safety_time=10)Hello world!
#     # print(_parse_command("shift super b b b b c super", alphabet={"a": "a", "b": "b", "c": "c"}))
#     # print("\n")
#     # print(_parse_command("shift super b b focus editor focus alg volume down", alphabet={"a": "a", "b": "b", "c": "c"}))
#     # print("\n")
#     # print(_parse_command("shift down super a editor escape a a shift b b", alphabet={"a": "a", "b": "b", "c": "c"}))
#     # print("\n")


#     # print(get_focused_window_name())
#     CONF = setup_conf.application_config("config.yaml")

#     # print(_parse_command("focus editor focus editor focus mozilla firefox focus super cap focus editor mozilla firefox", CONF).get_cmd_list())
#     # print(_parse_command("super cap super bat", CONF).get_cmd_list())

#     # _run_command("new bookmark super cap", CONF=CONF)

#     # test = [("start", None),('firefox', None)]
#     test = ["start", "Mozilla Firefox"]
#     _handle_action(test, CONF)
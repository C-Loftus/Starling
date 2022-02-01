import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.vosk_bindings.decoder import VoskModel as v



d= v()
t=d.run_inference("command_mode",None)
print(t)
from operator import gt
import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import src.AppIndicator.gtk_indicator as gtk_indicator
import src.setup_conf as setup_conf

def timer_test():
    CONF = setup_conf.application_config("config.yaml")
    indicator = gtk_indicator.ProgramIndicator(CONF)

if __name__ == '__main__':
    timer_test()
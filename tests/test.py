#!/usr/bin/python

# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# https://gist.github.com/candidtim/7290a1ad6e465d680b68

import os
import signal
import subprocess

import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify



APPINDICATOR_ID = 'scriptindicator'

# https://commons.wikimedia.org/wiki/File:Red_x.svg

# / https://commons.wikimedia.org/wiki/File:Eo_circle_green_blank.svg
def main(break_time):
    import time
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('Assets/green.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu(break_time))
    notify.init(APPINDICATOR_ID)
    # indicator.set_icon(os.path.abspath('Assets/red.svg'))

# /https://stackoverflow.com/questions/8826523/gtk-main-and-unix-sockets
    return gtk.main()

def build_menu(break_time):
    menu = gtk.Menu()

    item_script = gtk.MenuItem('script')
    item_script.connect('activate', script)

    menu.append(item_script)

    enable = gtk.MenuItem('enable auto break timer')
    enable.connect('activate', script)
    menu.append(enable)

    disable = gtk.MenuItem('disable auto break timer')
    disable.connect('activate', script)
    menu.append(disable)


    item_quit1 = gtk.MenuItem('Quit')
    item_quit1.connect('activate', quit1)
    menu.append(item_quit1)

    menu.show_all()
    return menu

def script(_):
    subprocess.call("echo test", shell=True)
    return script

def quit1(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indc = main(5)
#!/usr/bin/python

# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# https://gist.github.com/candidtim/7290a1ad6e465d680b68

from multiprocessing.connection import Client
import os
import re
import signal
import subprocess

import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GLib
from socket import socket   
# try:
#     from socket_fns import ClientSocket
# except:
#     from AppIndicator.socket_fns import ClientSocket    

import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from AppIndicator.socket_fns import ClientSocket    
from Desktop.generic_linux import *

PORT = ClientSocket.PORT

APPINDICATOR_ID = 'scriptindicator'

# Indicator for shell mode
# https://commons.wikimedia.org/wiki/File:Eo_circle_green_blank.svg
GREEN_PATH = 'src/Assets/green.svg'

# Indicator for command mode
# https://commons.wikimedia.org/wiki/File:Red_star.svg
ORANGE_PATH = 'src/Assets/orange.svg'

# Indicator for command mode
# <a href="https://commons.wikimedia.org/wiki/File:Triangle_blue.svg">Константине12591</a>, Public domain, via Wikimedia Commons
BLUE_PATH = 'src/Assets/blue.svg'

# Indicator for sleep mode
# https://commons.wikimedia.org/wiki/File:Creative-Tail-Halloween-half-moon.svg
SLEEP_PATH = 'src/Assets/moon1.svg'

class ProgramIndicator:
    timer = None
    CONF = None

    def __init__(self, CONF):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(ORANGE_PATH), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu(CONF))
        notify.init(APPINDICATOR_ID)
        self.CONF=CONF

    # /https://stackoverflow.com/questions/8826523/gtk-main-and-unix-sockets
        self.s = socket()    
        self.s.bind(('localhost', PORT))    
        self.s.listen()    
        GLib.io_add_watch(GLib.IOChannel(self.s.fileno()), 0, GLib.IOCondition.IN, self.listener, self.s)    
        return gtk.main()

    def build_menu(self, CONF):
        menu = gtk.Menu()


        enable = gtk.MenuItem('enable auto break timer')
        enable.connect('activate', self.script)
        menu.append(enable)

        disable = gtk.MenuItem('disable auto break timer')
        disable.connect('activate', self.kill_script)
        menu.append(disable)


        item_quit1 = gtk.MenuItem('Quit')
        item_quit1.connect('activate', self.quit1)
        menu.append(item_quit1)

        menu.show_all()
        return menu

    def set_orange(self, source):
        self.indicator.set_icon(os.path.abspath(ORANGE_PATH))

    def set_green(self, source):
        self.indicator.set_icon(os.path.abspath(GREEN_PATH))

    def set_blue(self, source):
        self.indicator.set_icon(os.path.abspath(BLUE_PATH))

    def set_sleep(self, source):
        self.indicator.set_icon(os.path.abspath(SLEEP_PATH))

    def script(self, source):
        time_until_break = self.CONF.get_time_before_break()
        # delay of 5 is a sensible default for printing msg to screen 
        timer = timer_create(time_until_break, delay=5)
        self.timer=timer

        return self.script

    def kill_script(self, source):
        if self.timer != None:
            self.timer.kill()
        screen_print("Timer disabled")
        return self.kill_script


    def quit1(self, source):
        try:
            self.kill_script(self)
        finally:
            notify.uninit()
            gtk.main_quit()

    def listener(self, io, cond, sock):    
        conn = sock.accept()[0]    
        GLib.io_add_watch(GLib.IOChannel(conn.fileno()),0,GLib.IOCondition.IN, self.handler, conn)    
        return True    

    def handler(self, io, cond, sock):    
        recv = (sock.recv(1000)).decode()
        print("Received: ", recv)

        if 'command mode' in recv:
            self.set_orange(self)    
        elif 'dictation mode' in recv:
            self.set_blue(self)
        elif 'shell mode' in recv:
            self.set_green(self)
        
        elif 'sleep mode' in recv:
            self.set_sleep(self)
        
        elif 'quit application'in recv:
            pid = recv.split(' ')[0]
            os.kill(int(pid), signal.SIGTERM)
            self.quit1(self)

        elif 'start timer' in recv:
            self.script()
        elif 'stop timer' in recv:
            self.kill_script(self)
        else:
            print("Nothing to change")

        return True    

if __name__ == "__main__":
    indc = ProgramIndicator(10)
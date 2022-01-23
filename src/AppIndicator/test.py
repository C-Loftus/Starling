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
from gi.repository import GLib;    
from socket import socket   



APPINDICATOR_ID = 'scriptindicator'
GREEN_PATH = 'src/Assets/green.svg'
RED_PATH = 'src/Assets/red.svg'


class ProgramIndicator:

    # https://commons.wikimedia.org/wiki/File:Red_x.svg
    # https://commons.wikimedia.org/wiki/File:Eo_circle_green_blank.svg
    def __init__(self, break_time):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(GREEN_PATH), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu(break_time))
        notify.init(APPINDICATOR_ID)

    # /https://stackoverflow.com/questions/8826523/gtk-main-and-unix-sockets
        s = socket()    
        s.bind(('localhost', 50155))    
        s.listen()    
        GLib.io_add_watch(GLib.IOChannel(s.fileno()), 0, GLib.IOCondition.IN, self.listener, s)    
        return gtk.main()

    def build_menu(self, break_time):
        menu = gtk.Menu()

        item_script = gtk.MenuItem('script')
        item_script.connect('activate', self.script)

        menu.append(item_script)

        enable = gtk.MenuItem('enable auto break timer')
        enable.connect('activate', self.script)
        menu.append(enable)

        disable = gtk.MenuItem('disable auto break timer')
        disable.connect('activate', self.script)
        menu.append(disable)


        item_quit1 = gtk.MenuItem('Quit')
        item_quit1.connect('activate', self.quit1)
        menu.append(item_quit1)

        red = gtk.MenuItem('red')
        red.connect('activate', self.set_red)
        menu.append(red)

        menu.show_all()
        return menu

    def set_red(self, source):
        self.indicator.set_icon(os.path.abspath(RED_PATH))

    def set_green(self, source):
        self.indicator.set_icon(os.path.abspath(GREEN_PATH))

    def script(self, source):
        subprocess.call("echo test", shell=True)
        return self.script

    def quit1(self, source):
        notify.uninit()
        gtk.main_quit()

    def listener(self, io, cond, sock):    
        conn = sock.accept()[0]    
        GLib.io_add_watch(GLib.IOChannel(conn.fileno()),0,GLib.IOCondition.IN, self.handler, conn)    
        return True    

    def handler(self, io, cond, sock):    
        print(sock.recv(1000))
        self.set_red(self)    
        return True    

if __name__ == "__main__":
    indc = ProgramIndicator(10)
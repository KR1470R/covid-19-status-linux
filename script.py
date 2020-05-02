#!/usr/bin/env python3
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3
from bs4 import BeautifulSoup
import requests as req
import os,sys,time

def stop(source):
    Gtk.main_quit()
def get_data(command):
    global resp
    global soup
    global confirmed
    global recovered
    global deaths

    try:
        resp = req.get("https://news.google.com/covid19/map?hl=en-US&gl=US&ceid=US:en")
    except:
        print('Error connection! Please connect to internet and try again.')
        sys.exit()
    try:
        soup = BeautifulSoup(resp.text, 'lxml')
        confirmed = soup.findAll("div",{'class','UvMayb'})[0].string
        recovered = soup.findAll("div",{'class','UvMayb'})[1].string
        deaths = soup.findAll("div",{'class','UvMayb'})[2].string
    except:
        print('Something went wrong...\n Trying install packeges and run again.')
        os.system('pip3 install bs4\npip3 install lxml')
        print('Packages has been installed, restarting...')
        os.execl(sys.executable, sys.executable, *sys.argv)

get_data('run')
def create_menu():
    menu = Gtk.Menu()
    # menu item 1
    item_info = Gtk.MenuItem.new_with_label('😷 Confirmed: '+str(confirmed)+';   😵  Deaths:  '+str(deaths)+';   ♥  Recovred:'+str(recovered)+';')
    item_refresh = Gtk.MenuItem.new_with_label('Refresh')
    item_refresh.connect('activate',get_data)
    item_about = Gtk.MenuItem.new_with_label('About')

    # item_about.connect('activate', self.about)
    menu.append(item_info)
    menu.append(item_refresh)
    menu.append(item_about)

    # separator
    menu_sep = Gtk.SeparatorMenuItem()
    menu.append(menu_sep)
    # quit
    item_quit = Gtk.MenuItem.new_with_label('Quit')
    item_quit.connect('activate',stop)
    menu.append(item_quit)

    menu.show_all()
    return menu

app = '.'
iconpath = os.path.abspath('icon/ico.png')
indicator = AppIndicator3.Indicator.new(
    app, iconpath,
    AppIndicator3.IndicatorCategory.OTHER)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)       
indicator.set_menu(create_menu())
indicator.set_label("Covid-19", app)

signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
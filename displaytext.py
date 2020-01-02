from datetime import datetime
import time
import bs4
import telnetlib
import logging
from urllib.request import urlopen as uReq
import urllib.error
from bs4 import BeautifulSoup as soup

def telnet(txt):
    try:
        telnet = telnetlib.Telnet('vfddisplay.lan')
    except:
        logging.error('Cannot connect to display, make sure it is on the network with vfddisplay.lan')
        return
    telnet.write('\n\n'.encode('latin1'))
    telnet.write(chr(0x0D).encode('latin1')) #0x0D clear; 0x0F All Display; 0x0B scroll; 
    telnet.write(chr(0x10).encode('latin1'))  ##Displayposition   0x10  
    telnet.write(chr(0).encode('latin1'))    ##Position
    telnet.write(txt.encode('latin1'))

def feinstaub():
    my_url = 'http://192.168.21.119/values'
    try:
        uClient = uReq(my_url)
    except:
        logging.error('Cannot connect to {}'.format(my_url))
        return
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    page_soup = page_soup.findAll("td")
    telnet("Unsere Feinstaubsensorwerte:")
    time.sleep(2)
    telnet(page_soup[3].getText().replace(u'\xa0µg/m³', ' ug/m3') + " " +  page_soup[6].getText().replace(u'\xa0µg/m³', ' ug/m3') + " " + page_soup[10].getText().replace(u'\xa0°C', ' gC') + " " + page_soup[13].getText().replace(u'\xa0', ' '))
    time.sleep(10)

def termine():
    my_url = 'https://eigenbaukombinat.de/unsere-veranstaltungen/'
    try:
        uClient = uReq(my_url)
    except:
        logging.error('Cannot connect to {}'.format(my_url))
        return
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    page_soup.findAll("div",{"class":"entry-content"})
    page_soup.findAll("section",{"class":"ical"})
    page = page_soup.find("article").getText().replace(u'\xa0', '')
    #print(page)
    telnet("Unsere Termine im Ueberblick:")
    time.sleep(2)
    for line in page.split('\n'):
         #print(line)
         #import pdb; pdb.set_trace()
         try:
            telnet(line[:39])# .encode('utf8'))
         except UnicodeEncodeError:
            logging.error('UnicodeEncodeError:{}'.format(line))
         time.sleep(1.7)
         
def localtime():
    i = 10
    while i > 0:
       localtime = time.asctime( time.localtime(time.time()) )
       #print(localtime)
       telnet(localtime)
       time.sleep(1)
       i = i -1

def text():
    telnet("JUGEND HACKT Halle  dont panic!")
    time.sleep(5)
    telnet("Mit Code die Welt verbessern")
    time.sleep(3)

while True:
    localtime()
    feinstaub()
    termine()
    #text()

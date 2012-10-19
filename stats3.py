import curses
import time

from http.client import HTTPSConnection

import urllib.request
import base64
import getpass
import json

try: input = raw_input
except: pass

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def authorizedGithubRequest(uname, passwd, request):
  base_url = "api.github.com"

  c = HTTPSConnection(base_url)
  userAndPass = base64.b64encode(("%s:%s" % (uname, passwd)).encode('ascii')).decode('ascii')
  
  headers = { 'Authorization' : 'Basic %s' % userAndPass }

  c.request('GET', request, headers=headers)

  res = c.getresponse()

  return json.loads(res.read().decode('ascii'))

  request = urllib.request.Request(base_url + request)
  base64string = base64.b64encode(bytes("%s:%s" % (uname,  passwd), 'ascii')).decode('ascii')
  request.add_header('Authorization', 'Basic %s' % base64string)

  return json.loads(urllib.request.urlopen(request).read())

def main(stdscr, uname, passwd):
  curses.start_color()
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
  curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

  while True:
    orgs = authorizedGithubRequest(uname, passwd, '/users/zipcodeman/orgs')
    pos = 15

    for org in orgs:
      stdscr.addstr(pos, 5, org['login'], curses.color_pair(CYAN))
      pos += 1
    stdscr.refresh()
    time.sleep(60)

if __name__ == '__main__':
  uname  = input("Username: ")
  passwd = getpass.getpass('Password: ')
  curses.wrapper(main, uname, passwd)

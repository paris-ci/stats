import curses
import time
import urllib2
import base64
import getpass
import json

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def authorizedGithubRequest(uname, passwd, request):
  base_url = "https://api.github.com"

  request = urllib2.Request(base_url + request)
  base64string = base64.encodestring("%s:%s" % (uname,  passwd))               \
                        .replace('\n', '')
  request.add_header('Authorization', 'Basic %s' % base64string)

  return json.loads(urllib2.urlopen(request).read())

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
    print authorizedGithubRequest(uname, passwd, '/rate_limit')
    return
    orgs = authorizedGithubRequest(uname, passwd, '/users/zipcodeman/orgs')
    pos = 0
    for org in orgs:
      stdscr.addstr(pos, 0, org['login'])
      pos += 1
    stdscr.refresh()
    time.sleep(60)

if __name__ == '__main__':
  uname  = raw_input("Username: ")
  passwd = getpass.getpass('Password: ')
  curses.wrapper(main, uname, passwd)
  print authorizedGithubRequest(uname, passwd, '/rate_limit')

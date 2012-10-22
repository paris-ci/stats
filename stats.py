import curses
import time

try:
  from http.client import HTTPSConnection
except ImportError:
  from httplib import HTTPSConnection

import base64
import getpass
import json

try: input = raw_input
except: pass

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

class Github:
  def __init__(self, username, password):
    self.u = username
    self.p = password

  def setCredentials(self, u, p):
    self.u = u
    self.p = p

  def validCredentials(self):
    response = self.apiRequest('/rate_limit')
    
    if 'message' in response:
      print(response['message'])
    return 'rate' in response

  def apiRequest(self, request):
    base_url = "api.github.com"

    c = HTTPSConnection(base_url)
    userAndPass = base64.b64encode(("%s:%s" % (self.u, self.p))
                                              .encode('ascii')).decode('ascii')
    
    headers = { 'Authorization' : 'Basic %s' % userAndPass }

    c.request('GET', request, headers=headers)

    res = c.getresponse()

    return json.loads(res.read().decode('ascii'))

  def orgs(self, user=None, org=None):
    if org != None:
      return self.apiRequest('/orgs/' + str(org))
    elif user != None:
      return self.apiRequest('/users/' + str(user) + '/orgs')
    else:
      return self.apiRequest('/user/orgs')

  def user(self):
    return self.users()

  def users(self, user=None):
    if user != None:
      return self.apiRequest('/users/' + str(user))
    else:
      return self.apiRequest('/user')

  def myEvents(self, public=False, received=False):
    return self.events(user=self.u, public=public, received=received)

  def events(self, user=None, public=False, received=False, org=None, 
                   owner=None, repo=None):
    if user != None:
      req = "/users/%s/" % user
      if received:
        req += "received_events"
      else:
        req += "events"
      if public:
        req += "/public"

      return self.apiRequest(req)
    elif org != None:
      return self.apiRequest('/orgs/' + org + "/events")
    elif owner != None and repo != None:
      return self.apiRequest('/repos/%s/%s/events' % (owner, repo))
    else:
      return self.apiRequest('/events')

def main(stdscr, git):
  curses.start_color()
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
  curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

  summaryWidth = 50

  summaryWindow = curses.newwin(0, summaryWidth, 0, 0)
  streamWindow = curses.newwin(0, 0, 0, summaryWidth)

  count = 6

  while True:

    if count == 6:
      summaryWindow.clear()
      pos = 1
      count = 0
      user = git.user()
      realname = ""
      if 'name' in user and user['name'] != "":
        realname = "%s (%s)" % (user['name'], user['login'])
      else:
        realname = user['login']
      
      summaryWindow.addstr(pos, 1, realname, curses.color_pair(BLUE))
      pos += 1

      if 'email' in user and user['email'] != "":
        summaryWindow.addstr(pos, 1, user['email'], curses.color_pair(WHITE))
        pos += 1

      if 'location' in user and user['location'] != "":
        summaryWindow.addstr(pos, 1, user['location'], curses.color_pair(WHITE))
        pos += 1

      pos += 1
      summaryWindow.addstr(pos, 1, "following %d" % (user['following']))
      pos += 1
      summaryWindow.addstr(pos, 1, "followers %d" % (user['followers']))
      pos += 1

      orgs = git.orgs()
      if len(orgs) > 0:
        pos += 2
        summaryWindow.addstr(pos, 1, "Organizations:", curses.color_pair(CYAN))
        pos += 1

      for org in orgs:
        details = git.orgs(org=org['login'])
        summaryWindow.addstr(pos, 1, "   %s" % org['login'], curses.color_pair(GREEN))

        public_repos_string = str(details['public_repos']) + " public repos"
        summaryWindow.addstr(pos, summaryWidth-len(public_repos_string),
                             public_repos_string, curses.color_pair(GREEN))
        pos += 1
      
      summaryWindow.refresh()
    else:
      count += 1
    pos = 1
    events = git.myEvents()
    streamWindow.clear()
    try: # write until we fail
      for event in events:
        t = event['type']
        if t == 'PushEvent':
          data = event['payload']
          line = "%s pushed to repository %s" % (event['actor']['login'],
                                                 event['repo']['name'])
          streamWindow.addstr(pos, 1, line)
          pos += 1
          for commit in data['commits']:
            line = "    %s - %s" % (commit['sha'], commit['message'])
            streamWindow.addstr(pos, 1, line)
            pos += 1
          pos += 1
        elif t == "CreateEvent":
          data = event['payload']
          line = '%s created new repository %s' % (event['actor']['login'],
                                                    event['repo']['name'])
          streamWindow.addstr(pos, 1, line)
          pos += 1
          if data['description'] != "":
            streamWindow.addstr(pos, 1, "    " + data['description'])
            pos += 1
          pos += 1
    except: pass

    streamWindow.refresh()
    time.sleep(10)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    while True:
      uname  = input("Username: ")
      passwd = getpass.getpass('Password: ')
      git = Github(uname, passwd)
      if git.validCredentials():
        break

    curses.wrapper(main, git)

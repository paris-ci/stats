import curses
import time

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def main(stdscr):
  curses.start_color()
  if curses.has_colors():
    stdscr.addstr(0, 0, 'Black', curses.color_pair(BLACK))
    stdscr.addstr(1, 0, 'Red', curses.color_pair(RED))
    stdscr.addstr(2, 0, 'Green', curses.color_pair(GREEN))
    stdscr.addstr(3, 0, 'Yellow', curses.color_pair(YELLOW))
    stdscr.addstr(4, 0, 'Blue', curses.color_pair(BLUE))
    stdscr.addstr(5, 0, 'Magenta', curses.color_pair(MAGENTA))
    stdscr.addstr(6, 0, 'Cyan', curses.color_pair(CYAN))
    stdscr.addstr(7, 0, 'White', curses.color_pair(WHITE))
  else:
    stdscr.addstr(0, 0, 'No Colors')
  stdscr.refresh()
  time.sleep(10)

if __name__ == '__main__':
  curses.wrapper(main)

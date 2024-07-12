import curses
from math import log10
from dataclasses import dataclass
from random import randint
from sys import argv, exit

if __name__ == '__main__':
	@dataclass
	class pozition:
		index : int
		count : int = 0

		def __init__(self, index : int):
			self.index = index

	size : list[int] = [ 9, 9, 9, 1 ]
	map : list[list[int]]
	yt : list[int]; xt : list[int]
	yp : list[pozition]; xp : list[pozition]
	y : int; x : int; win : int
	game : bool; cheat : bool

	argb : list[bool] = [ False for _ in  range(0, 5) ]
	args : tuple[str] = (
		'Gamemory v1.5',
		'by A. S. Zaykov',
		'suck my dick'
	)

	stdscry : int; stdscrx : int
	leny : int; lenx : int
	stdscr : '_curses.window'
	window : '_curses.window'

	lennum : int = lambda x: int(log10(x)) + 1
	ypoz : int = lambda y: y + 1
	xpoz : int = lambda x: (x * (size[3] + 1)) + 2
	xbmp : int = lambda x: (x * (size[3] + 1)) + 1
	xemp : int = lambda x: (x * (size[3] + 1)) + size[3] + 2

	def error_args(string : str, exit_code : int):
		print ('Error ' + string)
		print (args[2])
		exit (exit_code)

	def generate():
		global map, yt, xt, yp, xp, y, x, win, game, cheat
		map = [ [ 0 for _ in range(0, size[1]) ] for _ in range(0, size[0]) ]
		yt = [ 0 for _ in range(0, size[2]) ]
		xt = [ 0 for _ in range(0, size[2]) ]
		yp = [ pozition(index) for index in range(0, size[0]) ]
		xp = [ pozition(index) for index in range(0, size[1]) ]

		index = 0
		while index < size[2]:
			y = randint(0, size[0] - 1)
			x = randint(0, size[1] - 1)
			if map[y][x] != 0: continue

			yt[index] = y
			xt[index] = x
			yp[y].count += 1
			xp[x].count += 1

			index += 1
			map[y][x] = index

		yp = list(filter(lambda dick: dick.count != 0, yp))
		xp = list(filter(lambda dick: dick.count != 0, xp))
		y = binarysearch(yp, yt[0])
		x = binarysearch(xp, xt[0])
		game = True; cheat = False
		win = 0

	def getmapsize():
		global size, leny, lenx, stdscry, stdscrx
		size[3] = lennum(size[2])
		leny = size[0] + 2
		lenx = (size[1] * (size[3] + 1)) + 3
		stdscry, stdscrx = stdscr.getmaxyx()

	def initmap():
		global window
		window = curses.newwin(size[0] + 2, (size[1] * (size[3] + 1)) + 3 , int(stdscry - leny) // 2,  int(stdscrx - lenx) // 2)
		window.border()

		for indexy in range(0, size[0]):
			for indexx in range(0, size[1]):
				if map[indexy][indexx] != 0:
					window.addstr(ypoz(indexy), xpoz(indexx), str(map[indexy][indexx]))
		window.refresh()


	def binarysearch(array : list[pozition], poz : int) -> int:
		begin : int = 0; end : int = len(array)
		while begin <= end:
			index : int = (begin + end) // 2
			if poz < array[index].index:
				end = index - 1
			elif poz > array[index].index:
				begin = index + 1
			else: return index
		return -1

	def outnumbers():
		global window
		for indexy in range(0, size[0]):
			for indexx in range(0, size[1]):
				if map[indexy][indexx] > 0:
					window.addstr(ypoz(indexy), xpoz(indexx), str(map[indexy][indexx]) + ' ' * (size[3] - lennum(map[indexy][indexx])))
		window.refresh()

	def hidenumbers():
		global window
		for indexy in range(0, size[0]):
			for indexx in range(0, size[1]):
				if map[indexy][indexx] > 0:
					window.addstr(ypoz(indexy), xpoz(indexx), '#' * size[3])
		window.refresh()

	def outmove():
		global window
		window.addstr(ypoz(yp[y].index), xbmp(xp[x].index), '>')
		window.addstr(ypoz(yp[y].index), xemp(xp[x].index), '<')
		window.refresh()

	def hidemove():
		global window
		window.addstr(ypoz(yp[y].index), xbmp(xp[x].index), ' ')
		window.addstr(ypoz(yp[y].index), xemp(xp[x].index), ' ')
		window.refresh()

	def isclearmap(y0 : int, y1 : int, x0 : int, x1 : int) -> bool:
		for indexy in range(y0, y1):
			for indexx in range(x0, x1):
				if map[yp[indexy].index][xp[indexx].index] != 0: return False
		return True

	def move(key : int):
		global window, x, y
		hidemove()

		match key:
			case 0: #up
				if y > 0:
					if len(xp) > 1 and isclearmap(0, y, x, x + 1):
						if x == 0: x += 1
						elif x == len(xp) - 1: x -= 1
						elif isclearmap(0, y, 0, x): x += 1
						elif isclearmap(0, y, x + 1, len(xp)): x -= 1
					y -= 1
				else: y = len(yp) - 1
			case 1:	#down
				if y < len(yp) - 1:
					y += 1
					if len(xp) > 1 and isclearmap(y, len(yp), x, x + 1):
						if x == 0: x += 1
						elif x == len(xp) - 1: x -= 1
						elif isclearmap(y, len(yp), 0, x): x += 1
						elif isclearmap(y, len(yp), x + 1, len(xp)): x -= 1
				else: y = 0
			case 2: #left
				if x > 0:
					if len(yp) > 1 and isclearmap(y, y + 1, 0, x):
						if y == 0: y += 1
						elif y == len(yp) - 1: y -= 1
						elif isclearmap(0, y, 0, x): y += 1
						elif isclearmap(y + 1, len(yp), 0, x): y -= 1
					x -= 1
				else: x = len(xp) - 1
			case 3:	#right
				if x < len(xp) - 1:
					x += 1
					if len(yp) > 1 and isclearmap(y, y + 1, x, len(xp)):
						if y == 0: y += 1
						elif y == len(yp) - 1: y -= 1
						elif isclearmap(0, y, x, len(xp)): y += 1
						elif isclearmap(y + 1, len(yp), x, len(xp)): y -= 1
				else: x = 0
		outmove()

	def keyenter():
		global xp, yp, y, x, win, window, map, game, cheat
		hidemove()
		if map[yp[y].index][xp[x].index] != 0:
			if map[yp[y].index][xp[x].index] == (win + 1):
				if win == (size[2]) - 1:
					game = False
					return
				if win == 0 and not cheat: hidenumbers()

				map[yp[y].index][xp[x].index] = 0
				window.addstr(ypoz(yp[y].index), xpoz(xp[x].index), '-' * size[3])
				win += 1

				if yp[y].count == 1:
					yp.pop(y)
					if y > 0: y -= 1
				else: yp[y].count -= 1

				if xp[x].count == 1:
					xp.pop(x)
					if x > 0: x -= 1
				else: xp[x].count -= 1
			else:
				game = False
				return
		outmove(); window.refresh()

	def gotoelement():
		hidemove()
		global y, x
		y = binarysearch(yp, yt[win])
		x = binarysearch(xp, xt[win])
		outmove()

	def mapcheat():
		global cheat
		if win != 0:
			if cheat: cheat = False; hidenumbers()
			else: cheat = True; outnumbers()

	def main():
		global stdscr, argb, window
		index = 1

		while index < len(argv):
			if argv[index][0] == '-':
				if argv[index][1] == '-':
					match argv[index][2:]:
						case 'version': argb[0] = True
						case 'about': argb[1] = True
						case 'help': argb[2] = True
						case _: error_args('No argument: ' + argv[index][2:], 101)
				else:
					for char in argv[index][1:]:
						match char:
							case 'v': argb[0] = True
							case 'a': argb[1] = True
							case 'h': argb[2] = True
							case _: error_args('No key: ' + char, 102)
			elif (len(argv) - 2) > 0:
				if argb[4]: error_args('reativated size', 105)
				for i in range(0, 3):
					integer = int(argv[index + i])
					if integer < 3: error_args('size < 3', 104)
					size[i] = integer

				if size[2] > (size[0] * size[1]): error_args('map numbers > x * y', 105)
				argb[4] = True; index += 2
			else: error_args('logic args', 103)
			index += 1

		for index in range(0, 3):
			if argb[index]:
				print (args[index])
				argb[3] = True

		if argb[3]: exit(0)
		stdscr = curses.initscr()
		curses.curs_set(False)
		curses.noecho()
		getmapsize()

		if leny > stdscry or lenx > stdscrx:
			curses.endwin()
			error_args('window size', 106)

		generate()
		initmap()
		outmove()

		while True:
			match window.getch():
				case 65: move(0)
				case 66: move(1)
				case 67: move(3)
				case 68: move(2)
				case 10: keyenter()
				case 103: gotoelement()
				case 104: mapcheat()
				case 113: break
			if win == 1 and not cheat: hidenumbers()
			if not game: break

	main(); curses.endwin()
	print (('you win' if win == (size[2] - 1) else f'you loser {win}') + f' in {size[2]}')
else: print('Ты чё блядь это надо запускать а не использовать как библиотеку')
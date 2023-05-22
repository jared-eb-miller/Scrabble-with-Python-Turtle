import turtle as trtl
import json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from random import choice
from pyautogui import size as window_size

SCREEN_WIDTH, SCREEN_HEIGHT = window_size()

# window dimentions and position
WIN_WIDTH = 800
WIN_HEIGHT = 800
WIN_STARTX = SCREEN_WIDTH/2 - WIN_WIDTH/2

# sizeing variables
HALF_TILE_SIDE_LEN = 23
BORDER_SIZE = (2/23) * HALF_TILE_SIDE_LEN

# colors
DEFAULT_COLOR = (200, 190, 160)
DOUBLE_WORD_COLOR = (250, 175, 155)
TRIPLE_WORD_COLOR = (255, 90, 70)
DOUBLE_LETTER_COLOR = (185, 215, 215)
TRIPLE_LETTER_COLOR = (10, 155, 190)

# tuples of indices of tiles in the 'board' list
DOUBLE_WORD_TILES = (16, 28, 32, 42, 48, 56, 64, 70, \
		154, 160, 168, 176, 182, 192, 196, 208)
TRIPLE_WORD_TILES = (0, 7, 14, 105, 119, 210, 217, 224)
DOUBLE_LETTER_TILES = (3, 11, 36, 38, 45, 52, 59, 92, \
		96, 98, 102, 108, 116, 122, 126, 128, 132, \
		165, 172, 179, 186, 188, 213, 221)
TRIPLE_LETTER_TILES = (20, 24, 76, 80, 84, 88, 136, \
		140, 144, 148, 200, 204)

SHAPE_SIDE_LEN = HALF_TILE_SIDE_LEN - BORDER_SIZE
TILE_SHAPE = ((SHAPE_SIDE_LEN, SHAPE_SIDE_LEN), 
		(-SHAPE_SIDE_LEN, SHAPE_SIDE_LEN), 
		(-SHAPE_SIDE_LEN, -SHAPE_SIDE_LEN), 
		(SHAPE_SIDE_LEN, -SHAPE_SIDE_LEN))

def star_shape(half_tile_side_len):	# makes a 5-pointed star to give to wn.register_shape()
	from math import sin, cos, pi

	SCALE = 0.9
	TRANSLATE_DOWN = (half_tile_side_len/23) * 2
	OUTER_RAD = half_tile_side_len * SCALE
	INNER_RAD = (half_tile_side_len / 2.66) * SCALE
	INCREMENT_ANGLE = pi/5

	points = []
	angle = 0
	for p in range(5):
		x = (INNER_RAD * cos(angle)) + TRANSLATE_DOWN
		y = INNER_RAD * sin(angle)
		points.append((x,y))
		angle += INCREMENT_ANGLE
		x = (OUTER_RAD * cos(angle)) + TRANSLATE_DOWN
		y = OUTER_RAD * sin(angle)
		points.append((x,y))
		angle += INCREMENT_ANGLE

	return tuple(points)

wn = trtl.Screen()
wn.setup(width=WIN_WIDTH, height=WIN_HEIGHT, startx=WIN_STARTX, starty=0)
wn.title('Scrabble')
wn.register_shape('tile', TILE_SHAPE)
wn.register_shape('star', star_shape(HALF_TILE_SIDE_LEN))
for f in os.popen('ls imgs').read().split('\n')[:-1]:
	wn.addshape('imgs/' + f)
wn.colormode(255)

	
def make_special_shape(shape):	# creates 
	
	def tupleize(_data):
		list_of_tuples = []
		if isinstance(_data, list):
			for e in _data:
				list_of_tuples.append(tupleize(e))
			return tuple(list_of_tuples)
		else:
			return _data

	shift = BORDER_SIZE*2

	class Shape():
		def __init__(self):
			self._data = []
		def addcomponent(self, shape):
			self._data.append([shape, None, None])

	triangle_shape = [[-BORDER_SIZE, 0,], [0, BORDER_SIZE*2], [BORDER_SIZE, 0]]

	if shape == 'double':

		tile_compound = Shape()
		tile_compound.addcomponent(TILE_SHAPE)
		wn._shapes['double tile'] = tile_compound
		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] += SHAPE_SIDE_LEN
			i += 1
		i = 0
		for point in triangle_shape:
			triangle_shape[i][0] += shift
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] *= -1
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][0] -= shift*2
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] *= -1
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))

		i = 0
		for point in triangle_shape:	# rotate 90 degrees
			cache = triangle_shape[i][0]
			triangle_shape[i][0] = triangle_shape[i][1]
			triangle_shape[i][1] = cache
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))

		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] += shift*2
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][0] *= -1
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] -= shift*2
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		
	elif shape == 'triple':

		tile_compound = Shape()
		tile_compound.addcomponent(TILE_SHAPE)
		wn._shapes['triple tile'] = tile_compound
		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] += SHAPE_SIDE_LEN
			i += 1
		i = 0
		for point in triangle_shape:
			triangle_shape[i][0] += shift*2
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][1] *= -1
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))
		for x in range(2):
			i = 0
			for point in triangle_shape:
				triangle_shape[i][0] -= shift*2
				i += 1
			tile_compound.addcomponent(tupleize(triangle_shape))
			i = 0
			for point in triangle_shape:
				triangle_shape[i][1] *= -1
				i += 1
			tile_compound.addcomponent(tupleize(triangle_shape))\

		i = 0
		for point in triangle_shape:	# rotate 90 degrees
			cache = triangle_shape[i][0]
			triangle_shape[i][0] = triangle_shape[i][1]
			triangle_shape[i][1] = cache
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))

		for x in range(2):
			i = 0
			for point in triangle_shape:
				triangle_shape[i][0] *= -1
				i += 1
			tile_compound.addcomponent(tupleize(triangle_shape))
			i = 0
			for point in triangle_shape:
				triangle_shape[i][1] += shift*2
				i += 1
			tile_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for point in triangle_shape:
			triangle_shape[i][0] *= -1
			i += 1
		tile_compound.addcomponent(tupleize(triangle_shape))

	else:
		raise Exception('Invalid Input')

	return tile_compound._data

def format_shape_data(_type):

	DOUBLE_DATA = make_special_shape('double')

	TRIPLE_DATA = make_special_shape('triple')

	if _type[0] == 'd':
		default_data = DOUBLE_DATA
		print('double')
		if _type[1] == 'l':
			COLOR = DOUBLE_LETTER_COLOR
			print('letter')
		else:
			COLOR = DOUBLE_WORD_COLOR
			print('word')
	else:
		default_data = TRIPLE_DATA
		print('triple')
		if _type[1] == 'l':
			COLOR = TRIPLE_LETTER_COLOR
			print('letter')
		else:
			COLOR = TRIPLE_WORD_COLOR
			print('word')
	i = 0
	for component in default_data:
		default_data[i][1] = COLOR
		default_data[i][2] = COLOR
		i += 1

	return default_data

wn._shapes['double letter tile'] = trtl.Shape('compound')
wn._shapes['double letter tile']._data = format_shape_data('dl')
wn._shapes['double word tile'] = trtl.Shape('compound')
wn._shapes['double word tile']._data = format_shape_data('dw')
wn._shapes['triple letter tile'] = trtl.Shape('compound')
wn._shapes['triple letter tile']._data = format_shape_data('tl')
wn._shapes['triple word tile'] = trtl.Shape('compound')
wn._shapes['triple word tile']._data = format_shape_data('tw')

# create game board
board = [None]*225

wn.tracer(False)

STARTING_XCOR = -(HALF_TILE_SIDE_LEN*14)
xcor = STARTING_XCOR
ycor = HALF_TILE_SIDE_LEN*14
for tile in board:
	tile = trtl.Turtle()
	board[board.index(None)] = tile
	tile.penup()
	tile.goto(xcor, ycor)

	# set special tiles their repective colors
	if board.index(tile) in DOUBLE_LETTER_TILES:
		tile.shape('double letter tile')
	elif board.index(tile) in DOUBLE_WORD_TILES:
		tile.shape('double word tile')
	elif board.index(tile) in TRIPLE_LETTER_TILES:
		tile.shape('triple letter tile')
	elif board.index(tile) in TRIPLE_WORD_TILES:
		tile.shape('triple word tile')
	else:
		tile.color(DEFAULT_COLOR)
		tile.shape('tile')

	# change position for the next tile
	xcor += HALF_TILE_SIDE_LEN*2
	if xcor > -STARTING_XCOR:
		xcor = STARTING_XCOR
		ycor -= HALF_TILE_SIDE_LEN*2

# format the center tile
board[112].color(DOUBLE_WORD_COLOR)
trtl.Turtle(shape='star')

# draw border
_pensize = BORDER_SIZE*3
border_pen = trtl.Turtle(shape='blank')
border_pen.pensize(_pensize)
xcor = HALF_TILE_SIDE_LEN*15 + BORDER_SIZE + _pensize/2
ycor = HALF_TILE_SIDE_LEN*15 + BORDER_SIZE + _pensize/2
border_pen.penup()
border_pen.goto(xcor, ycor)
border_pen.pendown()
border_pen.goto(-xcor, ycor)
border_pen.goto(-xcor, -ycor)
border_pen.goto(xcor, -ycor)
border_pen.goto(xcor, ycor)

wn.tracer(True)
wn.update()

wn.mainloop()

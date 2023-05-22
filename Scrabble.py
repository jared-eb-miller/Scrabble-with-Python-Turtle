import turtle as trtl
import json, os

os.chdir(os.path.dirname(os.path.abspath(__file__))) # set working directory

from random import randint
from pyautogui import size as window_size


# window dimentions and position
SCREEN_WIDTH, SCREEN_HEIGHT = window_size()
WIN_WIDTH = 1000
WIN_HEIGHT = 800
WIN_STARTX = SCREEN_WIDTH/2 - WIN_WIDTH/2

# sizing variables
HALF_TILE_SIDE_LEN = 23
BORDER_SIZE = (2/23) * HALF_TILE_SIDE_LEN

# colors
DEFAULT_COLOR = (200, 190, 160)
DOUBLE_WORD_COLOR = (250, 175, 155)
TRIPLE_WORD_COLOR = (255, 90, 70)
DOUBLE_LETTER_COLOR = (165, 200, 215)
TRIPLE_LETTER_COLOR = (10, 155, 190)

# geometry of tiles in the 'board' list
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

NUM_PLAYERS = 2

with open('tile_data.json', 'r') as f:
	TILE_DATA_DIC = json.load(f)

with open('scrabble_dic.txt', 'r') as f:
	DICTIONARY = f.read().split('\n')

def star_shape(half_tile_side_len):	# makes a 5-pointed star to give to wn.register_shape()
	from math import sin, cos, pi

	SCALE = 0.9
	TRANSLATE_DOWN = (half_tile_side_len/23) * 2
	OUTER_RAD = half_tile_side_len * SCALE
	INNER_RAD = (half_tile_side_len / 2.66) * SCALE
	INCREMENT_ANGLE = pi/5

	points = []
	angle = 0
	for _ in range(5):
		x = (INNER_RAD * cos(angle)) + TRANSLATE_DOWN
		y = INNER_RAD * sin(angle)
		points.append((x,y))
		angle += INCREMENT_ANGLE
		x = (OUTER_RAD * cos(angle)) + TRANSLATE_DOWN
		y = OUTER_RAD * sin(angle)
		points.append((x,y))
		angle += INCREMENT_ANGLE

	return tuple(points)

def format_shape_data(_type):

	def make_special_shapes():
		'''
		Returns both the double shape (the shape for 
		double word and double letter tiles) and the 
		triple shape (the shape for triple word and 
		triple letter tiles) scaled for SHAPE_SIDE_LEN 
		and BORDER_SIZE
		'''
		def tupleize(_data):
			'''
			Changes the changing list variables to tuples
			to be accepted as the shape element of components
			of Turtle compound shapes
			'''
			list_of_tuples = []
			if isinstance(_data, list):
				for e in _data:
					list_of_tuples.append(tupleize(e))
				return tuple(list_of_tuples)
			else:
				return _data

		class Shape():
			def __init__(self):
				self._data = []
			def addcomponent(self, shape):
				self._data.append([shape, None, None])
				# 'None' elements will be used to specify 
				# the color of the larger shape later

		shift = BORDER_SIZE*2
		triangle_shape = [[-BORDER_SIZE, 0,], [0, BORDER_SIZE*2], [BORDER_SIZE, 0]]

		# Double shape
		double_compound = Shape()
		double_compound.addcomponent(TILE_SHAPE)
		wn._shapes['double tile'] = double_compound
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] += SHAPE_SIDE_LEN
			i += 1
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][0] += shift
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] *= -1
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][0] -= shift*2
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] *= -1
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))

		i = 0
		for _ in triangle_shape:	# rotate 90 degrees
			cache = triangle_shape[i][0]
			triangle_shape[i][0] = triangle_shape[i][1]
			triangle_shape[i][1] = cache
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))

		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] += shift*2
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][0] *= -1
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] -= shift*2
			i += 1
		double_compound.addcomponent(tupleize(triangle_shape))
			
		# Triple shape
		triangle_shape = [[-BORDER_SIZE, 0,], [0, BORDER_SIZE*2], [BORDER_SIZE, 0]]
		triple_compound = Shape()
		triple_compound.addcomponent(TILE_SHAPE)
		wn._shapes['triple tile'] = triple_compound
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] += SHAPE_SIDE_LEN
			i += 1
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][0] += shift*2
			i += 1
		triple_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][1] *= -1
			i += 1
		triple_compound.addcomponent(tupleize(triangle_shape))
		for _ in range(2):
			i = 0
			for _ in triangle_shape:
				triangle_shape[i][0] -= shift*2
				i += 1
			triple_compound.addcomponent(tupleize(triangle_shape))
			i = 0
			for _ in triangle_shape:
				triangle_shape[i][1] *= -1
				i += 1
			triple_compound.addcomponent(tupleize(triangle_shape))

		i = 0
		for _ in triangle_shape:	# rotate 90 degrees
			cache = triangle_shape[i][0]
			triangle_shape[i][0] = triangle_shape[i][1]
			triangle_shape[i][1] = cache
			i += 1
		triple_compound.addcomponent(tupleize(triangle_shape))

		for _ in range(2):
			i = 0
			for _ in triangle_shape:
				triangle_shape[i][0] *= -1
				i += 1
			triple_compound.addcomponent(tupleize(triangle_shape))
			i = 0
			for _ in triangle_shape:
				triangle_shape[i][1] += shift*2
				i += 1
			triple_compound.addcomponent(tupleize(triangle_shape))
		i = 0
		for _ in triangle_shape:
			triangle_shape[i][0] *= -1
			i += 1
		triple_compound.addcomponent(tupleize(triangle_shape))

		return (double_compound._data, triple_compound._data)

	# initial values
	DOUBLE_DATA, TRIPLE_DATA = make_special_shapes()

	# decide what to change to
	if _type[0] == 'd':
		default_data = DOUBLE_DATA
		if _type[1] == 'l':
			COLOR = DOUBLE_LETTER_COLOR
		else:
			COLOR = DOUBLE_WORD_COLOR
	else:
		default_data = TRIPLE_DATA
		if _type[1] == 'l':
			COLOR = TRIPLE_LETTER_COLOR
		else:
			COLOR = TRIPLE_WORD_COLOR
	# change the 'fill' and 'outline' elements for each component
	i = 0
	for _ in default_data:
		default_data[i][1] = COLOR
		default_data[i][2] = COLOR
		i += 1

	return default_data

def outline_tiles(tile_shape): # shrink tile so that they have the white back ground as their border.
	shape = list(tile_shape)
	new_points = []
	STRETCH_FACTOR = 0.89
	for point in shape:
		new_points.append((point[0] * STRETCH_FACTOR, 
			point[1] * STRETCH_FACTOR))
	return tuple(shape + new_points)

# gneral settings
wn = trtl.Screen()
wn.setup(width=WIN_WIDTH, height=WIN_HEIGHT, startx=WIN_STARTX, starty=0) # centered left-to-right and at the top of the screen top-to-bottom.
wn.title('Scrabble')
wn.tracer(False)
wn.colormode(255)

# shape settings
wn.register_shape('tile', TILE_SHAPE)
wn.register_shape('outline', outline_tiles(TILE_SHAPE))
# tile images were taken from https://github.com/anthony-chang/Scrabble/tiles
# images are stored in the 'imgs/' subfolder
os.chdir('imgs')
for t in TILE_DATA_DIC.keys():
	wn.addshape(TILE_DATA_DIC[t]['img_path'])
wn.addshape('blank.gif')
wn.addshape('discard.gif')
wn.addshape('reset.gif')
wn.addshape('submit.gif')
wn._shapes['double letter tile'] = trtl.Shape('compound')
wn._shapes['double letter tile']._data = format_shape_data('dl')
wn._shapes['double word tile'] = trtl.Shape('compound')
wn._shapes['double word tile']._data = format_shape_data('dw')
wn._shapes['triple letter tile'] = trtl.Shape('compound')
wn._shapes['triple letter tile']._data = format_shape_data('tl')
wn._shapes['triple word tile'] = trtl.Shape('compound')
wn._shapes['triple word tile']._data = format_shape_data('tw')
wn._shapes['center tile'] = trtl.Shape('compound')
wn._shapes['center tile']._data = wn._shapes['double word tile']._data + \
	[[star_shape(HALF_TILE_SIDE_LEN), 'black', 'black']]

# font settings
PREMIUM_TEXT_STYLING = ('Eurostile', 8, 'normal')
premium_text = trtl.Turtle(shape='blank')
premium_text.penup()
premium_text.setheading(90)

def write_premium_text(tile, text):
	tile.stamp()
	premium_text.goto(tile.xcor()+1.5, tile.ycor())
	premium_text.forward(5)
	for word in text:
		premium_text.write(word, font=PREMIUM_TEXT_STYLING, align='center')
		premium_text.back(11)

# create game board
board = [None]*225 # 15 x 15 board

STARTING_XCOR = -(HALF_TILE_SIDE_LEN*14)
xcor = STARTING_XCOR
ycor = HALF_TILE_SIDE_LEN*14
for i, tile in enumerate(board):
	tile = trtl.Turtle()
	board[i] = tile
	tile.penup()
	tile.goto(xcor, ycor)

	# set special tiles to their repective shapes
	if board.index(tile) in DOUBLE_LETTER_TILES:
		tile.shape('double letter tile')
		write_premium_text(tile, ('DOUBLE','LETTER','SCORE'))
	elif board.index(tile) in DOUBLE_WORD_TILES:
		tile.shape('double word tile')
		write_premium_text(tile, ('DOUBLE','WORD','SCORE'))
	elif board.index(tile) in TRIPLE_LETTER_TILES:
		tile.shape('triple letter tile')
		write_premium_text(tile, ('TRIPLE','LETTER','SCORE'))
	elif board.index(tile) in TRIPLE_WORD_TILES:
		tile.shape('triple word tile')
		write_premium_text(tile, ('TRIPLE','WORD','SCORE'))
	else:
		tile.color(DEFAULT_COLOR)
		tile.shape('tile')
		tile.stamp()

	tile.hideturtle()
  
	# change position for the next tile
	xcor += HALF_TILE_SIDE_LEN*2
	if xcor > -STARTING_XCOR: # move to the start of the next row.
		xcor = STARTING_XCOR
		ycor -= HALF_TILE_SIDE_LEN*2

# format the center tile
center_tile = board[112]
center_tile.shape('center tile')
center_tile.stamp()

# draw border
border_pen = trtl.Turtle(shape='blank')
border_pen.pensize(BORDER_SIZE*3)
xcor = HALF_TILE_SIDE_LEN*15 + BORDER_SIZE*5/2
ycor = xcor
border_pen.penup()
border_pen.goto(xcor, ycor)
border_pen.pendown()
border_pen.goto(-xcor, ycor)
border_pen.goto(-xcor, -ycor)
border_pen.goto(xcor, -ycor)
border_pen.goto(xcor, ycor)
del border_pen

def update(func):
	"""
	This function will decorate functions that 
	make changes to the screen that need to be 
	shown - it updates the screen.
	"""
	def wrapper(*args, **kwargs):
		value = func(*args, **kwargs)
		wn.update()
		return value
	return wrapper

class Gamepiece(trtl.Turtle):
	"""
	Gamepiece objects will be turtle objects 
	with a few extra attributes.
	"""
	def __init__(self, letter, letter_data):
		# attributes
		self.letter = letter
		self.value = letter_data['value']
		self.value_multiplier = 1
		self.board_index = None

		# turtle settings
		trtl.Turtle.__init__(self)
		self.shape(letter_data['img_path'])
		self.hideturtle()
		self.penup()

		self.highlighter = trtl.Turtle(shape='outline')
		self.highlighter.color('black')
		self.highlighter.penup()
		self.highlighter.hideturtle()

	def highlight(self):
		self.highlighter.goto(self.position())
		self.highlighter.stamp()

	def clear_highlight(self):
		self.highlighter.clear()
		Player.selected_tile = None

	def __repr__(self): # for debugging
		if self.board_index: # peice is on the board
			return f"'{self.letter.capitalize()}' at {self.board_index}"
		else: # peice is in the player's hand
			return f"'{self.letter.capitalize()}' in hand"

# fill bag with the correct ammount of peices
# this game does not inclue the 2 blank tiles
bag = []
for letter in TILE_DATA_DIC:
	for tile in range(TILE_DATA_DIC[letter]['count']):
		_tile = Gamepiece(letter, TILE_DATA_DIC[letter])
		bag.append(_tile)

class Player:
	HAND_SIZE = 7
	HAND_POSITION = 415
	TOP_Y_POS = SHAPE_SIDE_LEN*6
	BUTTON_POS = SHAPE_SIDE_LEN*10
	players = []
	selected_tile = None

	hand_highlighter = trtl.Turtle(shape='blank')
	hand_highlighter.color('black')
	hand_highlighter.pensize(5)
	hand_highlighter.penup()

	played_tiles = []

	def __init__(self):

		Player.players.append(self)

		self.score = 0
		self.hand = []

		self.player_num = len(Player.players)
		self.XCOR = -self.HAND_POSITION \
			if (self.player_num % 2) == 1 else self.HAND_POSITION

		self.submit_button = trtl.Turtle()
		self.submit_button.color(DEFAULT_COLOR)
		self.submit_button.hideturtle()
		self.submit_button.penup()

		self.reset_button = self.submit_button.clone()
		self.discard_button = self.submit_button.clone()

		self.submit_button.goto(self.XCOR*1.03, -self.BUTTON_POS)
		self.reset_button.goto(self.submit_button.xcor(), self.BUTTON_POS)
		self.discard_button.goto(self.submit_button.xcor()-2, # for some reason the images aren't perfectly centered
			self.submit_button.ycor() - HALF_TILE_SIDE_LEN*5)
		self.submit_button.shape('submit.gif')
		self.reset_button.shape('reset.gif')
		self.discard_button.shape('discard.gif')

		t_score_keeper = trtl.Turtle(shape='blank') 
		t_score_keeper.penup()
		t_score_keeper.goto(self.XCOR*1.03, self.TOP_Y_POS*2.7)
		
		self.score_keeper = t_score_keeper.clone()
		self.score_keeper.goto(self.XCOR*1.03, self.TOP_Y_POS*2.4)
		self.score_keeper.write(
			f'{self.score}', 
			font=('Eurostile', 30, 'bold'), 
			align="center"
			)

		t_score_keeper.write(
			'Score:', 
			font=('Eurostile', 30, 'bold', 'underline'), 
			align="center"
			)
		del t_score_keeper

	def fill_hand(self):
		ycor = self.TOP_Y_POS

		while len(self.hand) < self.HAND_SIZE:
			for tile in self.hand:
				if tile.ycor() == ycor:
					ycor -= SHAPE_SIDE_LEN*2
			try:
				new_tile = bag.pop(randint(0, len(bag)-1))
			except (IndexError, ValueError):
				break # the bag is empty
			new_tile.goto(self.XCOR, ycor)
			new_tile.showturtle()
			self.hand.append(new_tile)
			self.hand.sort(key=lambda Gamepiece: Gamepiece.ycor(), reverse=True)  # keep self.hand in visually decending order

	@update
	def start_turn(self):
		wn.onclick(self.pick_tile)
		self.moved_tiles = []
		self.outline_hand()

		if len(bag) > 0:	
			self.discard_button.showturtle()
			self.discard_button.onclick(self.discard_tiles)

	@update
	def reset_turn(self, *args, tile=None):
		ycor = self.TOP_Y_POS
		if not tile:
			tiles = self.moved_tiles
		else:
			tiles = [tile]
		for tile in tiles:
			for _tile in self.hand:
				if _tile.ycor() == ycor:
					_tile.clear_highlight()
					ycor -= SHAPE_SIDE_LEN*2		
			tile.goto(self.XCOR, ycor)
			tile.clear_highlight()
			tile.board_index = None
			self.hand.append(tile)
			self.hand.sort(key=lambda Gamepiece: Gamepiece.ycor(), reverse=True) # keep self.hand in visually decending order
			self.moved_tiles[self.moved_tiles.index(tile)] = None

		self.moved_tiles =  list(filter(lambda a: a != None, self.moved_tiles))

	def submit_turn(self, *args):
		moved_board_indecies = [t.board_index for t in self.moved_tiles]

		class Word():
			words = []
			def __init__(self):
				self.word = ''
				self.tiles = []
				self.score = 0
				self.score_multiplier = 1
				self.words.append(self)

			def __repr__(self):
				return self.word[0].capitalize() + self.word[1:]

			def delete(self):
				self.words.remove(self)
				del self

		# --- Validate Turn Placement ---

		if len(self.played_tiles) == 0: # first turn
			if not 112 in moved_board_indecies: # one of the tiles not is on the center tile
				print('INVALID: first turn must be played on the center tile')
				return

		if len(self.moved_tiles) == 1:
			# the first tile to be played in a turn
			board_index = self.moved_tiles[0].board_index
			valid = False
			for t in self.played_tiles:
				# to the right or left of other tiles
				if board_index == t.board_index+1:
					if board_index % 15 != 0:
						increment = 1
						valid = True
						break
				if board_index == t.board_index-1:
					if board_index % 15 != 14:
						increment = 1
						valid = True
						break
				# above or below other tiles
				if board_index == t.board_index+15:
					increment = 15
					valid = True
					break
				if board_index == t.board_index-15:
					increment = 15
					valid = True
					break
			if not valid:
				print('INVALID: word must be played off of other tiles')
				return
		else:
			# all tiles played must be on the same row or column
			column_sum = 0
			row_sum = 0
			for t in self.moved_tiles:
				t.column = t.board_index % 15
				t.row = int(t.board_index / 15)
				column_sum += t.column
				row_sum += t.row
			# same row
			if row_sum == len(self.moved_tiles) * self.moved_tiles[0].row:
				increment = 1
			# same column
			elif column_sum == len(self.moved_tiles) * self.moved_tiles[0].column:
				increment = 15
			# neither - invalid
			else:
				print('INVALID: must be in the same row or column')
				return

		# --- Get Main Word ---

		# order the moved tiles by board index
		self.moved_tiles.sort(key=lambda Gamepiece: Gamepiece.board_index)

		main_word = Word()
		# add all moved ties to incorporated tiles
		main_word.tiles += self.moved_tiles

		index = int(self.moved_tiles[0].board_index) # move to the start of the word
		while not self.is_open(index-increment):
			index -= increment
			if (index%15)**2 + increment == 197:  # avoid going back to the end of the last line
				# (15th column (index % 15 == 14) and an increment of 1)
				break
			for tile in self.played_tiles:
				if tile.board_index == index:
					break
			main_word.tiles.append(tile)
			main_word.word = tile.letter + main_word.word
		
		moved_index = 0
		index = int(self.moved_tiles[0].board_index) # move through the rest of the tiles in the word
		while not self.is_open(index):
			if index in moved_board_indecies:
				main_word.word += self.moved_tiles[moved_index].letter
				moved_index += 1
			else:
				if (index%15) + increment == 1:  # avoid going to the begining of the next line
					# (1st column (index % 15 == 0) and an increment of 1)
					break
				for tile in self.played_tiles:
					if tile.board_index == index:
						main_word.word += tile.letter
						main_word.tiles.append(tile)
						break
			index += increment

		# --- Get Other Words ---

		# flip increment value for to the value of its perpindicular orientation
		# increment is either 1 or 15
		increment = ((increment%15)*14)+1

		for tile in self.moved_tiles:
			word = Word()
			word.word += tile.letter
			word.tiles.append(tile)

			index = tile.board_index + increment
			while not self.is_open(index):
				if (index%15) + increment == 1:  # avoid going to the begining of the next line
					# (1st column (index % 15 == 0) and an increment of 1)
					break
				for _tile in self.played_tiles:
					if _tile.board_index == index:
						word.word += _tile.letter
						word.tiles.append(_tile)
						break
				index += increment

			index = tile.board_index - increment

			while not self.is_open(index):
				if ((index%15)*increment) + increment == 15:  # avoid going back to the end of the las line
					# (15th column (index % 15 == 14) and an increment of 1)
					break
				for _tile in self.played_tiles:
					if _tile.board_index == index:
						break
				word.tiles.append(_tile)
				word.word = _tile.letter + word.word

				index -= increment

			if len(word.word) < 2:
				word.delete()

		# --- Check Words ---

		for word in Word.words:
			valid = False
			for _word in DICTIONARY:
				if word.word == _word:
					valid = True
					break
			if not valid:
				print(f"INVALID: '{word}' ({[tile for tile in word.tiles]}) is not a valid scrabble word")
				return

		# --- Score ---
		turn_score = 0
		for word in Word.words:
			for tile in word.tiles:
				if tile in self.moved_tiles:
					if tile.board_index in DOUBLE_LETTER_TILES:
						tile.value_multiplier *= 2
					elif tile.board_index in DOUBLE_WORD_TILES:
						word.score_multiplier *= 2
					elif tile.board_index in TRIPLE_LETTER_TILES:
						tile.value_multiplier *= 3
					elif tile.board_index in TRIPLE_WORD_TILES:
						word.score_multiplier *= 3

					word.score += int(tile.value * tile.value_multiplier)
					tile.value_multiplier = 1
				else:
					word.score += tile.value
			turn_score += word.score * word.score_multiplier
		
		if len(self.moved_tiles) == 7:
			turn_score += 50

		self.score += turn_score

		# display score
		self.score_keeper.clear()
		self.score_keeper.write(
			f'{self.score}', 
			font=('Eurostile', 30, 'bold'), 
			align="center"
			)

		# console log
		print(f'Player {self.player_num}:')
		for word in Word.words:
			print(f'''\tWord '{word}':
		Tiles:	{word.tiles}
		Score:	{word.score*word.score_multiplier}''')
		print(f'\tScore:\t{self.score}\n')

		# --- Change Turn ---

		# at this point the turn is valid and needs to be finished

		self.played_tiles += self.moved_tiles
		self.change_turn()

	@update
	def discard_tiles(self, *args):
		wn.onclick(None)

		self.reset_turn()
		try:
			Player.selected_tile.clear_highlight()
		except AttributeError:
			pass # no tile was selected — this will happen most of the time.
		self.reset_button.showturtle()
		self.discard_button.hideturtle()

		selected_tiles = []

		@update
		def select_tile(tile):
			if tile not in selected_tiles:
				tile.highlight()
				selected_tiles.append(tile)
				self.hand.remove(tile)
			else:
				tile.clear_highlight()
				self.hand.append(tile)
				selected_tiles.remove(tile)
			if len(selected_tiles) == 1:
				self.submit_button.showturtle()
				self.submit_button.onclick(lambda x,y, self=self, 
					selected_tiles=selected_tiles: 
					func(True, self, selected_tiles))
			elif len(selected_tiles) == 0:
				self.submit_button.hideturtle()
				self.submit_button.onclick(None)

		for tile in self.hand:
			tile.onclick(lambda x,y, tile=tile: select_tile(tile))

		def func(to_submit, self, selected_tiles):
			for tile in self.hand + selected_tiles:
				tile.onclick(None)
			for tile in selected_tiles:
				tile.clear_highlight()
			if to_submit:
				for tile in selected_tiles:
					tile.hideturtle()
				self.change_turn()
			else:
				self.hand += selected_tiles
				self.activate_buttons()
				self.reset_turn()
				self.start_turn()

		self.reset_button.onclick(lambda x,y, self=self, 
			selected_tiles=selected_tiles: func(False, self, selected_tiles))

	def activate_buttons(self):
		for btn, func in [
			(self.submit_button, self.submit_turn),
			(self.reset_button, self.reset_turn)
			]:
			btn.showturtle()
			btn.onclick(func)

	def deactivate_buttons(self):
		for btn in [
			self.submit_button,
			self.reset_button,
			self.discard_button
			]:
			btn.hideturtle()
			btn.onclick(None)

	@update
	def pick_tile(self, x, y):

		for tile in self.hand + self.moved_tiles:
			if (
				y < tile.ycor() + 20
				and y > tile.ycor() - 20
				and x < tile.xcor() + 20
				and x > tile.xcor() - 20
				):
				if Player.selected_tile != tile:
					if Player.selected_tile:
						Player.selected_tile.clear_highlight()
					Player.selected_tile = tile
					tile.highlight()
				else:
					tile.clear_highlight()
				return

		if Player.selected_tile:
			if abs(x) < HALF_TILE_SIDE_LEN*15:
				for tile in board:
					if (
						y < tile.ycor() + HALF_TILE_SIDE_LEN
						and y > tile.ycor() - HALF_TILE_SIDE_LEN
						and x < tile.xcor() + HALF_TILE_SIDE_LEN
						and x > tile.xcor() - HALF_TILE_SIDE_LEN
						and self.is_open(board.index(tile))
						):
						Player.selected_tile.board_index = board.index(tile)
						Player.selected_tile.goto(tile.position())
						if len(self.moved_tiles) == 0:
							# activate buttons if they have not been already
							self.activate_buttons()
						try:
							self.hand.remove(self.selected_tile)
							self.moved_tiles.append(self.selected_tile)
						except ValueError:
							pass # if selected_tile is already out of self.hand and in self.moved_tiles
			else:
				if (
					x * (abs(x)/x) > HALF_TILE_SIDE_LEN*15 
					and Player.selected_tile in self.moved_tiles
					): # put one tile back in the player's hand
					self.reset_turn(tile=Player.selected_tile)
		try:
			Player.selected_tile.clear_highlight()
		except AttributeError:
			pass # Player.selected_tile was already cleared
	
	def is_open(self, _board_index):
		'''
		Returns true if the selected board tile is ocupied
		'''
		indecies = [t.board_index for t in self.moved_tiles] + \
					[t.board_index for t in self.played_tiles]
		for i in indecies:
			if i == _board_index:
				# already ocupied
				return False
		return True

	def outline_hand(self):

		h_height = self.TOP_Y_POS*1.21
		h_width = self.XCOR*0.06

		self.hand_highlighter.clear()
		self.hand_highlighter.goto(self.XCOR+h_width, h_height) # start at outside top
		self.hand_highlighter.pendown()
		# - draw -
		self.hand_highlighter.goto(self.XCOR+h_width, -h_height) # outside bottom
		self.hand_highlighter.goto(self.XCOR-h_width, -h_height) # inside bottom
		self.hand_highlighter.goto(self.XCOR-h_width, h_height) # inside top
		self.hand_highlighter.goto(self.XCOR+h_width, h_height) # outside top

		self.hand_highlighter.penup()

	def change_turn(self):
		self.deactivate_buttons()
		self.fill_hand()
		self.players[abs(self.player_num-2)].start_turn()

	def start_game():
		while len(Player.players) < NUM_PLAYERS:
			Player().fill_hand()
		Player.players[0].start_turn()

Player.start_game()

wn.mainloop()

# setup_tiles.py
import json

tiles = {}

_tile = {
	'value': None
}

print('---To quit, type DONE---')
tile_name = input('New tile: ')
	
while tile_name != 'DONE':

	tile = _tile.copy()

	tile['value'] = int(input('\tValue: '))

	tile.update({'img_path': 'imgs/' + tile_name + '.png'})

	tiles.update({tile_name.lower(): tile})
	# next tile
	tile_name = input('New tile: ')


FILE_NAME = 'tile_data.json'
with open(FILE_NAME, 'r') as json_read_file:
	try:
		contents = json.load(json_read_file)
		tiles.update(contents)
	except:
		print('Error')
	with open(FILE_NAME, 'w') as json_write_file:
		json.dump(tiles, json_write_file)

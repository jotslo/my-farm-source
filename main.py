import consts

# move drone back to 0, 0
def reset_drone():
	x, y = get_pos_x(), get_pos_y()

	while x > 0:
		move(West)
		x -= 1
	
	while y > 0:
		move(South)
		y -= 1


# plant the expected entity at the current position
def plant_entity():
	x, y = get_pos_x(), get_pos_y()
	expected_entity = consts.ENTITY_MAP[x][y]

	if get_entity_type() == expected_entity:
		return

	valid_grounds = consts.GROUND_MAP[expected_entity]

	if get_ground_type() not in valid_grounds:
		till()
	
	plant(expected_entity)


# attempt to harvest the entity under the drone
def try_harvest():
	if can_harvest():
		harvest()


# water the ground if it is too dry
def try_water():
	if get_water() < 0.8:
		use_item(Items.Water)


# iterate through every block in the farm
def scan_farm():
	world_size = get_world_size()

	for x in range(world_size):
		for y in range(world_size):
			try_water()
			try_harvest()
			plant_entity()
			try_harvest()

			move(North)
		move(East)


reset_drone()

while True:
	scan_farm()
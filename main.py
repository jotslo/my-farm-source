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
	if get_water() < 0.5:
		use_item(Items.Water)


# return true if pumpkin is ready for harvesting. if not, replant it
def is_pumpkin_ready():

	if get_entity_type() == Entities.Pumpkin and can_harvest():
		return True
	elif get_entity_type() != Entities.Pumpkin:
		plant_entity()
		return False


# iterate through each entity in column until requirements are met
def check_column(x, world_size):
	pumpkin_count = 0
	is_expecting_pumpkin = False

	for y in range(world_size):
		expected_entity = consts.ENTITY_MAP[x][y]

		try_water()

		if expected_entity == Entities.Pumpkin:
			is_expecting_pumpkin = True
			if is_pumpkin_ready():
				pumpkin_count += 1

		else:
			try_harvest()
			plant_entity()
			try_harvest()

		move(North)
	
	# if it's a column with pumpkins and there's some missing, check the column again
	if is_expecting_pumpkin and pumpkin_count < 6:
		return check_column(x, world_size)


# iterate through every block in the farm
def scan_farm():
	world_size = get_world_size()

	# harvest pumpkin patch that was finished last iteration
	try_harvest()

	for x in range(world_size):
		check_column(x, world_size)
		move(East)

reset_drone()

while True:
	scan_farm()
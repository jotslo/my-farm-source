import consts

first_pumpkin_id = -1

# move drone back to 0, 0
def reset_drone():
	x, y = get_pos_x(), get_pos_y()

	while x > 0:
		move(West)
		x -= 1
	
	while y > 0:
		move(South)
		y -= 1


def get_expected_entity():
	x, y = get_pos_x(), get_pos_y()

	if x >= len(consts.ENTITY_MAP) or y >= len(consts.ENTITY_MAP[x]):
		length = len(consts.RANDOM_ENTITY_LIST)
		return consts.RANDOM_ENTITY_LIST[random() * length]
	
	return consts.ENTITY_MAP[x][y]


# plant the expected entity at the current position
def plant_entity():
	expected_entity = get_expected_entity()

	valid_grounds = consts.GROUND_MAP[expected_entity]
	if get_ground_type() not in valid_grounds:
		till()

	if expected_entity == Entities.Sunflower:
		while get_entity_type() != Entities.Sunflower or measure() < consts.MIN_SUNFLOWER_PETALS:
			harvest()
			plant(Entities.Sunflower)

	if get_entity_type() == expected_entity:
		return
	
	plant(expected_entity)


# attempt to harvest the entity under the drone
def try_harvest():
	if can_harvest():
		harvest()


# water the ground if it is too dry
def try_water():
	if get_water() < 0.3:
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
	global first_pumpkin_id

	pumpkin_count = 0
	is_expecting_pumpkin = False

	for y in range(world_size):
		expected_entity = get_expected_entity()

		try_water()

		if expected_entity == Entities.Pumpkin:
			is_expecting_pumpkin = True
			if is_pumpkin_ready():
				pumpkin_count += 1
			
			# store the first pumpkin's id
			if first_pumpkin_id == -1:
				first_pumpkin_id = measure()
			
			# if we're at the end of the pumpkin and it has same ID as pumpkin1, harvest!
			if x == y == consts.PUMPKIN_SIZE - 1 and measure() == first_pumpkin_id:
				try_harvest()
				first_pumpkin_id = -1
				return

		else:
			try_harvest()
			plant_entity()
			try_harvest()

		move(North)
	
	# if it's a column with pumpkins and there's some missing, check the column again
	if is_expecting_pumpkin and pumpkin_count < consts.PUMPKIN_SIZE:
		return check_column(x, world_size)


# iterate through every block in the farm
def scan_farm():
	world_size = get_world_size()

	# harvest pumpkin patch that was finished last iteration
	try_harvest()

	for x in range(world_size):
		check_column(x, world_size)
		move(East)

		while get_pos_y() > 0:
			move(South)

reset_drone()

while True:
	scan_farm()
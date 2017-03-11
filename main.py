# imports
##
import sys, vtemu
from location import Location
from character import Character


# special definitions for colorized text
##
# if the terminal is Linux or Cygwin, use the following codes
if sys.platform in ['linux2', 'cygwin']:
	def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
	def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
	def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
	def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
	def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
	def prBlue(prt): print("\033[96m {}\033[00m" .format(prt))
	def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
	def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))

if sys.platform == 'win32':	
	def prRed(prt): print("\x1b[1;31m {}\x1b[00m" .format(prt))
	def prGreen(prt): print("\x1b[2;32m {}\x1b[00m" .format(prt))
	def prYellow(prt): print("\x1b[1;33m {}\x1b[00m" .format(prt))
	def prBlue(prt): print("\x1b[1;34m {}\x1b[00m" .format(prt))
	def prPurple(prt): print("\x1b[1;35m {}\x1b[00m" .format(prt))
	def prCyan(prt): print("\x1b[1;36m {}\x1b[00m" .format(prt))
	def prWhite(prt): print("\x1b[1;37m {}\x1b[00m" .format(prt)) 


class Realm(object):
	""" creates, stores and retrieves locations; presents narratives for each """
	
	# class variables
	##

	# define a dictionary which contains a tuple representing each Realm location's coordinates, paired with a list containing (1) a print statement description of the area and (2+) any accompanying commands required to add items to the player's inventory
	LOOT_LIST = {(0,0): ["After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk.", "tinder", "goat milk"],
			 	 (0,1): ["Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire.", "flint"], 
			 	 (0,2): ["You stumble upon a rusty blade.", "rusty blade"],
			 	 (-1,0): ["While searching the area, you begin to rifle through the pockets of the two bodies.  On the first, you find a notebook.  The second appears to still be alive so you don't approach him just yet.", "notebook"]
			 	}

	# TO_DO:  Add further items to these monster lists, including loot drops (randomized tiers of loot item lists) and NPC level (somewhat randomized also from tiers of NPC level lists)
	MONSTER_LIST = {(0,0): ['spider'],
				 	(0,1): ['spider', 'spider'],
					(0,2): ['spider'],
			   		(-1,0): ['bandit']
				   }

	#defines the input prompt
	PROMPT = '=---> '

	# methods
	##
	def __init__(self):
		self.locations = {}								# dictionary containing instances of Location class representing each traversible area of the Realm
		starting_coords = [0,0]
		self.add_location(starting_coords)
		self.player = self.create_Char()				# create player instance of character class
		self.narrative(self.player.get_coords())		# this line starts the loop which gets user input for interacting with the environment

	def create_Char(self):
		""" prompts user to answer questions in order to create their character """
		# 
		# print "Welcome to Realm of Reckoning.  Please answer the following questions to create your character:"
		# 			
		# print "1.  What is your character's gender?"
		# sex = raw_input("?")
		# if sex not in ["m", "male", "f", "female"]:
			# print "Please enter male or female."
		# 			
		# print "2.  What is your character's name?"
		# name = raw_input("?")
		# 
		# player = Character(sex, name, 10, 5, 3, 0, [], [0,0])
		# print "Ok, here's some information about your character: ", player
		return Character("male", "Dexter", 10, 5, 3, 0, [], [0,0])

	def get_master_loot_list(self):
		return self.LOOT_LIST

	def get__master_monster_list(self):
		return self.MONSTER_LIST

	def narrative(self, area):
		""" Handles delivery of narrative text based on location as well as any choices available in any given location 
			TO_DO:  repair alternate version which allows for encounters
		"""

		key = tuple(area)

		narratives = {(0,0): "You are standing in the same field in which you first awoke\nwithout any memory of how you got here.  Which way?\n",
					 (-1,0): "\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)",
					  (0,1): "\n     You walk for some time to finally arrive at an old, \napparently abandoned, fortress which has crumbled with time.  \nThere is nothing here but ruin.  As you approach an outcrop of rock, you realize there is a narrow passage leading down into the ground, perhaps an old cellar entrance.  Do you enter? (y/n)",
					  (0,2): "\n     As you head north around the abandoned and crumbling\nfortress you see a valley spread out before you.  In the\ndistance to the north is a village with wafts of smoke being\ncarried off by the breeze trailing over the scene like\nthe twisted tails of many kites.  To the west gently\nsloping foothills transition into distant blue mountains\nand to the east, a vast forest conspires to block out all \nsurface detail."
					 }

		# narratives = {(0,0): ["\n     You are standing in the same field in which you first awoke\nwithout any memory of how you got here.  Which way?\n"],
					  # (-1,0): ["\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)"],
					  # (0,1): ["\n     You walk for some time to finally arrive at an old, \napparently abandoned, fortress which has crumbled with time.  \nThere is nothing here but ruin.  As you approach an outcrop of rock, you realize there is a narrow passage leading down into the ground, perhaps an old cellar entrance.  Do you enter? (y/n)"],
					  # (0,2): ["\n     As you head north around the abandoned and crumbling\nfortress you see a valley spread out before you.  In the\ndistance to the north is a village with wafts of smoke being\ncarried off by the breeze trailing over the scene like\nthe twisted tails of many kites.  To the west gently\nsloping foothills transition into distant blue mountains\nand to the east, a vast forest conspires to block out all \nsurface detail."]}

		if self.player.newplayer == True:
			print "\n     You awaken to the distant sound of commotion to your west.  \nYou open your eyes and realize you are in a vulnerable spot\nin an open field.  You look west toward the direction of\nthe distant sounds and hear that it is now quiet.  To your \nnorth in the distance is a fortress.  To your east is a \nforest and to your south is a riverbank with a boat tied at \na pier.  \n\nWhich direction do you go? (Press 'h' for help)"
			self.player.newplayer = False

		elif key in narratives:
			print narratives[key]


			# if len(narratives[key]) > 1:  # if there are commands associated with this area, execute them
				# for i in range(1,len(narratives[key])):
					# temp_list = area[:]
					# temp_list.append(i)
					# choice_key = tuple(temp_list)
					# narratives[key][i](choice_key)
 		else:
			prRed("Under construction.  Returning to the beginning.")
			self.teleport([0,0])
	
		# get user input
		user_input = raw_input(self.PROMPT)
		# get rid of any capitalized typing by the user
		user_input.lower()

		# call keydown to handle user input
		self.keydown(user_input)

	def encounter(self, choice_key):
		# a third number has been added to the tuple key to represent level of depth (decision/choice 1: outcome, decision/choice 2/outcome, etc.)  The Value of each of these keys goes in the form:  ['user-input choice', print narrative, command(s) to execute]
		
		# prompt user for input in respose to encounter
		input = raw_input(self.PROMPT).lower()

		# cast choice_key as a tuple so it can be used as a dictionary key
		choice_key = tuple(choice_key)

		outcomes = { (-1,0,1): 
								{'y': ["\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your neck.  Your life fades slowly.", self.die], 'n': ["\nWell, daylight's a-wasting.  Where to now?"]}, 
					 (0,1,1):
					 			{'y': ["\nYou steal yourself and proceed down the cracked and disintegrating steps only to find a locked wooden door.  Do you attempt to force the lock? (y/n)", self.next_choice], 'n': ["\nWhere to now?"]},
					 (0,1,2):   {'y': ["\nYou put all your force into it as you drive your shoulder into the door.  It gives way in a sudden explosion of splinters, dust and debris.  It's too dark to proceed safely without a lantern."], 'n': ["\nWhere to now?"]} }
		if choice_key in outcomes:
			if len(outcomes[choice_key][input]) > 1:
				for i in range (1,len(outcomes[choice_key][input])):
					if outcomes[choice_key][input][i] == self.next_choice:
						self.next_choice(choice_key)
					else:
						outcomes[choice_key][input][i]()
		else:
			print "Please type 'h' for help."

	def add_location(self, coords):
		""" adds a location to the Realm """
		# check for existence of loot entry in dictionary before assigning loot listed there to this instance's loot list
		# location_name = self.get_location_name(coords)
		key = tuple(coords)

		if key in self.LOOT_LIST:
			loot = self.LOOT_LIST[key]
			loot_present = True
		else:
			loot = []
			loot_present = False

		if key in self.MONSTER_LIST:
			monster_list = self.get__master_monster_list()
			monsters = monster_list[key]
			monsters_present = True
		else:
			monsters = []
			monsters_present = False
		
		# create new instance of Location and add it to the list of instances, then set it to the player's current location
		new_location = Location(coords, monsters_present, loot_present, monsters, loot)
		self.locations[new_location.name] = new_location
		self.current_player_location = self.locations[new_location.name]

	def get_locations_dict(self):
		return self.locations

	def check_location_existence(self, coords):
		""" Check for the existence of a Location object and create it if it doesn't exist yet.  This is called when moving to a different location on the Realm """
		name = self.get_location_name(coords)

		if name in self.get_locations_dict():
			return True
		else:
			return False

	def get_location_name(self, coords):
		""" takes Location coordinates as input, returning a string name for a Location """
		name = str(coords[0]) + str(coords[1])
		return name

	def get_location(self, current_location_coords):
		""" attempts to return an object with a name based on the current location coordinates 	if the object name doesn't exist, throws NameError exception """
		try:
			string = self.get_location_name(current_location_coords)
			return self.locations[string]
		except NameError:
			print "Location does not exist."

	def teleport(self, coords):
		self.player.set_coords(coords)
		self.narrative(self.player.get_coords())

	def move(self, char, direction):
		""" taking character instance and user input direction as parameters, handles player movement between Locations """
		# pair all options with an action in a dictionary
		directions = { "n": [char.get_coord(0),(char.get_coord(1)+1)],
					   "s": [char.get_coord(0),(char.get_coord(1)-1)],
					   "e": [(char.get_coord(0)+1),char.get_coord(1)],
					   "w": [(char.get_coord(0)-1), char.get_coord(1)] }

		# execute directional movement by updating player's coords
		if direction in directions:
			char.set_coords(directions[direction])
			coords = char.get_coords()
		# check for the existence of the Location to which the player has moved 
		if self.check_location_existence(coords):
			self.get_location(coords)
		else:
			self.add_location(coords)
		self.narrative(self.player.get_coords())

	def help_menu(self):
		prBlue("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \ni check your inventory\na attributes\nq quit\nh help\n")

	def inv_list(self):
		""" Lists all the items in the player's inventory
		"""
		print "\nInventory: \n" 
		prGreen(self.player.get_inventory())

	def inv_add(self, item):
		""" Adds an item to the player's inventory, asking if they wish to drop an item if the inventory is full. """
		if len(self.player.inventory) < 5:
			self.player.inventory.append(item)
			prGreen("\n %s added to inventory." % (item))
		else:
			print "Inventory full.  Drop an item? (y/n)"
			choice = raw_input(self.PROMPT)
			if choice in {'y', 'yes', 'Y', 'Yes', 'YES'}:
				self.inv_prmpt_remove()
				self.inv_add(item)
			else:
				print "Dropped %s on the ground." % (item)

	def search_area(self):
		""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk. """
		# cast list representing player's x/y coordinates as a tuple for comparison to LOOT_LIST dictionary's keys
		area = tuple(self.player.get_coords())

		loot_present = self.current_player_location.get_loot_present()

		if loot_present:	# if loot is present in the area
			if area in self.LOOT_LIST:  # if the area has items contained in the loot list (redundant)
				for i in range(1, len(self.LOOT_LIST[area])):
					self.inv_add(self.LOOT_LIST[area][i])	# execute the command(s) contained in the second element of the value list, adding said items to player's inventory
		else:
			prYellow("You found nothing useful here.")

	def die(self):
		"""	this function ends the program """
		message = prRed("\nGame Over.\n")
		sys.exit(message)

	def quit_game(self):
		prRed("Are you sure you want to exit? (y/n)")
		choice = raw_input(self.PROMPT)

		if choice.lower() in {'y', 'Y', 'yes', 'Yes', 'YES'}:
			self.die()
		elif choice.lower() in {'n', 'no'}:
			print "Let's get back to it then."

	def keydown(self, user_input):
		""" Handles user input """
		
		# dictionary of possible user inputs with matching names of methods to call for each
		inputs = {"n": self.move, 
	  	  		  "s": self.move,
	  	  		  "e": self.move,
	      		  "w": self.move,
	      		  "h": self.help_menu,	  	  		
	  	  		  "i": self.inv_list,
	  	  		  "a": self.player.attrib_list,
	  	  		  "x": self.search_area,
	  	  		  "q": self.quit_game}
		
		if user_input in inputs:
			if user_input in ["n", "s", "e", "w"]:
				inputs[user_input](self.player, user_input)  # call the function that matches the key pressed by the user, passing the parameter if it is a direction of travel
			else:  # otherwise don't pass a parameter
				inputs[user_input]()
		else:
			print "Please type 'h' for help."
		self.narrative(self.player.get_coords())


world = Realm()

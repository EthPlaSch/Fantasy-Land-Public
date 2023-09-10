#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

# Importing necessary python Library
import time

# Importing Other Files we are working with
import gui
import character
import map_management
import battle

# Importing the window and entire GUI
app = gui.simpleapp_tk(None)
app.title('RPG Battle (edited)')


# Using the write function from gui.py, this will be a reoccuring method we use to draw to the window
# Game title and basic information printed
app.write('''
 _    _      _                             _         
| |  | |    | |                           | |        
| |  | | ___| | ___  ___  _ __ ___   ___  | |_  ___  
| |/\| |/ _ \ |/ __|/ _ \| '_ ` _ \ / _ \ | __|/ _ \ 
\  /\  /  __/ | (__| (_) | | | | | |  __/ | |_| (_) |
 \/  \/ \___|_|\___|\___/|_| |_| |_|\___|  \__|\___/

____________ _____  ______       _   _   _      _ 
| ___ \ ___ \  __ \ | ___ \     | | | | | |    | |
| |_/ / |_/ / |  \/ | |_/ / __ _| |_| |_| | ___| |
|    /|  __/| | __  | ___ \/ _` | __| __| |/ _ \ |
| |\ \| |   | |_\ \ | |_/ / (_| | |_| |_| |  __/_|
\_| \_\_|    \____/ \____/ \__,_|\__|\__|_|\___(_)

''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")

# Function that allows the player to choose which game mode to play in
def set_mode():
  """ Select the game mode """
  # This is an error checking version of reading user input
  # This will be explained in class - pay attention!!
  # Understanding try/except cases is important for
  # verifying user input
  
  # Trying to get input from the player (1, 2, or quit) and selecting a game mode based on that
  # If input does not match expected, raise value error
  try:
    # Displaying options to the player
    app.write("Please select a side:")
    app.write("1. Good")
    app.write("2. Evil")
    app.write("")
    
    # App stops until input is recieved
    app.wait_variable(app.inputVariable)
    # Setting mode to input
    mode = app.inputVariable.get()
    
    # Close window if 'quit' is typed
    if mode == 'quit':
      app.quit()
    
    # Converting mode to an int
    mode = int(mode)
    
    # If input does not match expected, raise value error
    if mode not in range(1,3):
      raise ValueError
  
  # Letting the user know they need to input an expected input
  # Then asking for input again
  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    mode = set_mode()
  
  return mode # Returing the mode value to be passed into the set_race, create_player, and create_enemies functions

# Function that allows the player to choose which race to play as
# Takes in the mode from the set_mode function as an arguement
def set_race(mode):
  """ Set the player's race """
  
  # If-else deciding to run the code for good or evil characters
  if mode == 2: # Evil Mode
    app.write("Playing as the legally distinct Forces of Not Sauron.")
    app.write("")
  
    # Trying to get input from the player (1, 2, 3, 4, or quit) and selecting a race based on that
    # If input does not match expected, raise value error
    # race selection - evil
    try:
      # Displaying options to the player
      app.write("Please select your race:")
      app.write("1. Goblin")
      app.write("2. Orc")
      app.write("3. Uruk")
      app.write("4. Wizard")
      app.write("5. Skeleton")
      app.write("6. Slime")
      app.write("")
      
      # App stops until input is recieved
      app.wait_variable(app.inputVariable)
      # Setting race to input
      race = app.inputVariable.get()
      
      # Close window if 'quit' is typed
      if race == 'quit':
        app.quit()
      
      # Converting race to an int
      race = int(race)
      # If input does not match expected, raise value error
      if race not in range(1,7):
        raise ValueError
    
    # Letting the user know they need to input an expected input
    # Then asking for input again
    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")
      race = set_race(mode)

  else: # Good Mode
    app.write("Playing as the legally distinct Free Peoples of Just a Little Up from Middle Earth.")
    app.write("")

    # Trying to get input from the player (1, 2, 3, 4, or quit) and selecting a race based on that
    # If input does not match expected, raise value error
    # race selection - good
    try:
      # Displaying options to the player
      app.write("Please select your race:")
      app.write("1. Elf")
      app.write("2. Dwarf")
      app.write("3. Human")
      app.write("4. Hobbit")
      app.write("5. Wizard")
      app.write("6. Slime")
      app.write("")
      
      # App stops until input is recieved
      app.wait_variable(app.inputVariable)
      # Setting race to input
      race = app.inputVariable.get()
      
      # Close window if 'quit'
      if race == 'quit':
        app.quit()
        
      # Converting race to an int
      race = int(race)
      # If input does not match expected, raise value error
      if race not in range(1,7):
        raise ValueError
    
    # Letting the user know they need to input an expected input
    # Then asking for input again
    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")
      race = set_race(mode)
  
  return race # Returing the race value to be used in the create_player function

# Function that allows the player to choose their character name
def set_name():
  """ Set the player's name """
  
  # Trying to get input from the player (Any characters) and setting that as the character name
  # If input does not match expected, raise value error
  try:
    # Asking player for preferred name
    app.write("Please enter your Character Name:")
    app.write("")
    
    # App stops until input is recieved
    app.wait_variable(app.inputVariable)
    # Setting character name to input
    char_name = app.inputVariable.get()

    # Close window if 'quit' is typed
    if char_name == 'quit':
      app.quit()

    # If input is blank, raise value error
    if char_name == '':
      raise ValueError

  # Letting the user know they need to input an expected input
  # Then asking for input again
  except ValueError:
    app.write("")
    app.write("Your name cannot be blank")
    char_name = set_name()

  return char_name # Returing the character name to be used in the create_player function

# Funcition that creates the player object based on previous collected information
# Takes in the mode, the player race, and character name from the set_mode, set_race, and set_name functions as an arguement
def create_player(mode, race, char_name):
  """ Create the player's character """
  # Evil
  if mode == 2: # if charcter is evil (2)
    # using the returned race value to set player's race (determining which if-statment to use)
    # under each if-statment, using the Character class from character.py to create a player object with a name and race
    if race == 1:
      player = character.Goblin(char_name, app)
    elif race == 2:
      player = character.Orc(char_name, app)
    elif race == 3:
      player = character.Uruk(char_name, app)
    elif race == 4:
      player = character.Wizard(char_name, app)
    elif race == 6:
      player = character.Slime(char_name, app)
    else:
      player = character.Skeleton(char_name, app)
  # Good
  else: # if charcter is good
    # using the returned race value to set player's race (determining which if-statment to use)
    # under each if-statment, using the Character class from character.py to create a player object with a name and race
    if race == 1:
      player = character.Elf(char_name, app)
    elif race == 2:
      player = character.Dwarf(char_name, app)
    elif race == 3:
      player = character.Human(char_name, app)
    elif race == 4:
      player = character.Hobbit(char_name, app)
    elif race == 6:
      player = character.Slime(char_name, app)
    else:
      player = character.Wizard(char_name, app)
      
  return player # Returning the created player object to be used later

# Function that allows the player to choose their difficulty
def set_difficulty():
  """ Set the difficulty of the game """
  
  # Trying to get input from the player (e, m, h, l, or quit) and setting that as the character name
  # If input does not match expected, raise value error
  try:
    # Displaying options to the player
    app.write("Please select a difficulty level:")
    app.write('p - Passive-ish')
    app.write("e - Easy")
    app.write("m - Medium")
    app.write("h - Hard")
    app.write("l - Legendary")
    app.write('a - Absurd')
    app.write("")
    
    # App stops until input is recieved
    app.wait_variable(app.inputVariable)
    # Setting mode to input
    difficulty = app.inputVariable.get()

    # Close window if 'quit'
    if difficulty == 'quit':
      app.quit()

    # If input does not match expected, raise value error
    if difficulty not in ['p','e','m','h','l', 'a'] or difficulty == '':
      raise ValueError

  # Letting the user know they need to input an expected input
  # Then asking for input again
  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    difficulty = set_difficulty()

  return difficulty # To be passed into the create_enemies funciton

# Function that creates enemy objects based on player's selected difficulty
# Takes in the mode and the difficulty from the set_mode and set_difficulty functions as an arguement
def create_enemies(mode, difficulty): # Update later to create enemies at random on a map but with a higher chance based on difficulty
  """ Create the enemies """
  # If mode was evil (picked 2) created good enemies
  if mode == 2: # Evil Mode - good enemies
    # based on the returned difficulty create "good" enemies objects with a name
    if difficulty == 'p':
      enemies = [character.Slime('Bob', app), character.Slime('Cyprus', app)]
    elif difficulty == 'm':
      enemies = [character.Hobbit("Peregron", app), character.Hobbit("Meriaduc", app), character.Human("A-owyn", app)]
    elif difficulty == 'h':
      enemies = [character.Dwarf("Gomlo", app), character.Elf("Legolos", app), character.Human("Boromor", app)]
    elif difficulty == 'l':
      enemies = [character.Human("Faramor", app), character.Human("Aragarn", app), character.Wizard("Gandolf", app)]
    elif difficulty == 'a':
      enemies = [character.Human("Jeffery", app), character.Dwarf("Hendrick", app), character.Wizard("Gandolf", app), character.Elf('Jeremy', app), character.Hobbit('Harry Baggins', app)]
    else:
      enemies = [character.Hobbit("Frodi", app), character.Hobbit("Som", app)]
      
  # If mode was good created bad enemies
  else: # Good Mode - evil enemies
    # based on the returned difficulty create "Bad" enemies objects with a name
    if difficulty == 'p':
      enemies = [character.Slime('Trubbish', app), character.Slime('Trabbish', app)]
    elif difficulty == 'm':
      enemies = [character.Goblin("Azig", app), character.Skeleton("Gorkol", app), character.Orc("Sharko", app)]
    elif difficulty == 'h':
      enemies = [character.Orc("Shagrit", app), character.Orc("Gorbog", app), character.Uruk("Lortz", app)]
    elif difficulty == 'l':
      enemies = [character.Orc("Grishnikh", app), character.Uruk("Lortz", app), character.Wizard("Sarumon", app)]
    elif difficulty == 'a':
      enemies = [character.Uruk("Neshy", app), character.Uruk("Wes", app), character.Wizard("Anti-Gandolf", app), character.Orc('Myrtha', app), character.Goblin('Gringots', app), character.Skeleton('Paper Weight', app)]
    else:
      enemies = [character.Goblin("Azig", app), character.Goblin("Gorkol", app)]

  return enemies # return the created enemy objects to be used later

# Function that runs at the end of a playthrough giving the player the option to quit or play again
def quit_game():
  """ Quits the game """
  # Try-except to prevent any crashing
  try:
    # Asking the player if they want to play again
    app.write("Play Again? (y/n)")
    app.write("")
    
    # App stops until input is recieved
    app.wait_variable(app.inputVariable)
    # Setting character name to input
    quit_choice = app.inputVariable.get()

    # Close window if 'quit' is typed
    if quit_choice == 'quit':
      app.quit()

    # if the input was not expected (so not y, n, or quit) then raise the error
    if quit_choice not in 'yn' or quit_choice == '':
      raise ValueError

  # Letting the user know they need to input an expected input
  # Then asking for input again
  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    quit_choice = quit_game()

  return quit_choice # Returns whether or not the player quit, n (quit), or y (play again)

# Function that prints the game results after the game is either won or lost
def print_results():
  # Signalling the end of the game to the player
  app.write("Game Over!")
  
  # Using the values that have built up over the game to display end stats to the player
  app.write("No. Battles: {0}".format(str(battles)))
  app.write("No. Wins: {0}".format(wins))
  app.write("No. Kills: {0}".format(kills))
  app.write("Success Rate (%): {0:.2f}%".format(float(wins*100/battles)))
  app.write("Avg. kills per battle: {0:.2f}".format(float(kills)/battles))
  app.write("")

# Whether or not the player starts the 
def map_choice(player, enemies):
  app.write("Type Map to play")
  app.write("")

  # App stops until input is recieved
  app.wait_variable(app.inputVariable)
  # Setting mode to input
  map_choice = app.inputVariable.get()
   
  try: 
    # Close window if 'quit' is typed
    if map_choice == 'quit':
      app.quit()
    elif map_choice.lower() == 'map':
      global game_map
      game_map = map_management.Map(player, enemies, app, [20, 30], [], battles, wins, kills)
      print_map = game_map.draw_map()
    else:
      raise ValueError

  except ValueError:
    # Tell the player their choice was not vaild
    app.write("You must enter a valid choice, quitting game")
    app.write("")
    time.sleep(1)
    app.quit()
    
# The main function that is run to play the game
def main():
  
  # Resetting the values to 0 for the next playthrough
  # They needed to be global to be reached outside of the main function
  global battles
  battles = 0
  global wins
  wins = 0
  global kills
  kills = 0

  # Starting the next playthrough by running above functions
  # This is the player chosing the: Mode (good or evil), Character race, Character name
  mode = set_mode()
  race = set_race(mode)
  char_name = set_name()

  # Creating the player object based on everything previously run
  player = create_player(mode, race, char_name)

  # Displaying this information to the player
  app.write(player)
  app.write("")

  # Dealing with difficulty (setting and enenmy creation)
  difficulty = set_difficulty()
  enemies = create_enemies(mode, difficulty)
  
  map_choice(player, enemies)  
  
  # Main game loop
  while True:
      
    # creating a variable with the player's choice to quit or not
    quit = quit_game()
    
    battles += game_map.battles
    wins += game_map.wins
    kills += game_map.kills
    
    # Calling print_results() to print the results
    print_results()

    # If-else statement
    # If player wants to quit, end the game
    if quit == "n":
      app.write("Thank you for playing RPG Battle.")
      time.sleep(2)
      app.quit()

    # If not, reset everything and play again
    else:
      # Playing again - reset all enemies and players
      player.reset()
      for enemy in enemies:
        enemy.reset()
      map_choice(player, enemies)

# This basically tells you this is a script that can be run, this is not a library
if __name__ == '__main__':
  
  # Running the main function (playing the game)
  main()
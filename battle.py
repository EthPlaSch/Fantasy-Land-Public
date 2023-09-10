#!/usr/local/bin/python3
"""
Battle.py - The battle class manages the events of the battle

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

# Import Python Modules
import sys
import time

# Battle class stores the state of the battle and manages the battle loop
# Currently the battle class instanciates at the beginning of the program, change this to instanciates on collision with enemies
class Battle:

  def __init__(self, player, enemies, app, player_tile):
    
    """
    Instantiates a battle object between the players and enemies specified,
    sending output to the given gui instance
    """
    
    # Setting the initial state of the battle
    self.player = player
    self.enemies = enemies
    self.app = app
    self.enemy_turn = False
    self.player_tile = player_tile
    self.turn = 1
    self.wins = 0
    self.kills = 0
    self.player_won = False
    self.player_lost = False
    
    self.app.write("")
    self.app.write('You were caught by an enemy on patrol! All other enemies rushed to your location to fight!')
    self.app.write('')
    time.sleep(1)

  # Plays out the battle, runs the battle actions, calling methods that run the calculations
  def play(self):
    """
    Begins and controls the battle
    returns tuple of (win [1 or 0], no. kills)
    """
    
    # While the battle hasn't ended
    while not self.player_won and not self.player_lost:
      
      # Print whose turn it is and pause for 1 second
      self.app.write("Turn "+str(self.turn))
      self.app.write("")
      time.sleep(1)
      
      if self.player_tile == 'V ':
        self.app.write("You are battling in the Volcanic area, burn damage is applied every turn, all parties take 10 damage per turn.")
        self.app.write("")
        time.sleep(0.5)
        self.player.health -= 10
        for enemy in self.enemies:
          enemy.health -= 10
      
      # This is where the bulk of the battle takes place
      # Calling these methods is running the all the player actions, inputs, and calculations, same goes for the enemies
      # If the player speed is greater than the average enemy speed, player goes first, else enemies go first
      enemy_speed = self.turn_order()
      
      if self.player.speed >= enemy_speed:
        self.do_player_actions()
        self.enemy_turn = self.do_enemy_actions()
      else:
        self.enemy_turn = self.do_enemy_actions()
        if self.enemy_turn != False:
          self.do_player_actions()
      
      # Advance turn counter
      self.turn += 1
      
    return (self.wins, self.kills, self.enemy_turn) # This will update the player stats to be printed later

  # Calculating the average enemy speed to decide the turn order
  def turn_order(self):
    
    enemy_speed = 0
    num_enemy = 0
    
    for enemy in self.enemies:
      enemy_speed += enemy.speed
      num_enemy += 1
    
    enemy_speed = (enemy_speed/num_enemy)
    
    return enemy_speed
    
  # Gets the player input for their turn
  def get_action(self):
    """ Gets the player's chosen action for their turn """
    
    player_race = self.player.__class__.__name__

    try:
      # Present the player with the options for their turn
      self.app.write(self.player.name + "'s Turn:")
      self.app.write("1. Attack Enemies")
      self.app.write("2. Cast Magic")
      self.app.write("3. Use Potion")
      self.app.write("4. Flee")
      if player_race == "Ork":
        self.app.write('5. Harden (boost defense)')
      if player_race == "Slime" and self.player.health < self.player.max_health:
        self.app.write('5. Get ANGRY (major attack boost)')
      self.app.write("")
      # Pause, wait for player response and set player_action to the player's response
      self.app.wait_variable(self.app.inputVariable)
      player_action = self.app.inputVariable.get()

      # Close window if 'quit' is typed
      if player_action == 'quit':
        self.app.quit()

      player_action = int(player_action)
      # If the player's choice was not vaild, raise an error
      if player_race == 'Ork' or player_race == 'Slime':
        if player_action not in range(1,6):
          raise ValueError
      else:
        if player_action not in range(1,5):
          raise ValueError

    except ValueError:
      # Tell the player their choice was not vaild
      self.app.write("You must enter a valid choice")
      self.app.write("")
      # Try again
      player_action = self.get_action()
    
    return player_action # Return the player's action to determine what to do next (will be used in the do_player_actions method)

  # If the player has selected to use a spell this will deal with the spell UI logic
  def select_spell(self):
    """ Selects the spell the player would like to cast """
    
    # Checking the player's race to see what spells they can cast
    player_race = self.player.__class__.__name__

    try:
      # Print spell options for the player, all 3 if a Wizard, only shield if any other class
      self.app.write("Select your spell:")
      if player_race == "Wizard" and self.player.mana >= 10:
        self.app.write("1. Fireball (10 mp)")
      if self.player.mana >= 20:
        self.app.write("2. Shield (20 mp)")
      if player_race == "Wizard":
        self.app.write("3. Mana Drain (no mp cost)")
      self.app.write("0. Cancel Spell")
      self.app.write("")
      # Pause, wait for player response and set spell_choice to the player's response
      self.app.wait_variable(self.app.inputVariable)
      spell_choice = self.app.inputVariable.get()

      # Close window if 'quit' is typed
      if spell_choice == 'quit':
        self.app.quit()
        
      spell_choice = int(spell_choice)
      # If player's choice was 0, return 'False' (used to back out of the spells menu later)
      if spell_choice == 0:
        return False
      
      # Check if the player can cast that spell
      valid_spell = self.player.valid_spell(spell_choice) # Vaild spell is a method called that is in the character object (from character.py)
      if not valid_spell:
        raise ValueError
      
    except ValueError:
      # Tell the player their choice was not vaild
      self.app.write("You must enter a valid choice")
      self.app.write("")
      # Try again
      spell_choice = self.select_spell()
    
    return spell_choice # The player's spell choice, used later in do_player_actions

  # If the player has selected to use a potion this will deal with the potion UI logic
  def select_potion(self):
    
    try:
      # List potion options to the player
      self.app.write("Select your Potion:")
      self.app.write("0. Cancel Potion")
      
      # For every potion the player has, print it
      i = 1
      for potion in self.player.potions:
        self.app.write(f"{i}. {potion.title()}")
        i += 1
      
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      potion_choice = self.app.inputVariable.get()
      
            # Close window if 'quit' is typed
      if potion_choice == 'quit':
        self.app.quit()
        
      potion_choice = int(potion_choice)
      
      # If player's choice was 0, return 'False' (used to back out of the potions menu later)
      if potion_choice == 0:
        return False
     
      # Check if the player can use that potion
      valid_spell = self.player.valid_potion(potion_choice) # Vaild potion is a method called that is in the character object (from character.py)
      if not valid_spell:
        raise ValueError
      
      if potion_choice == 0:
        potion_name = 'back out'
      else: 
        potion_name = self.player.potions[potion_choice - 1]
      
      return potion_name
      
    except ValueError:
      # Tell the player their choice was not vaild
      self.app.write("You must enter a valid potion choice")
      self.app.write("")
      # Try again
      potion_choice = self.select_potion()
      
  # Allows the player to select a target
  def choose_target(self):
    """ Selects the target of the player's action """
    try:
      self.app.write("Choose your target:")
      # use j to give a number option
      j = 0
      
      while j < len(self.enemies): # Number of enemies in play
        
        # If enemy 1 has health
        if self.enemies[j].health > 0:
          # Print the enemies name and the number associated with them
          self.app.write(str(j) + ". " + self.enemies[j].name)
          
        j += 1
        
      self.app.write("")
      # Pause, wait for player response and set target to the player's response
      self.app.wait_variable(self.app.inputVariable)
      target = self.app.inputVariable.get()

      # Close window if 'quit' is typed
      if target == 'quit':
        self.app.quit()

      target = int(target)
      # If the player's choice was not vaild (chose a number that isn't one of the enemies), raise an error
      if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0:
        raise ValueError
      
    except ValueError:
      # Tell the player their choice was not vaild
      self.app.write("You must enter a valid choice")
      self.app.write("")
      # Try again
      target = self.choose_target()

    return target # Used later to determine which enemy the player should attack

  # Allows the player to choose their stance
  def choose_stance(self):
    try:
      # Print player options
      self.app.write("Choose your stance:")
      self.app.write("a - Aggressive")
      self.app.write("d - Defensive")
      self.app.write("b - Balanced")
      self.app.write("")
      # Pause, wait for player response and set stand_choice to the player's response
      self.app.wait_variable(self.app.inputVariable)
      stance_choice = self.app.inputVariable.get()

      # Close window if 'quit' is typed
      if stance_choice == 'quit':
        self.app.quit()

      # If the player's choice was not vaild (not an expected choice), raise an error
      if stance_choice not in ['a','d','b'] or stance_choice == '':
        raise ValueError

    except ValueError:
      # Tell the player their choice was not vaild
      self.app.write("You must enter a valid choice")
      self.app.write("")
      # Try again
      stance_choice = self.choose_stance()
    
    return stance_choice # Return the player's stance choice to be used in calculations later

  # Method that calls the above methods based on player input (to perform player actions)
  def do_player_actions(self):
    """ Performs the player's actions """
  
    turn_over = False
    player_race = self.player.__class__.__name__
  
    while not self.player_won and not turn_over:

      # Give the player information about their character, then give them the option to set their stance
      self.player.print_status() # Method is part of the character object from character.py
      stance_choice = self.choose_stance() 
      self.player.set_stance(stance_choice) # Method is part of the character object from character.py
      
      # Set the player's action (using the get_action method)
      player_action = self.get_action()

      has_attacked = False
     
      # Based on the player's chosen action
      if player_action == 3: # Use a potion
        potion_choice = self.select_potion()
        
        if potion_choice != 'back out':
          # Raise attack by 10%
          if potion_choice == 'attack':
            self.player.use_attack_potion()
          # Heal player by 100 HP
          elif potion_choice == 'health':
            self.player.use_health_potion()
    
      elif player_action == 2: # Cast a spell
        spell_choice = self.select_spell()

        # If the spell choice is 0, back out of the menu, otherwise perform spell logic
        if spell_choice != 0:
          has_attacked = True
          if spell_choice == 1 or spell_choice == 3:
            target = self.choose_target()
            # If this returns true, an enemy has been killed
            if self.player.cast_spell(spell_choice, self.enemies[target]): # Method is part of the character object from character.py
              self.kills += 1
          else:
            self.player.cast_spell(spell_choice) # Method is part of the character object from character.py
            
      elif player_action == 5:
        if player_race == 'Ork': 
          self.player.defense_boost()
          has_attacked = True
        elif player_race == 'Slime':
          self.player.angry_slime()
          has_attacked = True
         
      # As of current this is the 'Flee from battle option' it currently just closes the battle window which should return the player to the overworld
      # Surrounding enemies should be deleted or moved back to allow the player to escape and not be instantly put back into battle
      elif player_action == 4:
        self.app.write("You fled from battle, running far from this land never to be seen again.")
        self.app.write("")
        time.sleep(2)
        self.app.quit()
        
      else: # Attack
        target = self.choose_target()
        has_attacked = True
        
        # If this returns true, an enemy has been killed
        if self.player.attack_enemy(self.enemies[target]): # Method is part of the character object from character.py
          self.kills += 1
    
      turn_over = True
      
      # You have to attack to end the player's turn which is a bit broken
      if not has_attacked:
        turn_over = False
      else:      
        self.player_won = True
        # For each of the enemies, check if they are allow, if so the player hasn't won
        for enemy in self.enemies:
          if enemy.health > 0:
            self.player_won = False
            break

        if self.player_won == True:
          # Tell the player they have won, pause for 1 second, add to the wins counter
          self.app.write("Your enemies have been vanquished!!")
          self.app.write("")
          
          time.sleep(1)
          self.wins += 1

  # The logic for an the enemies' turn
  def do_enemy_actions(self):
    """ Performs the enemies' actions """
    
    # If the player hasn't won, print it's the enemies' turn
    if not self.player_won:
      self.app.write("Enemies' Turn:")
      self.app.write("")
      time.sleep(1)
    
      # For each of the enemies, if they aren't dead or if the player hasn't lost, call the enemies move method
      for enemy in self.enemies:
        if enemy.health > 0 and not self.player_lost:

          if not self.player_lost:
            self.player_lost = enemy.move(self.player) # Move is a method in the enemy object from the Character class

      # If the player has lost, print to let them know
      if self.player_lost == True:
        self.app.write("You have been killed by your enemies.")
        self.app.write("")
        time.sleep(1)
        return False
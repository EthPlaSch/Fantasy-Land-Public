#!/usr/local/bin/python3
"""
Character.py - Class definition for RPG Characters

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

# Import required Python modules
import time
import random

#--------------------------------------------------------------------------------#
# Define the attributes and methods available to all characters in the Character #
# Superclass. All characters will be able to access these abilities.             #
# Note: All classes should inherit the 'object' class.                           #
#--------------------------------------------------------------------------------#

# The Character class acts as a default template for all characters, will be inherited from any race specific subclasses
class Character:
  # -- Defines the attributes and methods of the base Character class -- #
  
  # Creating basic character traits
  def __init__(self, char_name, app):
    """ Parent constructor - called before child constructors """
    
    # Creating the basic attributes every character will have
    self.attack_mod = 1.0
    self.defense_mod = 1.0
    self.temp_attack = 1
    self.temp_defense = 1
    self.exp = 0
    self.level = 0
    self.name = char_name
    self.shield = 0
    self.max_shield = 50
    self.gold = 0
    
    # App being the window and GUI we created in gui.py
    self.app = app

  # Creating a string representation of the character we can print later
  def __str__(self):
    """ string representation of character """
    return str("You are " + self.name + " the " + self.__class__.__name__)

  # Default move for a character before the AI kicks in, in this case to heal if health is low
  def move(self, player):
    """
    Defines any actions that will be attempted before individual
    character AI kicks in - applies to all children
    """
    
    # Setting a default move the character will attempt if their health is low
    move_complete = False
    if self.health < 50 and 'health' in self.potions:
      # Assume defensive stance and heal
      self.set_stance('d')
      self.use_health_potion()
      move_complete = True
      
    # If not low on health, chose action in battle.py
    # Return whether or not the character made a move
    return move_complete

# -- Character Attacking Actions -- #

  # Method for choosing stance (player or characters)
  def set_stance(self, stance_choice): # Arguement - Character stance choice
    """ sets the fighting stance based on given parameter """
    
    # If character chooses the attack stance
    if stance_choice == "a":
      # Give a 30% attack bonus 
      self.attack_mod = 1.3
      # Give a 40% defence nerf
      self.defense_mod = 0.6
      # Print to the GUI what stance the character choose
      self.app.write(self.name + " chose aggressive stance.")

    # If character chooses the defence stance
    elif stance_choice == "d":
      # Give a 40% attack nerf
      self.attack_mod = 0.6
      # Give a 30% defence bonus
      self.defense_mod = 1.3
      # Print to the GUI what stance the character choose
      self.app.write(self.name + " chose defensive stance.")

    # If character chooses the balanced stance
    else:
      # Keep character attack and defence stats the same
      self.attack_mod = 1.0
      self.defense_mod = 1.0
      # Print to the GUI what stance the character choose
      self.app.write(self.name + " chose balanced stance.")
      
    # Print a blank line (makes things clearer)
    self.app.write("")

  # Method for attacking an enemy
  def attack_enemy(self, target): # Arguement - Character's choice to target
    ''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
    to be targeted). Returns True if target killed, False if still alive.'''

    # Adds some randomness to the attack power
    roll = random.randint(10,15)
    # Base damage calculator
    hit = int(roll * self.attack_mod * self.attack * self.temp_attack)
    # Print who attacks who (so the player knows) and pause for 1 second
    self.app.write(self.name + " attacks " + target.name + ".")
    time.sleep(1)
    
    # Counter Attack
    counter_attack = random.randint(1, 10)
    if counter_attack == 1:
      hit *= 1.5
      self.app.write(f'{target.name} foresaw the attack coming and dashed out of the way lauching a powerful counter attack!')
      self.app.write("")
      kill = self.defend_attack(int(hit))
    
    # Normal Attack
    else:
      # Adding 'random' critical hits
      crit_roll = random.randint(1, 10)
      if crit_roll == 10: # 1 in 10 chance for crit
        # Do double damage by x hit by 2
        hit = hit*2
        # Print if it was a crit to let the player know and pause for 1 second
        self.app.write(self.name + " scores a critical hit! Double damage inflicted!!")
        time.sleep(1)
        
      # Kill variable (was the target killed)
      # Run the defend_attack method
      kill = target.defend_attack(hit)
      # Pause for 1 second
      time.sleep(1)

    # If the attack did enough damage to kixll the target
    if kill:
      # Print who killed who to let the player know and pause for 1 second
      self.app.write(self.name + " has killed " + target.name + "!")
      self.app.write("")
      time.sleep(1)
       # If the character kills an enemy, award exp and gold
      earned_exp = int((target.exp_reward  * random.uniform(1, 1.5)))
      self.exp += earned_exp
      earned_gold = int((target.gold_reward * random.uniform(1, 1.5)))
      self.gold += earned_gold
      self.app.write(f'{self.name} gained {earned_exp} exp.')
      self.app.write(f'{self.name} gained {earned_gold} gold and now has {self.gold} gold.')
      self.app.write('')
      time.sleep(0.5)
      
      # Adding an effort values system to the game where if an enemy is killed, the character is rewarded with a minor stat boost
      if str(type(target)) == "<class 'character.Dwarf'>" or str(type(target)) == "<class 'character.Uruk'>":
        self.defense += 0.1
        self.app.write(f'{self.name} gained a small permanent defence boost.')
        self.app.write('')
        
      elif str(type(target)) == "<class 'character.Wizard'>":
        self.max_mana += 2
        self.mana += 2
        self.app.write(f'{self.name} gained 2 extra mana points. Max mana is now {self.max_mana}.')
        self.app.write('')
        
      elif str(type(target)) == "<class 'character.Elf'>" or str(type(target)) == "<class 'character.Goblin'>":
        self.max_health += 5
        self.health += 5
        self.app.write(f'{self.name} gained 5 extra health points. Max health is now {self.max_health}.')
        self.app.write('')
        
      elif str(type(target)) == "<class 'character.Hobbit'>" or str(type(target)) == "<class 'character.Orc'>":
        self.resistance += 0.1
        self.app.write(f'{self.name} gained a small permanent resistance boost.')
        self.app.write('')
        
      elif str(type(target)) == "<class 'character.Human'>" or str(type(target)) == "<class 'character.Skeleton'>":
        self.attack += 0.1
        self.app.write(f'{self.name} gained a small permanent attack boost.')
        self.app.write('')
      
      # If their exp is above 100, level them up
      if self.exp >= 100:
        self.level += 1
        self.exp -= 100
        
        # Stat boost
        self.max_health = int(self.max_health * 1.02)
        self.health = int(self.health * 1.02)
        self.attack *= 1.02
        self.defense *= 1.02
        self.resistance *= 1.02
        
        self.app.write(f'{self.name} has levelled up to level {self.level}. Their stats have been increased')
        self.app.write('')
        
      return True # Target has been killed      
    else:
      return False # Target was not killed

  # Function for calculating how much damage the attack actually did based on the
  # attack of the character and the defence of the target
  # Returns if a player was killed or not (T/F)
  def defend_attack(self, att_damage):
    ''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
    a parameter. Returns True is character dies, False if still alive.'''
    
    # defend roll
    roll = random.randint(10, 15)
    block = int(roll * self.defense_mod * self.defense * self.temp_defense)
    
    block = int((block/att_damage) * 100)
    if block > 75:
      block = 0.75
    else:
      block /= 100
        
    # Roll for block - must roll a 20 (5% chance)
    block_roll = random.randint(1, 20)
    if block_roll == 10:
      # Print who blocked to let the player know
      self.app.write(self.name + " successfully blocks the attack!")
      # If a prefect block is achieved set the block amount equal to the attack amount (so the damage taken is 0)
      block = 0
      # Pause for 1 second
      time.sleep(1)

    # Calculate damage from attack
    damage = int(att_damage * block)
    # Prevent negative damage
    if damage < 0:
      damage = 0

    # If character has a shield, shield is depleted, not health
    if self.shield > 0:
      # Shield absorbs all damage if shield is greater than damage
      if damage <= self.shield:
        # Print who shielded against how much damage and pause for 1 second
        self.app.write(self.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        # Reduce shield's health by damage
        self.shield = self.shield - damage
        # Reset damage to 0
        damage = 0
        
      # Otherwise some damage will be sustained and shield will be depleted
      elif damage != 0:
        # Print who shielded against how much damage and that the shield broke and pause for 1 second
        self.app.write(self.name + "'s shield absorbs " + str(self.shield) + " damage.")
        self.app.write(self.name + "'s shield shatters ")
        time.sleep(1)
        # Reduce the damage by the amount the shield blocked
        damage = damage - self.shield
        # Character's shield is removed
        self.shield = 0
      
    # -- Reduce health -- #
    # Print how much health was lost by who
    self.app.write(self.name + " suffers " + str(damage) + " damage!")
    # Take away the appropriate amount of health
    self.health = self.health - damage
    # Pause for 1 second
    time.sleep(1)
      
    # Check to see if dead or not
    if self.health <= 0:
      self.health = 0
      # Print who was killed and pause for 1 second
      self.app.write(self.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True # Character has been killed
    else:
      # Print who lives and with how much health and pause for 1 second
      self.app.write(self.name + " has " + str(self.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False # Character is still alive

# -- Character Magic Actions -- #

  # Function that checks if a character can cast a spell
  def valid_spell(self, choice): # Argument - Character's spell choice
    ''' Checks to see if the spell being cast is a valid spell i.e. can be cast by
    that race and the character has enough mana '''

    # Resetting the value to false before checks
    valid = False

    # Determine this character's race
    # This is a built-in property we can use to work out the
    # class name of the object (i.e. their race)
    race = self.__class__.__name__
    
    # Everyone can cast a shield
    # Only the wizard can cast the other 2 spells
    # Add some more interesting spells later that other races can cast
    if choice == 1:
      if race == "Wizard" and self.mana >= 10:
        valid = True
    elif choice == 2 and self.mana >= 20:
      valid = True
    elif choice == 3:
      if race == "Wizard":
        valid = True
        
    # Return whether or not that race can cast that spell
    return valid 
  
  # Function that checks if a character can use a potion
  def valid_potion(self, choice):
    
    valid = False
    
    # Creating a list of valid choices
    valid_choices = [0]
    
    choice_number = 1
    for potion in self.potions:
      valid_choices.append(choice_number)
      choice_number += 1

    # Checking if the choice is valid
    if int(choice) in valid_choices:
      valid = True
      
    return valid

  # Actually casting said spell
  def cast_spell(self, choice, target=False):
    ''' Casts the spell chosen by the character. Requires 2 parameters - the spell
    being cast and the target of the spell. '''

    # Resetting the value to false before checks
    kill = False

    if choice == 1:
      # Kill will be true or false based on the fuction called, in this case cast_fireball
      kill = self.cast_fireball(target)
    elif choice == 2:
      # Kill will always be false, but a shield will be deployed if the character has enough mana
      self.cast_shield()
    elif choice == 3:
      # Kill will always be false, but the targets mana will be drained
      self.cast_mana_drain(target)
    else:
      # If the character can't cast that spell, print that it's invaild
      self.app.write("Invalid spell choice. Spell failed!")
      self.app.write("")

    return kill # Was the target killed

  # Calculations for the fireball spell
  def cast_fireball(self, target):
    # Reduce charatcer mana
    self.mana -= 10
    # Print who casted the spell at who and pause for 1 second
    self.app.write(self.name + " casts Fireball on " + target.name + "!")
    time.sleep(1)
      
    # Randomising the spell's damage  
    roll = random.randint(1, 10)
    defense_roll = random.randint(1, 10)
    # Base damage calculation
    damage = int(roll * self.magic) - int(defense_roll * target.resistance)
    if damage < 0:
      damage = 0
      
    # Calculating shield damage
    if target.shield > 0:
      # Shield absorbs all damage if shield is greater than damage
      if damage <= target.shield:
        # Print who shielded against how much damage and pause for 1 second
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        # Reduce shield health
        target.shield = target.shield - damage
        # Reset damage
        damage = 0
        
      # Otherwise some damage will be sustained and shield will be depleted
      elif damage != 0:
         # Print who shielded against how much damage and that the shield broke then pause for 1 second
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        self.app.write(target.name + "'s shield shatters")
        time.sleep(1)
        # Reduce the damage by the amount the shield blocked
        damage = damage - target.shield
        # Break the shield
        target.shield = 0
        
    # Print who takes what amount damage and pause for 1 second  
    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(1)
    # Reduce the target's health by the damage
    target.health = target.health - damage
      
    # Check to see if the target is dead or not
    # If so
    if target.health <= 0:
      target.health = 0
      # Print who died and pause for 1 second
      self.app.write(target.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True # Target has been killed

    # If not
    else:
      # Print how much health the target has left and pause for 1 second
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False # Target is still alive

  # Character casts a shield
  def cast_shield(self):
    # Reduce mana
    self.mana -= 20
    # Print who casted the shield and pause for 1 second
    self.app.write(self.name + " casts Shield!")
    time.sleep(1)
    
    # If they already have a shield but it is less than full or if they have no shield
    if self.shield <= self.max_shield:
      # Replenish the shield
      self.shield = self.max_shield
      
    # Print who is now shielded from how much damage and pause for 1 second
    self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
    self.app.write("")
    time.sleep(1)

  # Character casts the mana drain spell (calculations)
  def cast_mana_drain(self, target):
    # Print who casts the spell on who and pause for 1 second
    self.app.write(self.name + " casts Mana Drain on " + target.name + "!")
    time.sleep(1)

    # If the target has more than the max about of mana drained by the spell
    if target.mana >= 20:
      # Drain the max (20 mana)
      drain = 20
    else:
      # Drain whatever they have left
      drain = target.mana
    
    # Print who drains (n) mana from who and pause for 1 second
    self.app.write(self.name + " drains " + str(drain) + " mana from "+ target.name + ".")
    time.sleep(1)
      
    # Reduce target's mana
    target.mana -= drain
    # Increase character's mana
    self.mana += drain
    
    # If the target has no mana left
    if target.mana <= 0:
      target.mana = 0
      # Print that the target is out of mana
      self.app.write(target.name + "'s mana has been exhausted!")
    else:
      # Print how much mana the target has left
      self.app.write(target.name + " has " + str(target.mana) + " mana left")
    self.app.write("")

  # A defense boost ability for the Ork class
  def defense_boost(self):
    
    self.app.write(f"You chose to boost your defense")
    self.app.write(f"Your defense increased by 10% for the battle")
    self.app.write(f"")
    
    self.temp_defense *= 1.1

  # If the slime has been attacked you can have a massive attack bonus (Slime ability)
  def angry_slime(self):
    
    if self.health == self.max_health:
      self.app.write("You stop being passive and pull out the big guns!")
      self.app.write("Your attack increased by 50% for the battle")
      self.app.write("")
      
      self.temp_attack *= 1.5
    else:
      self.app.write("Your enemy has done nothing to you yet, you can't be mad them.")

# -- Character Item Actions -- #

  # Charatcer uses a potion (currently only a health potion is avalible)
  def use_potion(self, choice):
    
    if choice == 'health':
      self.use_health_potion()
    elif choice == 'attack':
      self.use_attack_potion()
    else:
      self.app.write("Invalid potion choice. No potion was drunk!")
  
# Use health potion to heal
  def use_health_potion(self):
    """
    Uses a health potion if the player has one. Returns True if has potion,
    false if hasn't
    """
    # If the character has a potion, take away one potion and replenish health
    if 'health' in self.potions:
      self.potions.pop(self.potions.index('health'))
      self.health += 100
      # If the character's health goes over their max health, set their health to their max
      if self.health > self.max_health:
        self.health = self.max_health
      
      # Print who used a potion and pause for 1 second
      self.app.write(self.name + " uses a Health potion!")
      time.sleep(1)
      # Print character's name and health and pause for 1 second
      self.app.write(self.name + " has " + str(self.health) + " hit points.")
      self.app.write("")
      time.sleep(1)
      return True # Character had a potion to use
    else:
      # Print that the character has no potions left
      self.app.write("You have no potions left!")
      self.app.write("")
      return False # Character did not have a potion to use

# Use attack potion to boost attack
  def use_attack_potion(self):
    """
    Uses an attack potion if the player has one. Returns True if has potion,
    false if hasn't
    """
    # If the character has a potion, take away one potion and increase attack
    if 'attack' in self.potions:
      self.potions.pop(self.potions.index('attack'))
      # 10% attack bonus
      self.temp_attack *= 1.1
      
      # Print who used a potion and pause for 1 second
      self.app.write(self.name + " uses an Attack potion!")
      time.sleep(1)
      # Print character's name and health and pause for 1 second
      self.app.write(self.name + " increased their attack by 10 percent.")
      self.app.write("")
      time.sleep(1)
      return True # Character had a potion to use
    else:
      # Print that the character has no potions left
      self.app.write("You have no potions left!")
      self.app.write("")
      return False # Character did not have a potion to use

# -- Miscellaneous Character Actions -- #

  # Resets a character back to their inital state
  def reset(self):
    ''' Resets the character to its initial state '''
    
    self.health = self.max_health
    self.mana = self.max_mana
    self.temp_attack = 1
    self.temp_defense = 1
    self.shield = 0
    
    # Not resetting the exp values so they can passed on through multiple battles
    
  # Prints all the information about a character
  def print_status(self):
    ''' Prints the current status of the character '''
    # Prints character name and pause for 0.5 seconds
    self.app.write(self.name + "'s Status:")
    time.sleep(0.5)
    
    # Sets up and prints a health bar
    health_bar = "Health: "
    health_bar += "|"
    i = 0
    # Adds '#' or ' ' to represent 25 health points each
    # Prints until the bar is as long as the character's health bar should be
    while i <= self.max_health:
      if i <= self.health:
        # Represents health
        health_bar += "#"
      else:
        # Represents no health
        health_bar += " "
      # Steps in 25 health points
      i += 25
    
    # Putting the bar together with a number and % then printing it then pause for 0.5 seconds
    health_bar += "| " + str(self.health) + " hp (" + str(int(self.health*100/self.max_health)) +"%)"
    self.app.write(health_bar)
    time.sleep(0.5)
    
    # Sets up and prints a experience bar
    exp_bar = "Exp: "
    exp_bar += "|"
    i = 0
    # Adds '#' or ' ' to represent 10 exp points each
    # Prints until the bar is as long as the character's exp bar should be
    while i <= 100:
      if self.exp == 0:
        exp_bar += ' '
      elif i <= self.exp:
        # Represents exp
        exp_bar += "#"
      else:
        # Represents no exp
        exp_bar += " "
      # Steps in 10 exp points
      i += 10
    
    # Putting the bar together with a number and % then printing it then pause for 0.5 seconds
    exp_bar += "| " + str(self.exp) + f" exp ({str(self.exp)})"
    self.app.write(exp_bar)
    time.sleep(0.5)
        
    # If the character has mana, print the mana bar using the same steps
    if self.max_mana > 0:
      # Sets up and prints a mana bar
      mana_bar = "Mana: "
      mana_bar += "|"
      i = 0
      # Adds '#' or ' ' to represent 10 mana points each
      # Prints until the bar is as long as the character's mana bar should be
      while i <= self.max_mana:
        if i <= self.mana:
          # Represents mana
          mana_bar += "*"
        else:
          # Represents no mana
          mana_bar += " "
        i += 10
        # Steps in 10 mana points
        
      # Putting the bar together with a number and % then printing it then pause for 0.5 seconds
      mana_bar += "| " + str(self.mana) + " mp (" + str(int(self.mana*100/self.max_mana)) +"%)"
      self.app.write(mana_bar)
      time.sleep(0.5)
   
    # If the character has a  shield, print the shield bar using the same steps
    if self.shield > 0:
      # Sets up and prints a shield bar
      shield_bar = "Shield: "
      shield_bar += "|"
      i = 0
      # Adds '#' or ' ' to represent 10 shield points each
      # Prints until the bar is as long as the character's shield bar should be
      while i <= 100:
        if i <= self.shield:
          # Represents shield
          shield_bar += "o"
        else:
          # Represents no shield
          shield_bar += " "
        i += 10
        # Steps in 10 mana points
        
      # Putting the bar together with a number and % then printing it then pause for 0.5 seconds
      shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield*100/self.max_shield)) +"%)"
      self.app.write(shield_bar)
      time.sleep(0.5)   
      
    # Printing player level
    self.app.write(f"Level: {str(self.level)}")
    time.sleep(0.5)
    
    # Printing player gold
    self.app.write(f"Gold: {str(self.gold)}")
    time.sleep(0.5)
    
    # Print how many potions the character has remaining and pause for 0.5 seconds
    self.app.write("Potions remaining: " + ', '.join(self.potions))
    self.app.write("")
    time.sleep(0.5)

#---------------------------------------------------------------------#
# Define the attributes specific to each of the Character Subclasses. #
# This identifies the differences between each race.                  #
#---------------------------------------------------------------------#

# The Dwarf class inherits from the Character class which acts as a default character template to be built upon
class Dwarf(Character): 
  '''Defines the attributes of a Dwarf in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Dwarf class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Dwarf specific values
    self.max_health = 300
    self.max_mana = 30
    self.starting_potions = ['health', 'attack']
    self.attack = 100
    self.defense = 6
    self.magic = 4
    self.resistance = 5
    self.speed = 5
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 22
    self.gold_reward = 20

  # What the Dwarf AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Dwarf class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # If health is low set become defensive and cast a shield
      if self.health <= 100:
        self.set_stance('d')
        if self.shield == 0 and self.mana >= 20:
          self.cast_spell(2)
      # If health is high use attack potion
      elif self.health >= 250 and 'attack' in self.potions:
        self.set_stance('d')
        self.use_attack_potion()
      # Attack the player and return whether or not the player was killed
      else:
        self.set_stance('a')
        return self.attack_enemy(player)
    
    return False # Move has not been completed
   
# The Elf class inherits from the Character class which acts as a default character template to be built upon 
class Elf(Character):
  '''Defines the attributes of an Elf in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Elf class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Elf specific values
    self.max_health = 300
    self.max_mana = 60
    self.starting_potions = ['health']
    self.attack = 6
    self.defense = 8
    self.magic = 8
    self.resistance = 8
    self.speed = 8
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 20
    self.gold_reward = 20

  # What the Elf AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Elf class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # Defence stance
      self.set_stance('d')
      
      # If the Elf does not have a shield and has enough mana, cast a shield
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        # Otherwise attack the player
        return self.attack_enemy(player)
      
    return False # Move has not been completed

# The Goblin class inherits from the Character class which acts as a default character template to be built upon
class Goblin(Character):
  '''Defines the attributes of a Goblin in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Goblin class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Goblin specific values
    self.max_health = 100
    self.max_mana = 0
    self.starting_potions = []
    self.attack = 3
    self.defense = 3
    self.magic = 0
    self.resistance = 0
    self.speed = 6
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 6
    self.gold_reward = 7

  # What the Goblin AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Goblin class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # Defence stance
      self.set_stance('d')
      # Attack the player
      return self.attack_enemy(player)
    
    return False # Move has not been completed

# The Hobbit class inherits from the Character class which acts as a default character template to be built upon
class Hobbit(Character):
  '''Defines the attributes of a Hobbit in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Hobbit class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Hobbit specific values
    self.max_health = 250
    self.max_mana = 40
    self.starting_potions = ['health', 'health']
    self.attack = 3
    self.defense = 9
    self.magic = 6
    self.resistance = 10
    self.speed = 5
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 16
    self.gold_reward = 12

  # What the Hobbit AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Hobbit class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # Defence stance
      self.set_stance('d')
      # If the Hobbit does not have a shield and has enough mana, cast a shield
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        # Otherwise attack the player
        return self.attack_enemy(player)
      
    return False # Move has not been completed

# The Human class inherits from the Character class which acts as a default character template to be built upon
class Human(Character):
  '''Defines the attributes of a Human in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Human class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Human specific values
    self.max_health = 250
    self.max_mana = 40
    self.starting_potions = ['health', 'attack']
    self.attack = 7
    self.defense = 8
    self.magic = 5
    self.resistance = 4
    self.speed = 6
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 24
    self.gold_reward = 22

  # What the Human AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Human class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # If health above 75%: Attack stance
      if self.health*100 / self.max_health > 75:
        self.set_stance('a')
      # If health above 30% and below 76%: Balanced stance
      elif self.health*100 / self.max_health > 30:
        self.set_stance('b')
      # If health below or at 30%: Defence stance
      else:
        self.set_stance('d')
        
      # If the Human does not have a shield and has enough mana, cast a shield
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      # Otherwise use an attack potion
      elif 'attack' in self.potions:
          self.use_attack_potion()
      else:
        # Otherwise attack the player
        return self.attack_enemy(player)
      
    return False # Move has not been completed

# The Orc class inherits from the Character class which acts as a default character template to be built upon
class Orc(Character):
  '''Defines the attributes of an Orc in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Orc class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Orc specific values
    self.max_health = 250
    self.max_mana = 0
    self.starting_potions = []
    self.attack = 7
    self.defense = 5
    self.magic = 2
    self.resistance = 4
    self.speed = 4
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 16
    self.gold_reward = 12

  # What the Orc AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Orc class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # Balanced stance
      self.set_stance('b')
      # Attack the player
      return self.attack_enemy(player)
    
    return False # Move has not been completed

# The Uruk class inherits from the Character class which acts as a default character template to be built upon
class Uruk(Character):
  '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Uruk class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Uruk specific values
    self.max_health = 400
    self.max_mana = 20
    self.starting_potions = ['health']
    self.attack = 9
    self.defense = 7
    self.magic = 4
    self.resistance = 6
    self.speed = 2
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 24
    self.gold_reward = 25

  # What the Uruk AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Uruk class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # Attack stance
      self.set_stance('d')
      # Attack the player
      return self.attack_enemy(player)
    
    return False # Move has not been completed

# The Wizard class inherits from the Character class which acts as a default character template to be built upon
class Wizard(Character):
  '''Defines the attributes of a Wizard in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Wizard class
  def __init__(self, char_name, app):
    
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Wizard specific values
    self.max_health = 150
    self.max_mana = 100
    self.starting_potions = ['health', 'health']
    self.attack = 5
    self.defense = 6
    self.magic = 10
    self.resistance = 10
    self.speed = 3
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 18
    self.gold_reward = 20

  # What the Wizard AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Wizard class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      # Defence stance
      self.set_stance('d')
      
      # If the Wizard has less than 10 mana and the player has more than 0 mana, try to drain the player's mana
      if self.mana < 10 and player.mana > 0:
        self.cast_spell(3, player)
      
      # If the Wizard has no shield and has enough mana, cast a shield
      elif self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
        
      # If neither of those and Wizard's mana is above 10, cast a fireball at the player
      elif self.mana >= 10:
        return self.cast_spell(1, player)
      
      # Otherwise attack the player
      else:
        return self.attack_enemy(player)
      
    return False # Move has not been completed
  
# The Skeleton class inherits from the Character class which acts as a default character template to be built upon
class Skeleton(Character):
    
  def __init__(self, char_name, app):
  
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Skeleton specific values
    self.max_health = 75
    self.max_mana = 50
    self.starting_potions = ['attack']
    self.attack = 10
    self.defense = 3
    self.magic = 10
    self.resistance = 10
    self.speed = 9
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 6
    self.gold_reward = 7
    
  # What the Skeleton AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Skeleton class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
      
      if 'attack' in self.potions:
        # Defence stance
        self.set_stance('d')
        # Use attack potion
        self.use_attack_potion()
      else: 
        # Attack stance
        self.set_stance('a')
        # Attack the player
        return self.attack_enemy(player)
    
    return False # Move has not been completed

# The Slime class inherits from the Character class which acts as a default character template to be built upon  
class Slime(Character):
    
  def __init__(self, char_name, app):
  
    # Initialising the Character class traits
    Character.__init__(self, char_name, app)
    
    # Setting up the Slime specific values
    self.max_health = 100
    self.max_mana = 10
    self.starting_potions = []
    self.attack = 4
    self.defense = 5
    self.magic = 10
    self.resistance = 10
    self.speed = 2
    self.health = self.max_health
    self.mana = self.max_mana
    self.potions = self.starting_potions
    self.exp_reward = 6
    self.gold_reward = 7
    
  # What the Slime AI will do on its turn
  def move(self, player):
    """ Defines the AI for the Slime class """
    
    # Tries to run the default move from in the Character class
    move_complete = Character.move(self, player)
    
    if not move_complete:
  
        # Only attacks the player if it was attacked first
        if self.health < self.max_health:
          
          self.set_stance('d')
          # Attack the player
          return self.attack_enemy(player)
        else:
          
          self.app.write(f'{self.name} sits passively')
          self.app.write('')
          time.sleep(0.5)
    
    return False # Move has not been completed
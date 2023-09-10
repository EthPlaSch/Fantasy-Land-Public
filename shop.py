from random import randint
import map_management

class Shop:

  def __init__(self, app, player, enemies, player_pos, enemny_pos, battles, kills, wins):
      
      self.player = player
      self.enemies = enemies
      self.app = app
      self.battles = battles
      self.kills = kills
      self.wins = wins
      # Used to keep player position consistent before and after using the shop
      self.player_pos = player_pos
      self.enemny_pos = enemny_pos
      self.items = [('Attack Potion', 20), ('Health Potion', 20), ('Permanent Defense boost', 50), ('Permanent Attack boost', 50), ('Permanent Health boost', 50), ('Permanent Mana boost', 50)]
      self.app.write(self.player.gold)
    
  def apply_item(self, item):
      
      if item == 'Attack Potion':
          self.player.potions.append('attack')
          self.app.write('You gained an Attack potion')
          self.app.write('')
      elif item == 'Health Potion':          
          self.player.potions.append('health')
          self.app.write('You gained a Health potion')
          self.app.write('')
      elif item == 'Permanent Defense boost':
          self.player.defense *= 1.1
          self.app.write('You gained an small defense boost')
          self.app.write('')
      elif item == 'Permanent Attack boost':
          self.player.attack *= 1.1
          self.app.write('You gained an small attack boost')
          self.app.write('')
      elif item == 'Permanent Health boost':
          self.player.max_health += 20
          self.app.write('You gained an small health boost')
          self.app.write('')
      elif item == 'Permanent Mana boost':
          self.player.max_mana += 10
          self.app.write('You gained an small mana boost')
          self.app.write('')
      
  def purchase(self, item, for_sale):
      
    if self.player.gold >= for_sale[item][1]:
        self.player.gold -= for_sale[item][1]
        self.app.write(f'You bought the {for_sale[item][0]}. It cost {for_sale[item][1]}')
        self.app.write(f'You have {self.player.gold} gold left.')
        self.app.write("")
        self.apply_item(for_sale[item][0])
        for_sale.pop(item)
        
        self.app.write("For Sale:")  
        self.app.write("") 
        
        for i in range(len(for_sale)):
            self.app.write(f"{i + 1}. {for_sale[i][0]}, Price: {for_sale[i][1]}")
        self.app.write("")   
        
    else:
        self.app.write(f'You do not have enough gold, you have {self.player.gold} gold left.')
        self.app.write("") 
        
        self.app.write("For Sale:")  
        self.app.write("")  
        
        for i in range(len(for_sale)):
            self.app.write(f"{i + 1}. {for_sale[i][0]}, Price: {for_sale[i][1]}")
        self.app.write("")    
         
        self.player_options(for_sale)
                        
  def run_shop(self):
  
    self.app.write("Welcome to the shop!")  
    self.app.write("")  
    self.app.write("You can exit the shop at any time by typing in 'back'")
    self.app.write("")

    self.app.write(f"Your Gold: {self.player.gold}") 
    self.app.write("") 
    
    self.app.write("For Sale:")  
    self.app.write("")  
    
    for_sale = []
    
    for i in range(3):
        item = randint(0,5)
        for_sale.append(self.items[item])
        self.app.write(f"{i + 1}. {self.items[item][0]}, Price: {self.items[item][1]}")  
    
    self.app.write("")
        
    self.player_options(for_sale)
    
  def player_options(self, for_sale):  
      
    while for_sale:    

        # App stops until input is recieved
        self.app.wait_variable(self.app.inputVariable)
        # Setting character name to input
        choice = self.app.inputVariable.get()
        
        try:
            # Close window if 'quit' is typed
            if choice == 'quit':
                self.app.quit()
            
            # Player controls
            elif choice == 'back':
                for_sale = False
            elif str(choice) == '1':
                self.purchase((int(choice) - 1), for_sale)
            
            elif str(choice) == '2':           
                self.purchase((int(choice) - 1), for_sale)
                        
            elif str(choice) == '3':           
                self.purchase((int(choice) - 1), for_sale)
                        
            else:
                raise ValueError
            
        except ValueError:
            # Tell the player their choice was not vaild
            self.app.write("You must enter a valid choice")
            self.app.write("")
            # Try again
            choice = self.player_options(for_sale)
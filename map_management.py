# Map Management

from map_file import overworld_map
from random import randint
import shop
import battle
import time
    
class Map:
    
    # Initialising the Map Object
    def __init__(self, player, enemies, app, player_coords, enemny_symbols, battles, wins, kills):
        
        self.app = app
        self.player = player
        self.player_coords = player_coords # (y, x) (row then place along row)
        self.direction = ''
        self.enemies = enemies
        self.battles = battles
        self.wins = wins
        self.kills = kills
        self.enemy_symbols = enemny_symbols
        
        # Stopping enemies spawning every time the shop is opened
        if self.enemy_symbols == []:
            self.enemy_start()
          
    # Dealing with player input          
    def player_movement(self, player_tile):
        
        battled = False
        player_killed = False
            
        # Checking if the player has collided with an enemy
        for enemy in self.enemy_symbols:
            # Working out the distance between the enemy and the player
            difference_x = self.player_coords[1] - enemy[1][1]
            difference_y = self.player_coords[0] - enemy[1][0]
            
            if difference_x == 0 and difference_y == 0:
                
                self.battles = 0
                self.wins = 0
                self.kills = 0
                
                time.sleep(0.5)   
                # Creating the battle, run this when you have collision wiith an enemy
                # From the battle file load a battle between the player and enemy objects
                encounter = battle.Battle(self.player, self.enemies, self.app, player_tile)
                # Calling the .play() method to run the battle
                battle_wins, battle_kills, enemy_turn = encounter.play()
                #shop_window = ''
                # Updating stats for the end screeen
                self.battles += 1
                self.wins += battle_wins
                self.kills += battle_kills
                if enemy_turn == False:
                    player_killed = True
                        
                battled = True
                
                break
         
        # Preventing the direction text from appearing if the player has been killed    
        if player_killed == True or battled == True:
            self.app.write("The battle is over. Press Enter to continue.")
            self.app.write("")
        else:
            self.app.write("")
            self.app.write("Direction (WASD): ")
            self.app.write("")

        
        # Getting Player Input
        self.app.wait_variable(self.app.inputVariable)
        player_action = self.app.inputVariable.get()
        
        # Close window if 'quit' is typed
        if player_action == 'quit':
            self.app.quit()
            
        # Player controls (plus keeping them inside the map)
        elif player_action.lower() == 'w':
            if self.player_coords[0] >= 1:
                self.player_coords[0] -= 1
        elif player_action.lower() == 's':
            if self.player_coords[0] <= 38:
                self.player_coords[0] += 1
        elif player_action.lower() == 'a':
            if self.player_coords[1] >= 1:
                self.player_coords[1] -= 1
        elif player_action.lower() == 'd':
            if self.player_coords[1] <= 58:
                self.player_coords[1] += 1
        elif player_action.lower() == 'e' and player_tile == '$ ':
            shop_window = shop.Shop(self.app, self.player, self.enemies, self.player_coords, self.enemy_symbols, self.battles, self.kills, self.wins)
            shop_window.run_shop()
        
        if battled == False:
            # This causes the loop that makes leaving the map object impossible    
            self.draw_map()
    
    # Setting up the list of enemies and giving them inital positions)
    def enemy_start(self):
        
        for enemy in self.enemies:
            enemy_race = enemy.__class__.__name__
            
            # For every enemy in the list, add their symbol and a random coordinate to a list
            if enemy_race == 'Dwarf':
                self.enemy_symbols.append(['d ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Elf':
                self.enemy_symbols.append(['e ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Goblin':
                self.enemy_symbols.append(['g ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Hobbit':
                self.enemy_symbols.append(['h ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Human':
                self.enemy_symbols.append(['m ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Ork':
                self.enemy_symbols.append(['o ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Uruk':
                self.enemy_symbols.append(['u ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Wizard':
                self.enemy_symbols.append(['w ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Skeleton':
                self.enemy_symbols.append(['s ', [randint(2,37), randint(2,57)]])
            elif enemy_race == 'Slime':
                self.enemy_symbols.append(['b ', [randint(2,37), randint(2,57)]])
    
    # Enemy Movement AI
    def enemy_move(self):
        
        for enemy in self.enemy_symbols:
            
            # Working out the distance between the enemy and the player
            difference_x = self.player_coords[1] - enemy[1][1]
            difference_y = self.player_coords[0] - enemy[1][0]
            
            # If the enemy is more than 7 units from the player, just move randomly
            if (difference_x > 7 or difference_x < -7) or (difference_y > 7 or difference_y < -7):
                enemy[1][1] += randint(-1, 1)
                enemy[1][0] += randint(-1, 1)
                
                # Keeping the enemies on the map
                if enemy[1][1] <= 2:
                    enemy[1][1] = 2
                elif enemy[1][1] >= 57:
                    enemy[1][1] = 57
                    
                if enemy[1][0] <= 2:
                    enemy[1][0] = 2
                elif enemy[1][0] >= 37:
                    enemy[1][0] = 37
            else:
                # If the emeny is close to the player, move towards them
                if difference_x > 0:
                    enemy[1][1] += 1
                elif difference_x < 0:
                    enemy[1][1] -= 1
                    
                if difference_y > 0:
                    enemy[1][0] += 1
                elif difference_y < 0:
                    enemy[1][0] -= 1
                    
    # Drawing the map to the screen
    def draw_map(self):
        
        # Redrawing the table to 'clear' it, so the player doesn't leave a trail when they walk
        table = []
        
        for i in range(len(overworld_map)):
            row = []
            for j in overworld_map[i]:
                row.append(j)
            table.append(row)

        # Changing the tile the player is on to 'x ' so the player can see themselves
        player_tile = table[self.player_coords[0]][self.player_coords[1]]
        table[self.player_coords[0]][self.player_coords[1]] = 'x '
        
        for enemy in self.enemy_symbols:
            table[enemy[1][0]][enemy[1][1]] = enemy[0]

        # Drawing the table
        for row in table:
            self.app.write(''.join(row))
    
        # Running the enemy move, then the player's move
        self.enemy_move() 
        self.player_movement(player_tile) 
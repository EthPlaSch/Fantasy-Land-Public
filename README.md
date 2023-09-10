# Fantasy-Land
This is a turn based, text based, rpg battle engine implemented using Object Oriented Programming using Python. It is themed around generic fantasy.
You should run the rpg.py file to start the game.

How to Play:

0. Run rpg.py to start

1. WASD (then Enter) to move while on the map

2. Press E (then Enter) while on the shop to open it

3. Type 'back' to back out of the shop or 'back out' to back of potion/spell menus

4. Type 'quit' at any time to close the window

5. Hopefully it's possible to work out the rest of the controls

Changes:

1. Gone through and commented all the files (rpg.py, gui.py, character.py, battle.py, and map_management.py) to both understand what I'm working with and make it easier to return to in the future.

2. Added the if __name__ == '__main__': block to tell the reader that the rpg.py file is a script that should be run. The other files don't have this to indicate they are libraries.

3. Added 2 new character classes, the skeleton and the slime (added in character.py). These are just copied existing classes with twweaked individual values and a new move.

4. Added 2 abilities to the game, for the slime: a damage booster if it is not longer at full health (called angry slime), for the Orc: a defence boost ability.

5. Added the option to flee from battle, the player "runs away never to be seen again" and the window closes.

6. Added a handful of new items: Attack potion which funcitons the same as the health potion but temporarily boosts the users attack by 10% for that one battle, then in the shop the player can purchase a permanent health, attack, defence, or mana boost.

7. I adjusted the game balance by tweaking some of character values to make some classes weaker and some stronger, I adjusted the AI for the Dwarf, Human, Skeleton, and Slime class (and probably more I'm forgetting).

8. I added 2 new difficulties to the game: Passive-ish (really easy) and Absurd (nearly impossible), which change how many enemies spawn.

9. I adjusted the game balance by rewriting the damage calculation, the block is now a percentage of the attack capped out at blocking 75% so an overpowered character never takes 0 damage (excluding landing a perfect block).

10. I added a counter attack to the game that has a random chance to land everytime someone is attacked. It deals 1.5 times the damage the original attack was suppose to do and makes the counter-attacker not take any damage.

11. I added experience points to the game, gained when killing another character.

12. I added a level system to the game, every 100 exp gained levels you up. This level up boosts all the character's stats.

13. I added a gold mechanic to the game, gained when killing another character.

14. I added a shop to the game, where the player can spend their gold to buy the items listed above (see addition 6).

15. I added a speed stat to all characters that determines the order of battle (player's speed vs the average speed of the enemies, fastest goes first)

16. I added a map file to keep everything organised. It just contains the game map (which is a list of lists).

17. I added a new file 'map_management.py' that manages the overworld.

18. I added a map/overworld to the game, it is a 60x40 map with a compass in the bottom corner. It can be moved around with WASD. The shop is on the map and can be accessed by pressing E if player is colliding with the shop.

19. I added enemy movement AI. They spawn randomly around the map, each turn they move around randomly unless they are within 7 tiles of the player in which they move directly towards the player.

20. If the player collides with an enemy a battle is initiated.

21. I added terrain penalties, the characters are battling in the volcanic area (represented by 'V' on the map), a burn effect applies and all characters take 10 damage per turn for the duration of the battle.
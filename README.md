# Python-Roguelike
Small roguelike game built with Python and tcod

The game_server and network classes are included, but network functionality is commented out in the client side of the game as it wasn’t fully implemented. More on that below.
Basic Controls:
Movement can be done with arrow keys or WASD for directional movement.
QEZX offer diagonal movement for the player.
Esc opens the main menu, closes all menus, and can be used to cancel targeted spells.
G picks up items off the ground and adds them to the players inventory.
Enter allows the player to use a bonfire to rest and progress to the next level.
C brings up the character statistic menu.
B opens the players spell book and shows which pages are equipped in which slots.
I opens the inventory menu.
M opens the spell menu from which the player can select and use a spell (some require mouse targeting).
Map icons:
Icons that move are enemies. (enemies within view will also have their health bars appear on the right of the screen).
+ icons indicate spellbook pages that can be added to the players spellbook, these come in various colours.
P icons indicate potions that can be picked up. Red and blue potions are for health and mana respectively.
Various symbols are associated with traps or areas that shouldn’t be stepped on. Currently, the user is the only entity that can place traps so these symbols are more to lure monsters onto them than for the player to be wary of (ie. Lightning rune is denoted by a yellow Q, Pillar of Flame is denoted by a red X).
The & indicates a bonfire that can be rested at, and its use will move the player to the next dungeon.


Additions Since Prototype
Scoring: The players score appears in the bottom left of the screen and is added to upon gaining xp, levelling up, and progressing deeper into the dungeon. The idea was to have a leaderboard for online play and to include a high score gain for killing other players but this was not implemented. This would ensure players had a motivation to invade other players worlds to kill them (it would end their ability to gain a higher score on that character, but also gain score for themselves).
The book equipment system now allows the player to equip and transfer different coloured pages into their spellbook which gives them different spell options based on the pages in their book. Spells use a mana system (each have a cost that can be seen on the spell list when the player presses ‘m’). 
The game now has a fully functioning and incredibly modular spell system. It allows for targeting spells, spells that auto target, spells that cause lasting effects, spells that cause traps to appear, etc.
The spell system, status effect system, and trap system are all highly modular and can be combined (traps can cause status effects, spells can cause traps, etc) into interesting combinations. Traps will not hurt their own caster.
Brief Spell List:
Minor Heal – Heals the player 
Fireball – Targeted AoE damage
Pillar of Fire – Targeted trap
Stoneskin – Caster defense boost
Lightning – Untargeted damage to nearby enemies
Lightning Rune – Untargeted trap
Haste – Increases caster movement speed
Gust – Slight damage and moves enemies around the caster
Drain – Damages an enemy and heals the caster for that amount
Vines – Targeted trap that ensnares enemies and prevents movement
Weaken – Drains power from the nearest enemy
The player HUD was also updated to show enemy health bars in the players field of view, as well as their current score and the depth of the dungeon they are currently in. 
Furthermore, another enemy AI was added that allows for enemies to cast spells. It isn’t fully modular (only works with spells hardcoded into the AI) however it changes how the game is played and adds an option for various enemy types that can use the same spells that the player does. Currently, the only enemy that casts spells is the Wizard who uses a lightning spell to attack the player from range.

Network Functionality
The part I sunk the most time in was trying to get the network functionality completely working. The issue that prohibited me from moving forward with this was passing custom python objects through a socket.
Initially I was using pickle to serialize things before sending them through the socket, however pickle wasn’t able to serialize my objects properly (notably the game map and entity objects). I tried switching to a json format but json was even worse at serializing custom objects without writing specific methods for each class in order to serialize and deserialize a string representation of that object. I moved back to pickle after json didn’t work. There is also a jsonpickle module that sort of combines both, but it wasn’t going to be helpful in this case.
The entity class especially posed a problem because not all entities have the same attributes (due to composition) and as such writing a string representation of an entity becomes highly complex. This could partially be remedied by adding an attribute list as an attribute for the entity, and also by using IDs for things like the spell list (so instead of having to serialize a spell, I can pass a string representation of an integer through the socket that can be easily read).
The other solution was to have the above combined with a ‘default’ room for invasions that was stored on the server as well as the clients (so no game map object would have to be passed), and to pass the entities using a complicated string representation of the class. This was too far away from what I wanted to initially accomplish (an actual dark-souls style invasion system) and by the time I came up with this solution it was too late to attempt to implement it. 
The last solution was to save the maps as files (which I tried to do ala shelve, the same module I was using for saving and loading) and then transfer them to the server that way for reading and then build the objects with the map file that was passed. I may try to implement this if I continue to work on the game post-semester.
Balance Note
There is still balancing to be done. The odds of finding specific pages, items, and monsters could all make the experience and difficulty curve better.

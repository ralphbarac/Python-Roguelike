import tcod

def menu(console, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # Calculates the total height for the header and does one line per option
    header_height = tcod.console_get_height_rect(console, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Creates a new console that represents the menu window
    window = tcod.console_new(width, height)

    # Prints the header
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # Prints the options in the menu
    y = header_height
    letter_index = ord('a')
    for option in options:
        text = '(' + chr(letter_index) + ')' + option
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(console, header, player, inventory_width, screen_width, screen_height):
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.book.ele_1 == item:
                options.append('{0} (in book [Elemental 1])'.format(item.name))
            elif player.book.ele_2 == item:
                options.append('{0} (in book [Elemental 2])'.format(item.name))
            elif player.book.life == item:
                options.append('{0} (in book [Life])'.format(item.name))
            elif player.book.vision == item:
                options.append('{0} (in book [Vision]'.format(item.name))
            elif player.book.alt == item:
                options.append('{0} (in book [Alternate]'.format(item.name))
            else:
                options.append(item.name)

    menu(console, header, options, inventory_width, screen_width, screen_height)

def spell_menu(console, header, player, spell_list_width, screen_width, screen_height):
    if len(player.book.get_book_spell_list()) == 0:
        options = ['No spells available.']
    else:
        options = []

        for spell in player.book.spell_list:
            options.append(spell.name + "....." + str(spell.mana_cost))
    
    menu(console, header, options, spell_list_width, screen_width, screen_height)

def main_menu(console, screen_width, screen_height):
    
    tcod.console_set_default_foreground(0, tcod.light_blue)
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, tcod.BKGND_NONE, tcod.CENTER, 'CS 4483 Game')
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), tcod.BKGND_NONE, tcod.CENTER, 'By Ralph Barac')

    menu(console, '', ['New Game', 'Quit'], 24 ,screen_width, screen_height)

def level_up_menu(console, header, player, menu_width, screen_width, screen_height):
    options = ['Health (+10 HP, (currently {0})'.format(player.combat_entity.base_max_hp),
               'Mana (+10 MP (currently {0})'.format(player.combat_entity.base_max_mana),
               'Power (+2 power (currently {0})'.format(player.combat_entity.base_power),
               'Defense (+2 defense (currently {0})'.format(player.combat_entity.base_defense)
    ]

    menu(console, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = tcod.console_new(character_screen_width, character_screen_height)

    tcod.console_set_default_foreground(window, tcod.white)

    tcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Character Information')
    tcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    tcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    tcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Experience to level: {0}'.format(player.level.xp_to_next))
    tcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Maximum HP: {0}'.format(player.combat_entity.max_hp))
    tcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Maximum Mana: {0}'.format(player.combat_entity.max_mana))
    tcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Attack: {0}'.format(player.combat_entity.power))
    tcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Defense: {0}'.format(player.combat_entity.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    tcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def book_screen(player, book_screen_width, book_screen_height, screen_width, screen_height):
    window = tcod.console_new(book_screen_width, book_screen_height)
    
    tcod.console_set_default_foreground(window, tcod.white)

    if player.book.ele_1 is not None:
        ele_1 = player.book.ele_1.name
    else:
        ele_1 = "Empty."
    
    if player.book.ele_2 is not None:
        ele_2 = player.book.ele_2.name
    else:
        ele_2 = "Empty."
    
    if player.book.life is not None:
        life = player.book.life.name
    else:
        life = "Empty."
    
    if player.book.vision is not None:
        vision = player.book.vision.name
    else:
        vision = "Empty."
    
    if player.book.alt is not None:
        alt = player.book.alt.name
    else:
        alt = "Empty."

    tcod.console_print_rect_ex(window, 0, 1, book_screen_width, book_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Currently Equipped Pages')
    tcod.console_print_rect_ex(window, 0, 3, book_screen_width, book_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Elemental 1 Slot: {0}'.format(ele_1))
    tcod.console_print_rect_ex(window, 0, 4, book_screen_width, book_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Elemental 2 Slot: {0}'.format(ele_2))
    tcod.console_print_rect_ex(window, 0, 5, book_screen_width, book_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Life Slot: {0}'.format(life))
    tcod.console_print_rect_ex(window, 0, 6, book_screen_width, book_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Vision Slot: {0}'.format(vision))
    tcod.console_print_rect_ex(window, 0, 7, book_screen_width, book_screen_height, tcod.BKGND_NONE, tcod.LEFT, 'Alternate Slot: {0}'.format(alt))

    x = screen_width // 2 - book_screen_width // 2
    y = screen_height // 2 - book_screen_height // 2
    tcod.console_blit(window, 0, 0, book_screen_width, book_screen_height, 0, x, y, 1.0, 0.7)

def message_box(console, header, width, screen_width, screen_height):
    menu(console, header, [], width, screen_width, screen_height)
#!/usr/bin/python3

async def handle_inventory(player_inventory):
    ''' Perform miscellaneous inventory management actions/cases

        Returns: inventory_actions [(priority, action)]
    '''

    inventory_actions = []
    
    print(player_inventory)

    if not player_inventory:
        return inventory_actions

    # look for non-existence of life potions specifically
    if "life potion" not in player_inventory:
        inventory_actions.append((1, "buy life potion 50"))

    for key in player_inventory.keys():
        if key.endswith("lootbox"):
            inventory_actions.append((2, f"open {key}"))

    return inventory_actions
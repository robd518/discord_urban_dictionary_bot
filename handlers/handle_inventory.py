#!/usr/bin/python3

async def handle_inventory(player_inventory):
    ''' Perform miscellaneous inventory management actions/cases

        Returns: inventory_actions [(priority, action)]
    '''

    inventory_actions = []
    
    print(player_inventory)

    if not player_inventory:
        return inventory_actions

    elif "life potion" not in player_inventory:
        inventory_actions.append((1, "buy life potion 50"))

    elif next(k for k in player_inventory.keys() if k.endswith("lootbox")):
        lootbox = next(k for k in player_inventory.keys() if k.endswith("lootbox"))
        inventory_actions.append((2, f"open {lootbox}"))

    return inventory_actions
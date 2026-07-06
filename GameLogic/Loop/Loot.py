from Systems import PlayerSelect as Select



def loot(players, enemies):    
    # if Select.yesNo("Loot enemies?"):
        bloodVolume = 0

        for enemy in enemies:
            # if enemy.type == "human":
            drop = enemy.inventory
            
        Select.waitPrint(drop)
        # Let player examine inventory and take desired items if they have capacity.


    # returns


# def transfer(fighter, target):
#     distance = Movement.getTargetDistance(fighter, target)

#     if distance == 1:
#         if "Transfer" in fighter.abl["items"]:
#             return
#     # Characters pass items/components
#     return
from Systems import PlayerSelect as Select
from . import Cards


def modifyEnvironment(environment, biome):
    Cards.showEnvironment(environment)    
  
    aces = Cards.setFronts("Aces")
    choice = Cards.pickCard(aces)
    suit = Cards.findSuit(aces[choice][1])

    match suit:
        case "Clubs":
            Select.slowPrint("A new biome gains ascendancy.")
            match environment["Clubs"]:
                case "King": Select.slowPrint("The volcano belches smoke. Warm winds carry its embers.")
                case "Queen": Select.slowPrint("The glacier grinds forward. Bitter cold creeps across the valley.")
                case "Jack": Select.slowPrint("Fog rolls across the fjord. Fey things move silently at the edge of sight.")

        case "Diamonds":
            Select.slowPrint("The flow of magic shifts.")
            match environment["Diamonds"]:
                case "King": Select.slowPrint("Mana dissipates.")
                case "Queen": Select.slowPrint("Mana collapses.")
                case "Jack": Select.slowPrint("Mana surges.")

        case "Hearts":
            Select.slowPrint("The weather changes.")
            match environment["Hearts"]:
                case "King": Select.waitPrint("The rain abates. Water recedes while fog accumulates.")
                case "Queen": Select.waitPrint("The soil dries beneath warm sunlight. Clouds gather on the horizon.")
                case "Jack": Select.slowPrint("Rain falls thick from heavy clouds. Water collects in deep pools.")

        case "Spades":
            Select.slowPrint("An omen reveals changing fortunes.")
            match environment[suit]:
                case "King": Select.slowPrint("The wilds seek blood. Hunger and ambition will find their reward.")
                case "Queen": Select.slowPrint("Old powers recede, making space for younger threats. Meet them.")   
                case "Jack": Select.slowPrint("Forces unfriendly to human life stir from their slumber. Be cautious.")

    match environment[suit]:
        case "King": environment[suit] = "Queen"
        case "Queen": environment[suit] = "Jack"
        case "Jack": environment[suit] = "King"


    # King:
    #   Forces players to retreat from volcano.
    #   Stamina costs doubled for all actions.
    # Queen:
    #   Causes quakes in ice biome. Forces players to retreat.
    #   Players incur a stamina penalty for having extra dice or movement at the end of their turn.
    # Jack:
    #  Fog from the Feywood rolls across the fjord and settles in the deep wild.
    #  Players suffer invigoration penalty per mana level.

    # King:
    #   (element based on club card) Elementals can spawn in secondary biomes. Wisps and secondary beasts can spawn in the deep wild.
    #   2-5 mana wells per map. Alchemy mini game biased towards high cards.
    # Queen:
    #    Beasts from secondary biomes can spawn in the deep wild.
    #    1-3 wells per map. Tracking mini game biased towards high cards.
    # Jack:
    #    0-1 wells per map. Alchemy biased toward low cards.
    #    Deep biomes ignore Jacks. Shallow biomes ignore Kings.

    # King: All rest sites have water. Beast activity declines.
    # Queen: Most rest sites have water. Increase beast activity.
    # Jack: Beast concentration at rest sites with water increases. Beast concentration elsewhere declines.

    # King: Boss encounters possible. Regular encounters harder.
    # Queen: agents of the king / elementals depending on biome
    # Jack: aggressive beasts / small human scouting parties or bandits/trappers/bounty hunters
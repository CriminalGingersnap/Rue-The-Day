from . import Avarice_1, Avarice_2, Benediction_1, Benediction_2
from Systems import Roll, PlayerSelect as Select
from Loop import Cards


def setFoes(biome, budgets, luckCard) -> list:
    Select.waitPrint("Rolling to determine encounter number.")
    Select.quickPrint("First roll:")
    roll1 = Roll.roll(None, None, 1, None, None)

    Select.quickPrint("Second roll:")
    roll2 = Roll.roll(None, None, 1, None, None)

    Select.waitPrint("Applying luck card:")
    Cards.printDeck([luckCard])
    roll2 += Cards.findValue(luckCard)
    Select.waitPrint("Modified second roll: " + str(roll2) + "\n")
    Select.waitPrint("")

    rolls = [roll1, roll2]
    rollNum, groups = 0, [[], []]
    
    for roll in rolls:
        budget = budgets[rollNum]
        members = []
        match biome:
            case "Wildlands Pass": members = Avarice_1.passEncounters(roll, budget)
            case "Wildlands Bay": members = Avarice_1.bayEncounters(roll, budget)
            case "Ice Fjord": members = Avarice_1.fjordEncounter(roll, budget)
            case "Ice Glacier": members = Avarice_1.glacierEncounters(roll, budget)
            case "Dreamwood Periphery": members = Avarice_1.peripheryEncounters(roll, budget)
            case "Dreamwood Depths": members = Avarice_1.depthsEncounters(roll, budget)
            case "Flame Peninsula": members = Avarice_1.peninsulaEncounters(roll, budget)
            case "Flame Volcano": members = Avarice_1.volcanoEncounters(roll, budget)

            case "Kingdom Fort": members = Avarice_2.strongholdEncounters(roll, rollNum, "Fort", budget)
            case "Kingdom Road": members = Avarice_2.strongholdEncounters(roll, rollNum, "Road", budget)
            case "Marshland": members = Avarice_2.marshEncounters(roll, budget)
            case "Outlaw Camp": members = Avarice_2.strongholdEncounters(roll, rollNum, "Camp", budget)
            case "Outlaw Range": members = Avarice_2.strongholdEncounters(roll, rollNum, "Range", budget)
            case "Unsettled Lands": members = Avarice_2.unsettledEncounters(roll, budget)

            case "Dream Sea-Cave": members = Benediction_1.seaCaveEncounters(roll, budget)
            case "Holy Scrubland": members = Benediction_1.scrublandEncounters(roll, budget)
            case "Holy Desert": members = Benediction_1.desertEncounters(roll, budget)
            case "Rot Encroachment": members = Benediction_1.encroachmentEncounter(roll, budget)
            case "Rot Locus": members = Benediction_1.locusEncounter(roll, budget)
            case "Shoreline Dunes": members = Benediction_1.duneEncounters(roll, budget)

            case "Flame Lowland": members = Benediction_2.lowlandEncounters(roll, budget)
            case "Ice Highland": members = Benediction_2.highlandEncounters(roll, budget)
            # case "Ice Peak": members = Benediction_2.peakEncounters(roll, budget)
            case "Marsh Depths": members = Benediction_2.depthsEncounters(roll, budget)
            case "Shoreline Nest": members = Benediction_2.nestEncounters(roll, budget)

        memberIndex = 1
        for member in members:
            member.props["name"] += "[" + str(rollNum) + str(memberIndex) + "]"
            member.props["initials"] = str(rollNum) + str(memberIndex)
            memberIndex += 1

        for member in members:
            if "echo" in member.inv:
                if memberIndex <= 9:
                    echo = member.inv["echo"]
                    if (echo != "None"):
                        echo.props["name"] += "[" + str(rollNum) + str(memberIndex) + "]"
                        echo.props["initials"] = str(rollNum) + str(memberIndex)
                        memberIndex += 1
                else: member.inv["echo"] = "None"

        groups[rollNum] = members
        rollNum += 1

    return groups
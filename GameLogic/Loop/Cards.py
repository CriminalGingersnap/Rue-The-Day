from Systems import PlayerSelect as Select
import random

club, heart, diamond, spade = "\u2663", "\u2665", "\u2666", "\u2660"


def setBody(value, suit) -> list:
    top, sides, bottom = [" _________ "], ["|         |"], ["|_________|"]
    card = top + sides + sides + sides + sides + sides + bottom
    card[3] = "|    " + value + "    |"
    card[1], card[5]= "| " + suit + "       |", "|       " + suit + " |"

    return card

def setFronts(type) -> list:
    deck = []

    for suit in [club, heart, diamond, spade]:
        match type:
            case "Aces":
                deck += [setBody("A", suit)]
            case "Numbers":
                for number in range(2, 10):
                    deck += [setBody(str(number), suit)]
                deck = deck[:12]

    random.shuffle(deck)
    return deck

def setBacks(length) -> list:
    backs, cardBack = [], setBody(" ", "?")
    for i in range(length): backs += [cardBack]

    return backs


def showEnvironment(faceCards):
    Select.waitPrint("\nCurrent Environment:")
    Select.waitPrint("| Density |   | Weather |   | Mana    |   | Threat  |")

    clubFace = setBody(faceCards["Clubs"][0], club)
    heartFace = setBody(faceCards["Hearts"][0], heart)
    diamondFace = setBody(faceCards["Diamonds"][0], diamond)
    spadeFace = setBody(faceCards["Spades"][0], spade)

    deck = [clubFace, heartFace, diamondFace, spadeFace]
    printDeck(deck)


def printDeck(deck):
    row, rowCount = 0, int(len(deck) / 4)
    excess = (len(deck) % 4)

    while row <= rowCount:
        cardNum, rowOffset = 4, 4 * row
        if row == rowCount: cardNum = excess

        if cardNum > 0:
            for line in range(7):
                for cardIndex in range(cardNum):
                    print(deck[cardIndex + rowOffset][line], end="   ")
                print()
            print()
        
        row += 1


def pickCard(hand, picks) -> list:
    drawn, backs = [], setBacks(len(hand))
    printDeck(backs)

    for pick in range(picks):
        Select.waitPrint("\nChoose a card(1-" + str(len(hand)) + "):")
        
        while True:
            answer = int(Select.takeInput(1, len(hand))) - 1
            if answer not in drawn:
                backs[answer] = hand[answer]
                drawn += [answer]
                printDeck(backs)
                break
            else: Select.waitPrint("Please select a new card.")

    return drawn


def findSuit(line) -> str:
    if club in line: return "Clubs"
    elif diamond in line: return "Diamonds"
    elif heart in line: return "Hearts"
    elif spade in line: return "Spades"

def findValue(line) -> str:
    if "2" in line: return 2
    elif "3" in line: return 3
    elif "4" in line: return 4
    elif "5" in line: return 5
    elif "6" in line: return 6
    elif "7" in line: return 7
    elif "8" in line: return 8
    elif "9" in line: return 9
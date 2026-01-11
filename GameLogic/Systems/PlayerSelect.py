import time, random, copy
# from GameUI.GameWindow import keyPressed

waitTime = .3

# make a fast print option for large blocks of text. let the player choose before it starts.
def slowPrint(text):
    for i in text:
        print(i, end='')
        time.sleep(.07)
    time.sleep(waitTime)
    print()


def readScene(phraseList) -> None:
    for phrase in phraseList:
        print(phrase[0], end='')
        conversationPrint(phrase[1])

    input("Press Enter to continue.")

def conversationPrint(text):
    for i in text:
        print(i, end='')
        time.sleep(.06)
        if i in [".", ",", "?", "!", ">"]: time.sleep(.2)
        elif i == ":": time.sleep(.5)
    time.sleep(waitTime)
    print()


def waitPrint(text):
    time.sleep(waitTime)
    print(text)
    time.sleep(waitTime)


def targetSelect(targets) -> int:
    if len(targets) == 1: return targets[0]
    else:
        targetNames = []

        for target in targets:
            targetNames += [target.name]
        
        waitPrint("Choose Target:")
        name = makeSelection(targetNames)

        for target in targets:
            if target.name == name: return target

def makeSelection(options) -> int:
    for option in options:
        print(str(options.index(option)+1) + ": " + str(option))

    selection = takeInput(1, len(options))
    print()
    return options[selection - 1]

def yesNo(prompt) -> bool:
    waitPrint(prompt)
    answer = makeSelection(["Yes", "No"])
    if answer == "Yes": return True
    else: return False
    

def takeInput(floor, ceiling):
    if floor == ceiling:
        print("Value defaults to " + floor + ".")
        return floor
    else:
        while True:
            try:
                answer = int(input("-> "))
                if floor <= answer <= ceiling: return answer
                else: raise ValueError
            except ValueError:
                if ceiling == (floor + 1): print("Enter either " + str(floor) + " or " + str(ceiling) + ".")
                else: print("Enter a number between " + str(floor) + " and ", str(ceiling) + ".")
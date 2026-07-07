import time

waitTime = .3

# make a fast print option for large blocks of text. let the player choose before it starts.
def slowPrint(text):
    for i in text:
        quickPrint(i, '')
        time.sleep(.07)
    time.sleep(waitTime)
    quickPrint('', '')


def readScene(phraseList) -> None:
    for phrase in phraseList:
        quickPrint(phrase[0], '')
        conversationPrint(phrase[1])

    input("Press Enter to continue.")

def conversationPrint(text):
    for i in text:
        quickPrint(i, '')
        time.sleep(.06)
        if i in [".", ",", "?", "!", ">"]: time.sleep(.2)
        elif i == ":": time.sleep(.5)
    waitPrint("\n")


def quickPrint(text, ending: str | None = "\n"):
    print(text, end=ending)

def waitPrint(text):
    time.sleep(waitTime)
    quickPrint(text, "\n")
    time.sleep(waitTime)


def targetSelect(targets) -> int:
    targetNames = []
    for target in targets: targetNames += [target.name]
    
    name = pickOption(targetNames, "target")

    for target in targets:
        if target.name == name: return target


def pickOption(options, category) -> str:    
    if len(options) > 1:
        waitPrint("Select " + category + ":")
        return makeSelection(options)
    else:
        waitPrint("Sole option selected automatically: " + category)
        return options[0]

def makeSelection(options) -> str:
    for option in options:
        quickPrint(str(options.index(option)+1) + ": " + str(option))

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
        quickPrint("Value defaults to " + str(floor) + ".")
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


def listSelection(options, cap, prompt):
    ceiling, selection = len(options), []
    waitPrint(prompt)

    if cap == 0: waitPrint("Action skipped. Limit reached.")
    elif ceiling == 0: waitPrint("Action skipped. No options in category.")
    else:
        quickPrint("Enter a comma separated list. Ex: 1,4,9")
        # support ranges. ex 2-4
        
        for option in options:
            quickPrint(str(options.index(option)+1) + ": " + str(option))

        while True:
            try:
                answerList = input("-> ").split(",")
                if len(answerList) > cap: raise SyntaxError
                elif not all((1 <= answer <= ceiling) for answer in answerList): raise ValueError
                else:
                    for answer in answerList: selection += [options[answer - 1]]
            
            except SyntaxError:
                print("Quantity of selected values cannot exceed " + str(cap) + ".")
            except ValueError:
                print("All comma-separated values must be numbers between 1 and ", str(ceiling) + ".")
    
    return selection
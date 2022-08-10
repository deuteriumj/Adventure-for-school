import time
import json

f = open('script.json')
dataFile = json.load(f)
f.close()

currentRoom = "FOREST"
currentDesc = "there's trees around you and a clearing in front of you"
currentMovements = ["FRONTYARD"]
availableItems = []
inventory = []
doLoop = True



def displayIntro():
    print("intro")
    print("intro")
    print("intro")
    print("intro")
    print()

def inventoryUI():
    print("You have:")
    for i in inventory:
        print(i)
    input("Press enter to continue...")

def actionsUI():
    print("Go to ___\nTake ___\nUse ___\nInventory")
    input("Press enter to continue...")


displayIntro()
while True:
    action = input(f"\n(To check the commands type \"actions\")\nYou are in the {currentRoom}\n{currentDesc}\nMovement options:\n{' '.join(currentMovements)}\nAvailable items:\n{' '.join(availableItems)}\n>").upper()

    if action == "INVENTORY":
        inventoryUI()
    elif action == "ACTIONS":
        actionsUI()
    elif "TAKE " in action:
        for i in availableItems:
            if i in action:
                inventory += i
                print(f"You got {i}")
                print(dataFile["places"][currentRoom]["itemDescriptions"][i])
    elif "GO TO " in action:
        for i in currentMovements:
            if i in action:
                currentRoom = i
                    
    currentMovements = dataFile["places"][currentRoom]["connectedPlaces"]
    currentDesc = dataFile["places"][currentRoom]["description"]
    availableItems = dataFile["places"][currentRoom]["items"]

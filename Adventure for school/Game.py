import json
import random

# load the .json file
f = open('script.json')
placeJson = json.load(f)
f.close()
f = open('notebookpages.json')
pageJson = json.load(f)
f.close()

currentRoom = "FOREST"
currentDesc = ""
currentMovements = []
availableItems = []
availableInteractions = []
availableResults = []
inventory = []

# list of items usable anywhere
anywhereInteractions = placeJson["anywhereItems"]

houseOpen = False
hasWon = False

PHONE_PASSWORD = random.randint(100000, 999999)
PHONE_PASSWORDPAGE = str(random.randint(11, 20))

RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
PURPLE = 35
CYAN = 36

def colourtext(colour, text):
    return f'\033[{colour}m{text}\033[0m'

def displayIntro():
    print()
    print("You remember camping with your friends in the forest but it seems foggy and your head hurts.")
    print("You don't know where you are or how you got there.")

def inventoryUI():
    print(f"\nYou have:\n{' '.join(inventory)}")
    input("Press enter to continue...")

def actionsUI():
    print("Go to ___\nTake ___\nUse ___\nInventory")
    input("Press enter to continue...")


displayIntro()
while not hasWon:
    # set the room around the player based on which room they're in
    availableInteractions = placeJson["places"][currentRoom]["availableInteractions"]
    currentMovements = placeJson["places"][currentRoom]["connectedPlaces"]
    currentDesc = placeJson["places"][currentRoom]["description"]
    availableItems = placeJson["places"][currentRoom]["items"]
    availableResults = placeJson["places"][currentRoom]["interactionResults"]

    action = input(f"\n(To check the commands type \"actions\")\nYou are in the {colourtext(GREEN, currentRoom)}\n{currentDesc}\nMovement options:\n{colourtext(BLUE, ' '.join(currentMovements))}\nAvailable items:\n{colourtext(YELLOW, ' '.join(availableItems))}\n>").upper()
    
    if action == "INVENTORY":
        inventoryUI()
    elif action == "ACTIONS":
        actionsUI()

    elif "TAKE " in action:
        # check if the item they wanted to take is available
        for i in availableItems:
            if i in action:
                print(placeJson["places"][currentRoom]["itemDescriptions"][i])
                inventory.append(i)
                print(f"\nYou got {i}")
                placeJson["places"][currentRoom]["items"].remove(i)
                input("Press enter to continue...")

    elif "GO TO " in action:
        # check if the place they wanted to go to is available
        for i in currentMovements:
            if i in action:
                currentRoom = i

    elif "USE " in action:
        # check if the item they wanted to use is available
        for i in availableInteractions:
            if i in action and i in inventory:
                print(availableResults[i])
                # shovel will turn DIRT_PATCH into THE_HOLE and move you into it
                if i == "SHOVEL":
                    placeJson["places"]["FOREST"]["connectedPlaces"].remove("DIRT_PATCH")
                    placeJson["places"]["FOREST"]["connectedPlaces"].append("THE_HOLE")
                    currentRoom = "THE_HOLE"
                
                # STRANGE_KEY will open the chest and give you the HOUSE_KEY
                elif i == "STRANGE_KEY":
                    inventory.append("HOUSE_KEY")
                    print("You got HOUSE_KEY")
                    print(placeJson["places"][currentRoom]["itemDescriptions"]["HOUSE_KEY"])
                    input("Press enter to continue...")
                
                # HOUSE_KEY will open the house
                elif i == "HOUSE_KEY":
                    houseOpen = True

        for i in anywhereInteractions:
            if i in action and i in inventory:
                if i == "PHONE":
                    guess = int(input("Input the password\n>"))
                    if guess != PASSWORD:
                        print("incorrect")
                    else:
                        hasWon = True
                
                elif i == "NOTEBOOK":
                    in_notebook = True
                    while in_notebook:
                        page = input("Choose a page (1-20)\nTo close the notebook type close\n>").lower()
                        if page == "close":
                            in_notebook = False
                        elif page == PASSWORDPAGE:
                            print(f"Phone password:\n{PASSWORD}")
                        elif page in pageJson["pages"]:
                            print(pageJson["pages"][page])
                            input("Press enter to continue...")
                        else:
                            print("The page is blank")


    if currentRoom == "HOUSE":
        if houseOpen is False:
            print("the door is locked")
            currentRoom = "FRONTYARD"
        else:
            currentRoom = "ENTRY_HALL"

print("Congratulations, you win!")

import json

# load the .json file
f = open('Adventure for school/script.json')
dataFile = json.load(f)
f.close()

currentRoom = "FOREST"
currentDesc = ""
currentMovements = []
availableItems = []
availableInteractions = []
availableResults = []
inventory = ["HOUSE_KEY"]
houseOpen = False

def displayIntro():
    print("You remember camping with your friends in the forest but it seems foggy and your head hurts.")
    print("You don't know where you are or how you got there.")

def inventoryUI():
    print(f"\nYou have:\n{' '.join(inventory)}")
    input("Press enter to continue...")

def actionsUI():
    print("Go to ___\nTake ___\nUse ___\nInventory")
    input("Press enter to continue...")


displayIntro()
while True:
    availableInteractions = dataFile["places"][currentRoom]["availableInteractions"]
    currentMovements = dataFile["places"][currentRoom]["connectedPlaces"]
    currentDesc = dataFile["places"][currentRoom]["description"]
    availableItems = dataFile["places"][currentRoom]["items"]
    availableResults = dataFile["places"][currentRoom]["interactionResults"]

    action = input(f"\n(To check the commands type \"actions\")\nYou are in the {currentRoom}\n{currentDesc}\nMovement options:\n{' '.join(currentMovements)}\nAvailable items:\n{' '.join(availableItems)}\n>").upper()
    
    if action == "INVENTORY":
        inventoryUI()
    elif action == "ACTIONS":
        actionsUI()

    elif "TAKE " in action:
        # check if the item in action is also in available items
        for i in availableItems:
            if i in action:
                inventory.append(i)
                print(f"\nYou got {i}")
                print(dataFile["places"][currentRoom]["itemDescriptions"][i])
                dataFile["places"][currentRoom]["items"].remove(i)
                input("Press enter to continue...")

    elif "GO TO " in action:
        # check if the place in action is also in the available movements
        for i in currentMovements:
            if i in action:
                currentRoom = i

    elif "USE " in action:
        # check if the item in action is also in available interactions and inventory
        for i in availableInteractions:
            if i in action and i in inventory:
                print(availableResults[i])
                if i == "SHOVEL":
                    dataFile["places"]["FOREST"]["connectedPlaces"].remove("DIRT_PATCH")
                    dataFile["places"]["FOREST"]["connectedPlaces"].append("THE_HOLE")
                    currentRoom = "THE_HOLE"
                
                elif i == "STRANGE_KEY":
                    inventory.append("HOUSE_KEY")
                    print(f"You got HOUSE_KEY")
                    print(dataFile["places"][currentRoom]["itemDescriptions"]["HOUSE_KEY"])
                    input("Press enter to continue...")
                
                elif i == "HOUSE_KEY":
                    houseOpen = True
                
                elif i == "PHONE":
                    quit()
    
    if currentRoom == "HOUSE":
        if houseOpen is False:
            print("the door is locked")
            currentRoom = "FRONTYARD"
        else:
            currentRoom = "ENTRY_HALL"

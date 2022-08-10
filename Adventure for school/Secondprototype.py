import time
import json

f = open('script.json')
dataFile = json.load(f)
f.close()

godCommands = False
currentRoom = "FOREST"
currentDesc = ""
currentMovements = []
availableItems = []
availableInteractions = []
availableResults = []
inventory = []

houseOpen = False
chestUp = False
slowText = 0.25
slowerText = 1


def displayIntro():
    print("intro")
    print("intro")
    print("intro")
    print("intro")

def inventoryUI():
    print(f"You have:\n{' '.join(inventory)}")
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
    
    if currentRoom == "HOUSE":
        if houseOpen is False:
            print("the door is locked")
            currentRoom = "FRONTYARD"

            availableInteractions = dataFile["places"][currentRoom]["availableInteractions"]
            currentMovements = dataFile["places"][currentRoom]["connectedPlaces"]
            currentDesc = dataFile["places"][currentRoom]["description"]
            availableItems = dataFile["places"][currentRoom]["items"]
            availableResults = dataFile["places"][currentRoom]["interactionResults"]
        else:
            while currentRoom == "HOUSE":
                action = input(f"\n(To check the commands type \"actions\")\nYou are in the {currentRoom}\n{currentDesc}\nMovement options:\n{' '.join(currentMovements)}\nAvailable items:\n{' '.join(availableItems)}\n>").upper()

                if action == "INVENTORY":
                    inventoryUI()
                elif action == "ACTIONS":
                    actionsUI()
                elif "TAKE" in action:
                    if "PHONE" in action:
                        inventory.append("PHONE")
                elif action == "GO TO FRONTYARD":
                    currentRoom = "FRONTYARD"

                    availableInteractions = dataFile["places"][currentRoom]["availableInteractions"]
                    currentMovements = dataFile["places"][currentRoom]["connectedPlaces"]
                    currentDesc = dataFile["places"][currentRoom]["description"]
                    availableItems = dataFile["places"][currentRoom]["items"]
                    availableResults = dataFile["places"][currentRoom]["interactionResults"]
    elif currentRoom == "F0REST":
        while currentRoom == "F0REST":
            action = input(f"\n(To check the commands type \"actions\")\nYou are in the {currentRoom}\n{currentDesc}\nMovement options:\n{' '.join(currentMovements)}\nAvailable items:\n{' '.join(availableItems)}\n>").upper()
            if action == "ACTIONS":
                actionsUI()
            elif action == "INVENTORY":
                inventoryUI()
            elif action == "GO TO BACKYARD":
                currentRoom = "BACKYARD"

                availableInteractions = dataFile["places"][currentRoom]["availableInteractions"]
                currentMovements = dataFile["places"][currentRoom]["connectedPlaces"]
                currentDesc = dataFile["places"][currentRoom]["description"]
                availableItems = dataFile["places"][currentRoom]["items"]
                availableResults = dataFile["places"][currentRoom]["interactionResults"]
            elif action == "GO TO FURTHER":
                while currentRoom == "F0REST":
                    action = input(f"(To check the commands type \"actions\")\nYou are in the F0REST\nyou can't see very far in front of you, the darkness cloaks everything but the light you can see from the clearing, it seems warm over there, go that way\nMovement options:\nFURTHER (I can't remove this option) BACKYARD (pretend this is the only option)\nAvailable items:\n\n>").upper()
                    if action == "ACTIONS":
                        actionsUI()
                    elif action == "INVENTORY":
                        print("you can check once you're safe")
                    elif action == "GO TO BACKYARD":
                        currentRoom = "BACKYARD"
                        availableInteractions = dataFile["places"][currentRoom]["availableInteractions"]
                        currentMovements = dataFile["places"][currentRoom]["connectedPlaces"]
                        currentDesc = dataFile["places"][currentRoom]["description"]
                        availableItems = dataFile["places"][currentRoom]["items"]
                        availableResults = dataFile["places"][currentRoom]["interactionResults"]

                    elif action == "GO TO FURTHER":
                        i = 1
                        while i < 5:
                            i += 1
                            print("G", end='')
                            time.sleep(slowText)
                            print("O")
                            time.sleep(slowText*2)
                            print("B", end='')
                            time.sleep(slowText)
                            print("A", end='')
                            time.sleep(slowText)
                            print("C", end='')
                            time.sleep(slowText)
                            print("K")
                            time.sleep(slowText*2)
                        print("its too late. you have to quit the game.")
                        print("dont")
                        time.sleep(slowerText)
                        print("go")
                        time.sleep(slowerText)
                        print("further")

                        while True:
                            action = input(">")
                            if action.lower() == "go to further":
                                print("you find your camp and all your friends\nyou win")
                                quit()
    elif currentRoom == "DIRT_PATCH" and chestUp is True:
        currentRoom = "THE_HOLE"

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
        for i in availableItems:
            if i in action:
                inventory.append(i)
                print(f"You got {i}")
                print(dataFile["places"][currentRoom]["itemDescriptions"][i])
                dataFile["places"][currentRoom]["items"].remove(i)
                input("Press enter to continue...")
    elif "GO TO " in action:
        for i in currentMovements:
            if i in action:
                if currentRoom == "BACKYARD" and "FOREST" in action:
                    currentRoom = "F0REST"
                else:
                    currentRoom = i
    elif "USE " in action:
        for i in availableInteractions:
            if i in action and i in inventory:
                if i == "SHOVEL":
                    print(availableResults[i])
                    chestUp = True
                elif i == "STRANGE_KEY":
                    print(availableResults[i])
                    inventory.append("HOUSE_KEY")
                    print(f"You got HOUSE_KEY")
                    print(dataFile["places"][currentRoom]["itemDescriptions"]["HOUSE_KEY"])
                    input("Press enter to continue...")
                elif i == "HOUSE_KEY":
                    print(availableResults[i])
                    houseOpen = True
                elif i == "PHONE":
                    print(availableResults[i])
                    quit()

import sys
from typing import List, Dict, Union
from time import sleep
import csv
from tabulate import tabulate

from map import Location, Room
from inventory import Inventory


def get_rooms_for_location(
    action_location: Union[Location, str], locations: List[Union[Location, str]]
) -> List[Union[Room, str]]:
    """
    Get the rooms for a given location.

    Args:
        action_location (Union[Location, str]): The current location.
        locations (List[Union[Location, str]]): List of all locations.

    Returns:
        List[Union[Room, str]]: List of rooms for the given location.
    """
    # print(f"get_rooms_for_location called with {action_location} and {locations}")
    if isinstance(action_location, Location):
        # print("is an instance of Location")
        return action_location.rooms
    elif action_location == "Check Inventory":
        # print("action_location is checking inventory")
        return ["Check Inventory"]
    elif action_location == "Quit Game":
        return ["Quit Game"]
    else:
        for location in locations:
            if isinstance(location, Location) and location.location == action_location:
                # print("location.rooms")
                return location.rooms
    # print("None of those")
    return []


def handle_location_options(action_location, cache):
    """
    Handle options at the location level.

    Args:
        action_location (Union[Location, str]): The current location.
        cache: List[Dict[str, str]]: Player's current inventory

    Returns:
        bool: True if the player wants to leave the location, False otherwise.
    """
    while True:
        print(
            f"\nYou are at {action_location.location if isinstance(action_location, Location) else action_location}. What would you like to do?"
        )
        options = [
            "Explore Rooms",
            "Leave this location",
            "Check inventory",
            "Quit game",
        ]
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = get_commands("Choose an option: ", len(options))

        if choice == 1:  # Explore Rooms
            return False
        elif choice == 2:  # Leave this location
            return True
        elif choice == 3:  # Check inventory
            if cache:
                print("\nInventory:")
                for item in cache:
                    print(f"- {item['item']}: {item['description']}")
            else:
                print("\nYour inventory is empty.")
            print()
        elif choice == 4:  # Quit game
            print("Thanks for playing!")
            sys.exit()


def typingPrint(text: str):
    """
    Print text with a typewriter effect.

    Args:
        text (str): The text to print.
    """
    text = text.lstrip()
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        sleep(0.05)


def get_commands(message: str, length: int) -> int:
    """
    Get user input and convert it to an integer within a valid range.

    Args:
        message (str): The prompt message for input.
        length (int): The maximum valid input value.

    Returns:
        int: The validated user input.
    """
    while True:
        try:
            action_input = int(input(message))
            if 1 <= action_input <= length:
                return action_input
        except ValueError:
            pass
        print("Invalid input. Please enter a number within the valid range.")


def get_location(locations: List[Union[Location, str]]) -> Union[Location, str]:
    """
    Display location options and get user's choice.

    Args:
        locations (List[Union[Location, str]]): List of available locations.

    Returns:
        Union[Location, str]: The chosen location.
    """
    for i, location in enumerate(locations, 1):
        print(
            f"{i}. {location.location if isinstance(location, Location) else location}"
        )
    print()
    action_input = get_commands("Location: ", len(locations))
    print()
    action_location = locations[action_input - 1]
    if isinstance(action_location, Location):
        print(f"Going to {action_location.location}!\n")
    return action_location


def get_room(rooms: List[Union[Room, str]], location_name: str) -> Union[Room, str]:
    """
    Display room options and get user's choice, including an option to leave.

    Args:
        rooms (List[Union[Room, str]]): List of available rooms.
        location_name (str): Name of the current location.

    Returns:
        Union[Room, str]: The chosen room or "Leave" if the user wants to exit.
    """
    options = rooms + [f"Leave {location_name}"]
    for i, room in enumerate(options, 1):
        print(f"{i}. {room.room if isinstance(room, Room) else room}")
    print()
    action_input = get_commands("Room: ", len(options))
    return options[action_input - 1]


def get_action(action_room: Room, cache: List[Dict[str, str]], money: int = 0) -> str:
    """
    Display action options and get user's choice.

    Args:
        action_room (Room): The current room.
        cache: List[Dict[str, str]]: Player's current inventory
        money (int, optional): The amount of money the player has. Defaults to 0.

    Returns:
        str: The chosen action.
    """
    actions = []
    if action_room.person:
        actions.append(f"Question {action_room.person}")
    if action_room.items:
        actions.append(f"Examine {action_room.items}")
    if action_room.room:
        actions.append(f"Leave {action_room.room}")
    if money > 0:
        print(f"You have ${money}.")
    if cache:
        actions.append("Check Inventory")

    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    print()
    action_input = get_commands("Action: ", len(actions))
    return actions[action_input - 1]


def check_room_action(
    index: str, action_room: Room, items: List[Inventory], cache: List[Dict[str, str]]
) -> Union[bool, tuple]:
    """
    Handle the chosen action for a room.

    Args:
        index (str): The chosen action.
        action_room (Room): The current room.
        items (List[Inventory]): List of available items.
        cache: List[Dict[str, str]]: Player's current inventory

    Returns:
        Union[bool, tuple]: Result of the action.
    """

    if index.startswith("Question"):
        print(f"{action_room.text}\n")
        return False

    if index == "Examine a diary":
        return handle_diary_examination(action_room)

    if index.startswith("Examine"):
        print(f"{action_room.items}: {action_room.item_description}\n")
        for item in items:
            if action_room.items == item.item:
                temp_dict = {
                    "item": action_room.items,
                    "description": action_room.item_description,
                }
                if temp_dict not in cache:
                    return temp_dict, False
        return False

    if index == "Check Inventory":
        print("Inventory:")
        for item in cache:
            print(f"{item['item']} : {item['description']}")
        print()
        return False

    if index.startswith("Leave"):
        return True


def check_lock(cache: List[Dict[str, str]]) -> bool:
    """
    Check if the player has a lock pick kit in their inventory.

    Args:
        cache: List[Dict[str, str]]: Player's current inventory

    Returns:
        bool: True if the player has a lock pick kit, False otherwise.
    """
    for item in cache:
        if item["item"] == "a lock pick kit":
            print("The door was locked, but you used the lock pick kit to get in.\n")
            return True
    print("The door is locked, so you can't get in.\n")
    return False


def game_over(message: str):
    """
    End the game with a message.

    Args:
        message (str): The game over message.
    """
    typingPrint(message)
    typingPrint("You lose")
    sys.exit()


def handle_diary_examination(action_room: Room, cache: List[Dict[str, str]]) -> bool:
    """
    Handle the examination of the diary.

    Args:
        action_room (Room): The current room.
        cache: List[Dict[str, str]]: Player's current inventory

    Returns:
        bool: True if the code is solved, False otherwise.
        cache: List[Dict[str, str]]: Player's updated inventory
    """
    solve_code = False
    print("You find the following text in the diary:")
    with open("cipher.txt", "r") as file:
        print(file.read())

    solve_code = decoded("Examine a diary", action_room)

    temp_dict = {
        "item": action_room.items,
        "description": action_room.item_description,
    }
    if temp_dict not in cache:
        cache.append(temp_dict)
    return solve_code, cache


def decoded(index: str, action_room: Room) -> bool:
    """
    Check if the player has correctly decoded the message.

    Args:
        index (str): The chosen action.
        action_room (Room): The current room.

    Returns:
        bool: True if the message is correctly decoded, False otherwise.
    """
    # Source: https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-the-user
    print("Enter/Paste your content. Ctrl-D to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
        decode = open("decoded.txt")
        txt = decode.read()
        for code in contents:
            if code in txt:
                print()
                print("Correct")
                print()
                return True
            else:
                print("Input not recognized")
                decode.close()
                return False


def check_cipher(index, action_room):
    if index == f"Examine {action_room.items}":
        # Source: https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-the-user
        print("Enter/Paste your content. Ctrl-D to save it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        cipher = open("cipher.txt")
        txt = cipher.read()
        for code in contents:
            if code in txt:
                with open("decoded.txt", "r") as file:
                    lines = file.readlines()
                    print()
                    for line in lines:
                        print(line, end="")
                    print("\n")
                cipher.close()
                return True
            else:
                print("Input not recognize")
                cipher.close()
                return False


def print_csv(file: str):
    """
    Print the contents of a CSV file in a tabulated format.

    Args:
        file (str): The name of the CSV file.
    """
    with open(file, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        print(tabulate(data, headers="firstrow"))


def handle_school(action_room: Room):
    """
    Handle actions in the school.

    Args:
        action_room (Room): The current room.
    """
    if action_room.room == "Music Room":
        text = (
            action_room.text or "You enter the Music Room."
        )  # Provide a default text if None
        typingPrint(text)
        game_over("You lose")

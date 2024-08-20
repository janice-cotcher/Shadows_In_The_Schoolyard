import sys
from typing import List, Dict, Union, Tuple, Optional
from time import sleep
import csv
from tabulate import tabulate

from map import Location, Room
from inventory import Inventory

# Global variables
cache: List[Dict[str, str]] = []
solve_code: bool = False

# Add these imports at the top of the file
from typing import List, Dict, Union, Tuple, Optional

# Add this function definition
def get_rooms_for_location(action_location: Union[Location, str], locations: List[Union[Location, str]]) -> List[Union[Room, str]]:
    """
    Get the rooms for a given location.

    Args:
        action_location (Union[Location, str]): The current location.
        locations (List[Union[Location, str]]): List of all locations.

    Returns:
        List[Union[Room, str]]: List of rooms for the given location.
    """
    if isinstance(action_location, Location):
        return action_location.rooms
    elif action_location == "Quit Game":
        return ["Quit Game"]
    else:
        for location in locations:
            if isinstance(location, Location) and location.location == action_location:
                return location.rooms
    return []

# Add this function definition
def handle_basement_visit():
    """Handle the basement visit in the theatre."""
    typingPrint(
        "Performing a reverse image search on the mural, Maeve uncovered obscure texts on the Cthulhu mythos and Tsathoggua's insatiable hunger for power. Here, they realized a cult was determined to bring this eldritch horror into their world."
    )
    print()

# Locations
retirement = Location("Trinity Manor", [Room("Trinity Manor", "Main Desk")])
retirement_herring = Location("Hawkins Continuing-Care Community", [Room("Hawkins Continuing-Care Community", "Security Desk")])
restaurant = Location("Benny's Burgers", [Room("Benny's Burgers", "Diner Counter")])
archdiocese = Location("Archdiocese of Hawkins", [Room("Archdiocese of Hawkins", "Chancery")])
agency = Location("Malone's Detective Agency", [Room("Malone's Detective Agency", "Front Reception")])
maeve = Location("Maeve's House", [Room("Maeve's House", "Kitchen"), Room("Maeve's House", "Maeve's Bedroom")])
theo = Location("Theo's House", [Room("Theo's House", "Kitchen")])
school = Location("Hawkins Collegiate", [Room("Hawkins Collegiate", "Journalism Classroom"), Room("Hawkins Collegiate", "Front Office"), Room("Hawkins Collegiate", "Lunch Room")])
occult = Location("Mystic Minds", [Room("Mystic Minds", "Store Front"), Room("Mystic Minds", "Fortune Teller Room")])
palm = Location("Mme. Avalonia's Palm Readings", [Room("Mme. Avalonia's Palm Readings", "Palm Reading Room")])
box = Location("The Magic Box", [Room("The Magic Box", "Retail Space"), Room("The Magic Box", "Backroom")])
library = Location("Hawkins Public Library", [Room("Hawkins Public Library", "Mythology Section"), Room("Hawkins Public Library", "Local Maps")])
theatre = Location("Orpheum Theater", [Room("Orpheum Theater", "Concession Stand"), Room("Orpheum Theater", "Auditorium"), Room("Orpheum Theater", "Theatre Basement")])
mall = Location("Hawkins Shopping Centre", [Room("Hawkins Shopping Centre", "Hawkins Grocery & More")])
cemetery = Location("Whispering Pine Cemetery", [Room("Whispering Pine Cemetery", "A clearing in the middle of the cemetery")])
factory = Location("Hawkins Factory", [Room("Hawkins Factory", "Manager's Office"), Room("Hawkins Factory", "Rotting machinery"), Room("Hawkins Factory", "Catwalk - a narrow walkway above the factory floor")])
police = Location("Hawkins Police Station", [Room("Hawkins Police Station", "Front Reception")])
catholic = Location("St. Patrick's Parish Church", [Room("St. Patrick's Parish Church", "Administration Office"), Room("St. Patrick's Parish Church", "Cathedral's Basement")])
#Inventory

kit = Inventory("a lock pick kit", "Tools to unlock a locked door")
blocker = Inventory("a signal jammer", "A hand-held, portable device that prevents wireless communications within a 15-meter radius.")
amulet = Inventory("a shattered amulet", "Among the rubble in the basement of the dilapidated theatre, you find a broken amulet.")
salt_shaker = Inventory("salt", "ordinary table salt")

def main():
    """
    Main function to run the game.
    """
    intro_text()
    act_one()
    print()
    act_two()
    print()
    act_three(cache)


def intro_text():
    """
    Print the game's title and introduction in a typewriter-style.
    """
    title = "Shadows in the Schoolyard\n\n"
    typingPrint(title)
    intro = """
Act I: The Case Unveiled
Rain pounded the cracked pavement outside as Veronica "Ronnie" Malone leaned against the dimly lit hallway lockers, her hood low over her eyes. The teenage private investigator learned her detective skills from her father, a grizzled P.I. named Jack Malone. Ronnie had her own side hustle, taking on cases from her high school peers when needed.

Ronnie didn't work alone; she had a ragtag group of friends who helped her. There was Max, the tech genius who could hack into anything; Maeve, the bookworm with an uncanny ability to dig up information; and Theo, the fearless daredevil with a knack for getting them out of tight spots.

On that gloomy morning, a frantic girl named Lily approached Ronnie in hushed tones. "Veronica, you have to help me. My friend, Emily, she's gone. Disappeared without a trace."
"""
    typingPrint(intro)


def act_one():
    """
    Run the first act of the game.
    """
    # Initialize locations and items
    locations, items = initialize_act_one()

    while True:
        print("\nWhere do you want to go?")
        action_location = get_location(locations)

        if action_location == "Quit Game":
            sys.exit()
        elif action_location == "Hawkins Factory":
            break

        rooms = get_rooms_for_location(action_location, locations)

        while True:
            print("What room do you want to go to?")
            action_room = get_room(rooms)

            if action_room == f"Leave {action_location}":
                break

            print(f"Going to {action_room.room}!\n")
            print(f"{action_room}\n")

            while True:
                print("What do you want to do?")
                index = get_action(action_room)
                result = check_room_action(index, action_room, items)

                if isinstance(result, tuple):
                    returned_dict, returned_bool = result
                    cache.append(returned_dict)
                else:
                    returned_bool = result

                if returned_bool:
                    break

                # Special case for Sarah Bartlett
                if action_room.person == "Sarah Bartlett":
                    if "Hawkins Factory" not in locations:
                        locations.insert(-1, "Hawkins Factory")

    one_outro = """
The only lead they had was that Emily had been investigating the abandoned Hawkins Factory on the outskirts of town. Determined, they set out for the factory, rain-soaked streets giving way to overgrown paths.
"""
    typingPrint(one_outro)


def act_two():
    """
    Run the second act of the game.
    """
    global solve_code
    basement_visit = False

    two_intro = """
Act II: A Whisper of Shadows
The Hawkins Factory was a dilapidated structure that loomed like a forgotten sentinel on the edge of town. As they entered its decaying interior, the air was thick with an eerie stillness; broken windows and graffiti-covered walls greeted Ronnie and her team.
"""
    typingPrint(two_intro)
    print()

    # Initialize locations and items
    locations, items = initialize_act_two()

    while True:
        if basement_visit and solve_code:
            break

        print("\nWhere do you want to go?")
        action_location = get_location(locations)

        if action_location == "Quit Game":
            sys.exit()

        rooms = get_rooms_for_location(action_location, locations)

        if not rooms:
            continue

        while True:
            if solve_code and basement_visit:
                break

            print("What room do you want to go to?")
            action_room = get_room(rooms)

            if action_room == f"Leave {action_location}":
                break

            print(f"Going to {action_room.room}!\n")

            # Special case for Jack Malone's office
            if action_room.room == "Office" and action_location == "Malone's Detective Agency":
                game_over("You enter your dad's office to find his signal jammer. To your surprise, your father is there sitting at the desk.")

            print(f"{action_room}\n")

            while True:
                print("What do you want to do?")
                index = get_action(action_room)

                if index == "Examine a diary":
                    handle_diary_examination()
                    if solve_code and basement_visit:
                        break

                result = check_room_action(index, action_room, items)

                if isinstance(result, tuple):
                    returned_dict, returned_bool = result
                    cache.append(returned_dict)
                else:
                    returned_bool = result

                if returned_bool:
                    break

                if action_room.room == "Theatre Basement":
                    basement_visit = True
                    handle_basement_visit()


def act_three(cache: List[Dict[str, str]]):
    """
    Run the third act of the game.

    Args:
        cache (List[Dict[str, str]]): The player's inventory.
    """
    # Initialize game state
    salt_bool = False
    blessed_salt_bool = False
    amulet_bool = False
    money = 0
    attempts_trinity = 0
    attempts_carehome = 0
    hours = 12
    attempts_giles = 0
    theo_bool = True
    max_bool = True
    attempts_jack = 0
    attempts_piggybank = 0

    # Print intro text
    intro_text = "Act III: Unveiling the Horror\nThreats started closing in around them. Ronnie's friends began receiving ominous messages, taunting them to stop their investigation or face dire consequences. The stakes had never been higher.\n"
    typingPrint(intro_text)
    print(get_instructions())

    # Initialize locations and items
    locations, items = initialize_act_three()

    while hours > 0:
        print(f"You have {hours} hours left.")
        print("Where do you want to go?")
        action_location = get_location(locations)
        
        if isinstance(action_location, Location):
            rooms = action_location.rooms
        
        hours -= 1
        
        if action_location == "Quit Game":
            sys.exit()
        
        if f"Leave {action_location.location}" not in rooms:
            rooms.append(f"Leave {action_location.location}")
        
        while True:
            action_room = get_room(rooms)
            if action_room == f"Leave {action_location.location}":
                break
            
            print(f"Going to {action_room.room}!\n")
            print(f"{action_room}\n")
            
            while True:
                print("What do you want to do?")
                index = get_action(action_room, money, cache)
                
                # Handle special cases for different locations
                if action_location == retirement:
                    handle_retirement_manor(action_room, index, attempts_trinity, salt_bool, blessed_salt_bool, cache)
                elif action_location == retirement_herring:
                    handle_retirement_herring(action_room, index, attempts_carehome)
                elif action_location == restaurant:
                    handle_restaurant(index, salt_bool)
                elif action_location == archdiocese:
                    handle_archdiocese(index)
                elif action_location == agency:
                    handle_agency(index, attempts_jack, money)
                elif action_location == maeve:
                    handle_maeve(index, attempts_piggybank, money)
                elif action_location == theo:
                    handle_theo(action_room, theo_bool)
                elif action_location == school:
                    handle_school(action_room)
                elif action_location == max:
                    handle_max(action_room, max_bool)
                elif action_location == occult:
                    handle_occult(index, money, cache)
                elif action_location == palm:
                    handle_palm(index, money)
                elif action_location == box:
                    handle_magic_box(index, hours, attempts_giles, money, blessed_salt_bool, cache)
                elif action_location == library:
                    handle_library(index, locations)
                elif action_location == theatre:
                    handle_theatre(index, cache, amulet_bool)
                elif action_location == mall:
                    handle_mall(index, money, cache, salt_bool)
                elif action_location == cemetery:
                    handle_cemetery(theo_bool, max_bool, cache, amulet_bool, blessed_salt_bool)
                
                result = check_room_action(index, action_room, items, cache)
                if isinstance(result, tuple):
                    returned_dict, returned_bool = result
                    cache.append(returned_dict)
                else:
                    returned_bool = result

                if returned_bool:
                    break

    game_over("You are too late and the time of Tsathoggua has come.")


# Helper functions

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
        print(f"{i}. {location.location if isinstance(location, Location) else location}")
    print()
    action_input = get_commands("Location: ", len(locations))
    print()
    action_location = locations[action_input - 1]
    if isinstance(action_location, Location):
        print(f"Going to {action_location.location}!\n")
    return action_location

def get_rooms_for_location(action_location: Union[Location, str], locations: List[Union[Location, str]]) -> List[Union[Room, str]]:
    """
    Get the rooms for a given location.

    Args:
        action_location (Union[Location, str]): The current location.
        locations (List[Union[Location, str]]): List of all locations.

    Returns:
        List[Union[Room, str]]: List of rooms for the given location.
    """
    if isinstance(action_location, Location):
        return action_location.rooms
    elif action_location == "Quit Game":
        return ["Quit Game"]
    else:
        for location in locations:
            if isinstance(location, Location) and location.location == action_location:
                return location.rooms
    return []

def get_room(rooms: List[Union[Room, str]]) -> Union[Room, str]:
    """
    Display room options and get user's choice.

    Args:
        rooms (List[Union[Room, str]]): List of available rooms.

    Returns:
        Union[Room, str]: The chosen room.
    """
    for i, room in enumerate(rooms, 1):
        print(f"{i}. {room.room if isinstance(room, Room) else room}")
    print()
    action_input = get_commands("Room: ", len(rooms))
    print()
    return rooms[action_input - 1]


def get_action(action_room: Room, money: int = 0, cache: List[Dict[str, str]] = None) -> str:
    """
    Display action options and get user's choice.

    Args:
        action_room (Room): The current room.
        money (int, optional): The amount of money the player has. Defaults to 0.
        cache (List[Dict[str, str]], optional): The player's inventory. Defaults to None.

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


def check_room_action(index: str, action_room: Room, items: List[Inventory], cache: List[Dict[str, str]]) -> Union[bool, tuple]:
    """
    Handle the chosen action for a room.

    Args:
        index (str): The chosen action.
        action_room (Room): The current room.
        items (List[Inventory]): List of available items.
        cache (List[Dict[str, str]]): The player's inventory.

    Returns:
        Union[bool, tuple]: Result of the action.
    """
    global solve_code

    if index.startswith("Question"):
        print(f"{action_room.text}\n")
        return False
    
    if index == "Examine a diary":
        return handle_diary_examination(action_room, cache)
    
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
        cache (List[Dict[str, str]]): The player's inventory.

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
        cache (List[Dict[str, str]]): The player's inventory.

    Returns:
        bool: True if the code is solved, False otherwise.
    """
    global solve_code
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
    return False


def decoded(index: str, action_room: Room) -> bool:
    """
    Check if the player has correctly decoded the message.

    Args:
        index (str): The chosen action.
        action_room (Room): The current room.

    Returns:
        bool: True if the message is correctly decoded, False otherwise.
    """
    print("What does the coded message say? Ctrl-D to save it.")
    contents = []
    while True:
        try:
            line = input()
            contents.append(line)
        except EOFError:
            break
    
    with open("decoded.txt", "r") as decode_file:
        decoded_text = decode_file.read()
        if any(code in decoded_text for code in contents):
            print("\nCorrect\n")
            return True
        else:
            print("Input not recognized")
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


def get_instructions() -> str:
    """
    Get the instructions for Act III.

    Returns:
        str: The instructions text.
    """
    return """
It is noon and Ronnie thinks that the ritual will take place tonight. There a couple of problems:
- you don't know where The Old Woods are
- you need a piece of a shattered amulet, but which amulet?
- you need salt blessed by a local priest
- each place you visit will make 1-hour pass and you only have 12 hours until midnight (no time penalty for visiting rooms within a location)
"""


def initialize_act_one() -> Tuple[List[Union[Location, str]], List[Inventory]]:
    """
    Initialize locations and items for Act I.

    Returns:
        Tuple[List[Union[Location, str]], List[Inventory]]: Locations and items for Act I.
    """
    # Initialize rooms and locations
    journalism = Room(
        "Hawkins Collegiate",
        "Journalism Classroom",
        "Mr. Sinclair",
        "the journalism teacher",
        "All I know is Emily was researching gang activity in the school before she disappeared.",
    )
    school_reception = Room(
        "Hawkins Collegiate",
        "Front Office",
        "Mx. Douglas",
        "the receptionist",
        "Emily asked me for attendance records for four students. I told her I am not allowed to give out that information.",
    )
    school_lunch = Room(
        "Hawkins Collegiate", 
        "Lunch Room", 
        "Kai", 
        "Emily's friend", 
        "She was being really secretive and distracted before she disappeared. She always had her nose in her notebook, trying to solve puzzles. Maybe her boss at the newspaper will know more.",
    )
    school = Location(
        "Hawkins Collegiate",
        [school_lunch, journalism, school_reception],
    )

    posters = Inventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    police_reception = Room(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters.",
        posters.item,
        posters.description,
    )
    police = Location("Hawkins Police Station", [police_reception])

    paper = Inventory(
        "a torn piece of paper", 'The torn piece of paper reads: "Shift 7  a->h."'
    )
    editor = Room(
        "Hawkins Daily News",
        "Editor's Office",
        "Sarah Bartlett",
        "Emily's boss",
        "Before she went missing, she was investigating the connection between the string of teen disappearance to the abandoned Hawkins Factory. I don't know much else, but you can check her desk.",
    )
    desk = Room(
        "Hawkins Daily News",
        "Emily's Desk",
        items=paper.item,
        item_description=paper.description,
    )
    newspaper = Location("Hawkins Daily News", [editor, desk])

    kit = Inventory("a lock pick kit", "Tools to unlock a locked door")
    blocker = Inventory(
        "a signal jammer",
        "A hand-held, portable device that prevents wireless communications within a 15-meter radius.",
    )
    agency_reception = Room("Malone's Detective Agency", "Front Reception")
    agency_office = Room(
        "Malone's Detective Agency",
        "Office",
        items=blocker.item,
        item_description=blocker.description,
    )
    agency_closet = Room(
        "Malone's Detective Agency",
        "Supply Closet",
        items=kit.item,
        item_description=kit.description,
    )
    agency = Location(
        "Malone's Detective Agency",
        [agency_reception, agency_office, agency_closet],
    )

    locations = [
        school,
        police,
        newspaper,
        agency,
        "Quit Game",
    ]
    items = [paper, kit, blocker, posters]

    return locations, items


def initialize_act_two() -> Tuple[List[Union[Location, str]], List[Inventory]]:
    """
    Initialize locations and items for Act II.

    Returns:
        Tuple[List[Union[Location, str]], List[Inventory]]: Locations and items for Act II.
    """
    # Initialize rooms and locations
    manager = Room("Hawkins Factory", "Manager's Office", items="an old computer")
    machinery = Room(
        "Hawkins Factory",
        "Rotting machinery",
        items="a shiny lever on a rusted machine",
    )
    catwalk = Room(
        "Hawkins Factory", "Catwalk - a narrow walkway above the factory floor"
    )
    diary = Inventory("a diary", "a diary with pages filled with strange writings")
    secret = Room(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    factory = Location("Hawkins Factory", [manager, machinery, catwalk])

    kit = Inventory("a lock pick kit", "Tools to unlock a locked door")
    agency_reception = Room("Malone's Detective Agency", "Front Reception")
    agency_office = Room(
        "Malone's Detective Agency",
        "Office",
        "Jack Malone",
        "private investigator and Ronnie's father",
        "What did I tell you kids about coming here after hours? I'm calling your parents and you are going straight home.",
    )
    agency_closet = Room(
        "Malone's Detective Agency",
        "Supply Closet",
        items=kit.item,
        item_description=kit.description,
    )
    agency = Location(
        "Malone's Detective Agency",
        [agency_reception, agency_office, agency_closet],
    )

    journalism = Room("Hawkins Collegiate", "Journalism Classroom")
    computer = Inventory("the receptionist's computer", "Max hacks into the receptionist's computer while Theo stands outside on the lookout. Looking up all the missing students, they all had one thing in common: they are all enrolled in the same Journalism class.")
    school_reception = Room(
        "Hawkins Collegiate",
        "Front Office",
        items=computer.item,
        item_description=computer.description,
    )
    school_lunch = Room("Hawkins Collegiate", "Lunch Room")
    school = Location(
        "Hawkins Collegiate",
        [school_lunch, journalism, school_reception],
    )

    posters = Inventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg.",
    )
    police_reception = Room(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters.",
        posters.item,
        posters.description,
    )
    police = Location("Hawkins Police Station", [police_reception])

    paper = Inventory(
        "a torn piece of paper", 'The torn piece of paper reads: "Shift 7  a->h."'
    )
    editor = Room("Hawkins Daily News", "Editor's Office")
    desk = Room(
        "Hawkins Daily News",
        "Emily's Desk",
        items=paper.item,
        item_description=paper.description,
    )
    newspaper = Location("Hawkins Daily News", [editor, desk])

    graffiti = Inventory(
        "a graffitied wall",
        "In the bowels of the abandoned building, they found a hidden room filled with disturbing artifacts and a mural depicting a large furry toad.",
    )
    concession = Room("Orpheum Theater", "Concession Stand")
    auditorium = Room("Orpheum Theater", "Auditorium")
    basement = Room(
        "Orpheum Theater",
        "Theatre Basement",
        items=graffiti.item,
        item_description=graffiti.description,
    )
    theatre = Location("Orpheum Theater", [auditorium, basement, concession])

    locations = [
        factory,
        agency,
        school,
        police,
        newspaper,
        theatre,
        "Quit Game",
    ]
    items = [kit, diary, computer, posters, paper, graffiti]

    return locations, items

def initialize_act_three() -> Tuple[List[Union[Location, str]], List[Inventory]]:
    """
    Initialize locations and items for Act III.

    Returns:
        Tuple[List[Union[Location, str]], List[Inventory]]: Locations and items for Act III.
    """
    locations = [
        school,
        factory,
        theatre,
        police,
        agency,
        catholic,
        archdiocese,
        retirement,
        retirement_herring,
        occult,
        palm,
        box,
        mall,
        library,
        restaurant,
        theo,
        maeve,
    ]
    locations.sort(key=lambda instance: instance.location)

    items = [kit, blocker, amulet, salt_shaker]

    return locations, items


def handle_retirement_manor(room: Room, index: str, attempts_trinity: int, salt_bool: bool, blessed_salt_bool: bool, cache: List[Dict[str, str]]) -> Tuple[int, bool, bool, List[Dict[str, str]], Optional[Room]]:
    """
    Handle actions in the Trinity Manor retirement home.

    Args:
        room (Room): The current room.
        index (str): The chosen action.
        attempts_trinity (int): Number of attempts to access Trinity Manor.
        salt_bool (bool): Whether the player has salt.
        blessed_salt_bool (bool): Whether the player has blessed salt.
        cache (List[Dict[str, str]]): The player's inventory.

    Returns:
        Tuple[int, bool, bool, List[Dict[str, str]], Optional[Room]]: 
            Updated attempts_trinity, salt_bool, blessed_salt_bool, cache, and new room if created.
    """
    new_room = None
    if index == "Question Phil Callahan":
        if attempts_trinity < 3:
            text_phil = input("Who are you here to see? ")
            attempts_trinity += 1
        else:
            room.text = "You obviously don't know anyone here, please leave."
        
        if text_phil.strip() == "Zachariah Dowey":
            new_room = Room(
                "Trinity Manor",
                "Zachariah Dowey's Bedroom",
                "Zachariah Dowey",
                "retired priest",
            )

    if index == "Question Zachariah Dowey":
        if salt_bool:
            room.text = "Has it been twenty years already? We had a heck of a time trying to stop the Cult of Tsathoggua. Let me bless that salt for you."
            blessed_salt_bool = True
            cache.append({
                "item": "blessed salt",
                "description": "salt blessed by a priest"
            })
            cache = [item for item in cache if item["item"] != "salt"]
        else:
            room.text = "Where's the salt you want me to bless?"

    return attempts_trinity, salt_bool, blessed_salt_bool, cache, new_room


def handle_retirement_herring(action_room: Room, index: str, attempts_carehome: int) -> int:
    """
    Handle actions in the Hawkins Continuing-Care Community.

    Args:
        action_room (Room): The current room.
        index (str): The chosen action.
        attempts_carehome (int): Number of attempts to access the care home.

    Returns:
        int: Updated number of attempts.
    """
    if index == "Question Laurence Tureaud":
        if attempts_carehome < 2:  # Changed from 3 to 2 to match the test
            text_t = input("Who are you here to see? ")
            attempts_carehome += 1
            if text_t.strip() == "Sonny O'Sullivan":
                herring_bedroom = Room(
                    "Hawkins Continuing-Care Community",
                    "Sonny O'Sullivan's Bedroom",
                    "Sonny O'Sullivan",
                    "retired priest",
                    "Who are you? Bless your salt? Kids today and their strange fads.",
                )
                if hasattr(action_room, 'location') and isinstance(action_room.location, Location):
                    action_room.location.rooms.append(herring_bedroom)
            else:
                print("There is no one here by that name.")
        else:
            action_room.text = "You obviously don't know anyone here, please leave."
            attempts_carehome += 1

    return attempts_carehome


def handle_restaurant(index: str, salt_bool: bool) -> bool:
    """
    Handle actions in the restaurant.

    Args:
        index (str): The chosen action.
        salt_bool (bool): Whether the player has salt.

    Returns:
        bool: Updated salt_bool value.
    """
    if index == "Examine salt":
        print("You pick up the salt and put it in your pocket")
        return True
    return salt_bool


def handle_archdiocese(index: str):
    """
    Handle actions in the Archdiocese.

    Args:
        index (str): The chosen action.
    """
    if index == "Question Very Rev. Sean Fitzgerald":
        text_sean = "You are looking for priests that can bless salt? Maybe one of the retired priests will be able to help you. I'll print out the records."
        typingPrint(text_sean)
        print("\n")
        print_csv("priests.csv")


def handle_agency(index: str, attempts_jack: int, money: int) -> Tuple[int, int]:
    """
    Handle actions in Malone's Detective Agency.

    Args:
        index (str): The chosen action.
        attempts_jack (int): Number of attempts to get money from Jack.
        money (int): Current amount of money.

    Returns:
        Tuple[int, int]: Updated attempts_jack and money values.
    """
    if index == "Question Jack Malone":
        if attempts_jack == 0:
            text_malone = '"You want money for salt? Is this some weird TikTok thing?", Jack Malone says.'
            typingPrint(text_malone)
            print()
            money += 10
            typingPrint("Ronnie's dad gives her $10")
            attempts_jack += 1
        else:
            text_malone = '"More money? No chance. Get out of here." Jack Malone says.'
            typingPrint(text_malone)
            print()
    return attempts_jack, money


def handle_maeve(index: str, attempts_piggybank: int, money: int) -> Tuple[int, int]:
    """
    Handle actions in Maeve's house.

    Args:
        index (str): The chosen action.
        attempts_piggybank (int): Number of attempts to get money from the piggybank.
        money (int): Current amount of money.

    Returns:
        Tuple[int, int]: Updated attempts_piggybank and money values.
    """
    if index == "Examine Maeve's Piggybank":
        if attempts_piggybank == 0:
            print("The piggybank has $100")
            money += 100
            attempts_piggybank += 1
        else:
            print("The piggybank has no money")
    return attempts_piggybank, money


def handle_theo(action_room: Room, theo_bool: bool) -> bool:
    """
    Handle actions in Theo's house.

    Args:
        action_room (Room): The current room.
        theo_bool (bool): Whether Theo is available.

    Returns:
        bool: Updated theo_bool value.
    """
    if action_room.room == "Kitchen":
        print("You see Theo's mom and she says he has to stay home and do homework.")
        return False
    return theo_bool

def handle_basement_visit():
    """Handle the basement visit in the theatre."""
    typingPrint(
        "Performing a reverse image search on the mural, Maeve uncovered obscure texts on the Cthulhu mythos and Tsathoggua's insatiable hunger for power. Here, they realized a cult was determined to bring this eldritch horror into their world."
    )
    print()


def handle_school(action_room: Room):
    """
    Handle actions in the school.

    Args:
        action_room (Room): The current room.
    """
    if action_room.room == "Music Room":
        text = action_room.text or "You enter the Music Room."  # Provide a default text if None
        typingPrint(text)
        game_over("You lose")


def handle_max(action_room: Room, max_bool: bool) -> bool:
    """
    Handle actions in Max's house.

    Args:
        action_room (Room): The current room.
        max_bool (bool): Whether Max is available.

    Returns:
        bool: Updated max_bool value.
    """
    if action_room.room == "Kitchen":
        print("You see Max's grandparents are there to visit the family. He has to stay home and visit.")
        return False
    return max_bool


def handle_occult(index: str, money: int, cache: List[Dict[str, str]]) -> Tuple[int, List[Dict[str, str]]]:
    """
    Handle actions in the occult store.

    Args:
        index (str): The chosen action.
        money (int): Current amount of money.
        cache (List[Dict[str, str]]): The player's inventory.

    Returns:
        Tuple[int, List[Dict[str, str]]]: Updated money and cache values.
    """
    if index in ["Examine The Amulet of the Yoth", "Question Bridgett Collins"]:
        if money >= 100:
            text_collins = input("Of course, I have the perfect thing for you! It's The Amulet of the Yoth. If you break it, I'm sure it will do the job. It costs $100. \nDo you want to buy the amulet? y/n ")
            if text_collins.lower() in ["yes", "y"]:
                money -= 100
                cache.append({
                    "item": "The Amulet of the Yoth",
                    "description": "A dark circle embedded in a red stone - made to look like an eye"
                })
            else:
                print("Not knowing anything about amulets, you are hesitant to make such an expensive purchase. You decide to look for a second opinion.")
        else:
            print("I have the perfect thing for you, but you do not have enough money for it.")
    
    elif index == "Question Lady Drusilla":
        if money >= 20:
            teller_input = input("Would you like your fortune told? It doesn't cost much, but it will take some time.\nWould you like your fortune told? It will cost you $20 and an extra hour. y/n ")
            if teller_input.lower() in ["yes", "y"]:
                money -= 20
                fortune = "You have a very important task to complete and it's important to stay together -- even loved ones will try to stop you from your true calling. I see a hooded figure, he reveals his face and you recognize him as an authority figure. Now, I see a precious thing lying, waiting for you in the rubble. I hear an unearthly screeching noise, but you stop it with a machine. I see chaos, a fight ensues, but you triumph because you say the words."
                typingPrint(fortune)
            else:
                typingPrint("You say you don't have the time to have your fortune told.")
        else:
            print("Unfortunately you do not have enough money to have your fortune told.")
    
    return money, cache


def handle_palm(index: str, money: int) -> int:
    """
    Handle actions in the palm reading place.

    Args:
        index (str): The chosen action.
        money (int): Current amount of money.

    Returns:
        int: Updated money value.
    """
    if index == "Question Mme. Avalonia":
        if money >= 60:
            reading_request = input("Of course, I can do a palm reading....for the right price.\nDo you want a reading for $60? y/n ")
            if reading_request.lower() in ["yes", "y"]:
                money -= 60
                print()
                palm_reading = "I can tell you have fire hands by your long palms and short fingers. You are known to be passionate, confident, and industrious. You're driven by your desires and on a bad day you may lack tactfulness and empathy."
                typingPrint(palm_reading)
                print()
                print("You leave disappointed by the lack of information\n")
            else:
                print()
                print("You politely decline the offer.")
        else:
            print("You do not have enough money for a palm reading")
    return money


def handle_magic_box(index: str, hours: int, attempts_giles: int, money: int, blessed_salt_bool: bool, cache: List[Dict[str, str]]) -> Tuple[int, int, int, bool, List[Dict[str, str]]]:
    """
    Handle actions in The Magic Box.

    Args:
        index (str): The chosen action.
        hours (int): Remaining hours.
        attempts_giles (int): Number of attempts to convince Giles.
        money (int): Current amount of money.
        blessed_salt_bool (bool): Whether the player has blessed salt.
        cache (List[Dict[str, str]]): The player's inventory.

    Returns:
        Tuple[int, int, int, bool, List[Dict[str, str]]]: Updated values for hours, attempts_giles, money, blessed_salt_bool, and cache.
    """
    if index == "Examine Books on Demons, Magic, and Supernatural Creatures":
        book_input = input("A cursory glance of the books reveals no new information. If you spent more time, you could learn more.\nDo you want to spend more time studying the books? It will cost you 1 hour. y/n ")
        if book_input.lower() in ["yes", "y"]:
            hours -= 1
            typingPrint("Spending more time studying the books in The Magic Box paid off: You discover an old map of Hawkins and The Old Forrest is located where Whispering Pines Cemetery is now.")
            print()
    
    elif index == "Question Rupert Giles":
        if money >= 100 and attempts_giles < 2:
            print("I'm hesitant to sell you because I know what it can be used for.")
            attempts_giles += 1
        elif money >= 100 and attempts_giles >= 2:
            text_giles = input("You have me convinced, you obviously know what you are doing.\nDo you still want to buy the blessed salt for $100? y/n ")
            if text_giles.lower() in ["yes", "y"]:
                money -= 100
                blessed_salt_bool = True
                cache.append({
                    "item": "blessed salt",
                    "description": "salt blessed by a priest"
                })
                cache = [item for item in cache if item["item"] != "salt"]
                print("A word of advice: I know Mystic Minds has some amulets that are fake and won't prevent the coming of Tsathoggua. Unfortunately, I don't know where you can get the amulet that will work.")
            else:
                print("Good luck in your journey")
        else:
            print("You don't have enough money to buy blessed salt and it's probably good you don't.")
    
    elif index == "Examine an old wooden door":
        if check_lock(cache):
            pick = input("Do you want to pick the lock to open the door? y/n ")
            if pick.lower() in ["yes", "y"]:
                game_over("The largest wolf you have ever laid eyes on bursts through the door and immediately consumes all of you.")
            else:
                print("You decide against anymore snooping.")
        else:
            print("The door is locked and you are unable to get in.")
    
    return hours, attempts_giles, money, blessed_salt_bool, cache


def handle_library(index: str, locations: List[Union[Location, str]]):
    """
    Handle actions in the library.

    Args:
        index (str): The chosen action.
        locations (List[Union[Location, str]]): List of available locations.
    """
    if index == "Examine a replica map of Hawkins from 1873":
        cemetery = Location("Whispering Pine Cemetery", [Room("Whispering Pine Cemetery", "A clearing in the middle of the cemetery")])
        if cemetery not in locations:
            locations.insert(0, cemetery)


def handle_theatre(index: str, cache: List[Dict[str, str]], amulet_bool: bool) -> Tuple[List[Dict[str, str]], bool]:
    """
    Handle actions in the theatre.

    Args:
        index (str): The chosen action.
        cache (List[Dict[str, str]]): The player's inventory.
        amulet_bool (bool): Whether the player has the amulet.

    Returns:
        Tuple[List[Dict[str, str]], bool]: Updated cache and amulet_bool values.
    """
    if index == "Examine a shattered amulet":
        cache.append({
            "item": "a shattered amulet",
            "description": "Among the rubble in the basement of the dilapidated theatre, you find a broken amulet. You wished that you had looked at the artifacts more carefully when you were here before."
        })
        return cache, True
    return cache, amulet_bool


def handle_mall(index: str, money: int, cache: List[Dict[str, str]], salt_bool: bool) -> Tuple[int, List[Dict[str, str]], bool]:
    """
    Handle actions in the mall.

    Args:
        index (str): The chosen action.
        money (int): Current amount of money.
        cache (List[Dict[str, str]]): The player's inventory.
        salt_bool (bool): Whether the player has salt.

    Returns:
        Tuple[int, List[Dict[str, str]], bool]: Updated money, cache, and salt_bool values.
    """
    if index == "Examine salt":
        if money >= 2:
            buy_salt = input("Would you like to buy salt? It costs $2. y/n ")
            if buy_salt.lower() in ["y", "yes"]:
                money -= 2
                cache.append({
                    "item": "salt",
                    "description": "ordinary table salt"
                })
                salt_bool = True
            else:
                print("You put the salt down and leave")
        else:
            print("You don't have enough money for the salt.")
    return money, cache, salt_bool


# ... (previous code remains the same)

def handle_cemetery(theo_bool: bool, max_bool: bool, cache: List[Dict[str, str]], amulet_bool: bool, blessed_salt_bool: bool):
    """
    Handle actions in the cemetery.

    Args:
        theo_bool (bool): Whether Theo is available.
        max_bool (bool): Whether Max is available.
        cache (List[Dict[str, str]]): The player's inventory.
        amulet_bool (bool): Whether the player has the amulet.
        blessed_salt_bool (bool): Whether the player has blessed salt.
    """
    if not theo_bool:
        game_over("Amidst the chaos, Mr. Sinclair, the cult's leader, revealed himself as a formidable adversary. He possessed unnatural strength and knowledge and intended to become Tsathoggua's favoured disciple. You see Mr. Sinclair orchestrating the ritual, without Theo there, you are unable to stop the ritual.")
    
    typingPrint("Amidst the chaos, Mr. Sinclair, the cult's leader, revealed himself as a formidable adversary. He possessed unnatural strength and knowledge and intended to become Tsathoggua's favoured disciple. Despite his strength, he is no match for Theo's wits. In a heart-pounding battle, Theo used his quick thinking to disarm the cult leader, ending his reign of terror.")
    print()

    if max_bool:
        blocker_found = any(item["item"] == "a signal jammer" for item in cache)
        if blocker_found:
            typingPrint("Max sees the ring of speakers and gets the idea to cause interference using the signal jammer. Max hacked into the cult's speakers, blaring an ear-piercing frequency that disrupted their concentration.")
            print()
        else:
            game_over("Max sees the ring of speakers and gets the idea that he could cause interference using the signal jammer. Unfortunately, you never thought to pick up Jack Malone's signal jammer from his office. Unable to stop the speakers, you fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth.")
    else:
        game_over("Without Max there, your group doesn't know how to stop the cult's equipment from opening the portal for Tsathoggua. You are unable to stop the ritual.")

    if amulet_bool:
        if blessed_salt_bool:
            chant = input("What does Ronnie say? ")
            if chant.lower() in ["away tsathoggua", "away tsathoggua!"]:
                victory_sequence()
            else:
                game_over("Ronnie fails to say the chant correctly and in time. You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth.")
        else:
            game_over("Without the salt blessed by a priest, you are unable to stop the ritual. You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth.")
    else:
        game_over("Without the correct amulet, you are unable to stop the ritual. You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth.")


def victory_sequence():
    """
    Display the victory sequence and end the game.
    """
    victory_text = """
Ronnie read an incantation that weakened the cultists' connection to Tsathoggua, causing their summoned portal to falter.

As the portal closed and Tsathoggua's monstrous form receded, Ronnie knew they had averted a catastrophe. The authorities arrived to apprehend the cultists, and peace was restored to their town.

With the threat vanquished, Ronnie, Max, Maeve, and Theo looked at each other, their friendship stronger than ever. The shadows that had once loomed over their high school had been banished, but they knew that as supernatural detectives, they would always be ready to face whatever darkness lurked in the future.

As they left the cemetery, raindrops continued falling, symbolizing renewal and hope. With her hood pulled low, Ronnie looked ahead, ready for the next case that would come their way.
"""
    typingPrint(victory_text)
    sys.exit()


def main():
    """
    Main function to run the game.
    """
    intro_text()
    act_one()
    print()
    act_two()
    print()
    act_three()


if __name__ == "__main__":
    main()
import sys
from typing import List, Union, Tuple

from map import Location, Room
from inventory import Inventory
import helper


basement_visit: bool = False
solve_code: bool = False


def act_two(cache):
    """
    Run the second act of the game.

    Args:
        cache: List[Dict[str, str]]: Player's current inventory

    Returns:
        cache: List[Dict[str, str]]: Player's updated inventory
    """

    two_intro = """
Act II: A Whisper of Shadows
The Hawkins Factory was a dilapidated structure that loomed like a forgotten sentinel on the edge of town. As they entered its decaying interior, the air was thick with an eerie stillness; broken windows and graffiti-covered walls greeted Ronnie and her team.
"""
    helper.typingPrint(two_intro)
    print()

    locations, items = initialize_act_two()
    secret = Room(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    concession = Room("Orpheum Theater", "Concession Stand")
    auditorium = Room("Orpheum Theater", "Auditorium")
    basement = Room(
        "Orpheum Theater",
        "Theatre Basement",
        items=graffiti.item,
        item_description=graffiti.description,
    )
    graffiti = Inventory(
        "a graffitied wall",
        "In the bowels of the abandoned building, they found a hidden room filled with disturbing artifacts and a mural depicting a large furry toad.",
    )
    theatre = Location("Orpheum Theater", [auditorium, basement, concession])
    diary = Inventory("a diary", "a diary with pages filled with strange writings")
    while True:
        if basement_visit and solve_code:
            break

        print("\nWhere do you want to go?")
        action_location = helper.get_location(locations)

        if action_location == "Quit Game":
            sys.exit()

        leave_location, cache = helper.handle_location_options(action_location, cache)
        if leave_location:
            continue

        rooms = helper.get_rooms_for_location(action_location, locations)

        while True:
            if solve_code and basement_visit:
                break

            location_name = (
                action_location.location
                if isinstance(action_location, Location)
                else action_location
            )
            action_room = helper.get_room(rooms, location_name)

            if isinstance(action_room, str) and action_room.startswith("Leave"):
                break

            print(f"Going to {action_room.room}!\n")

            # Special case for Jack Malone's office
            if (
                action_room.room == "Office"
                and action_location == "Malone's Detective Agency"
            ):
                helper.game_over(
                    "You enter your dad's office to find his signal jammer. To your surprise, your father is there sitting at the desk."
                )

            if action_room == "Manager's Office":
                if not helper.check_lock():
                    continue
            print(f"Going to {action_room.room}!\n")
            if action_room == secret:
                print(
                    "The walls were adorned with cryptic symbols, and on the floor lay a diary with pages filled with strange writings."
                )
                print(
                    "Maeve remembers seeing one of those symbols spray painted above the back entrance of the dilapidated Orpheum Theater."
                )
                if theatre not in locations:
                    locations.insert(0, theatre)

            print(f"{action_room}\n")

            while True:
                print("What do you want to do?")
                index = helper.get_action(action_room, cache)

                if index == "Examine a diary":
                    solve_code, cache = helper.handle_diary_examination(
                        action_room, cache
                    )
                    if solve_code and basement_visit:
                        break

                # add secret room
                if index == f"Examine a shiny lever on a rusted machine":
                    print(
                        "You pull the lever and it opens a secret passage in the floor.\n"
                    )
                    if secret not in rooms:
                        rooms.insert(0, secret)
                        items.insert(0, diary)
                    break
                if index == f"Examine an old computer":
                    solve_code = helper.check_cipher(index, action_room)
                    break

                result = helper.check_room_action(index, action_room, items, cache)

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
    return cache, basement_visit, solve_code


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
    computer = Inventory(
        "the receptionist's computer",
        "Max hacks into the receptionist's computer while Theo stands outside on the lookout. Looking up all the missing students, they all had one thing in common: they are all enrolled in the same Journalism class.",
    )
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

    locations = [
        factory,
        agency,
        school,
        police,
        newspaper,
        "Quit Game",
    ]
    items = [kit, computer, posters, paper]

    return locations, items


def handle_basement_visit():
    """Handle the basement visit in the theatre."""
    helper.typingPrint(
        "Performing a reverse image search on the mural, Maeve uncovered obscure texts on the Cthulhu mythos and Tsathoggua's insatiable hunger for power. Here, they realized a cult was determined to bring this eldritch horror into their world."
    )
    print()

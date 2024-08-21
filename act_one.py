import helper
import sys
from typing import List, Union, Tuple, Dict

from map import Location, Room
from inventory import Inventory


def intro_text():
    """
    Print the game's title and introduction in a typewriter-style.
    """
    title = "Shadows in the Schoolyard\n\n"
    helper.typingPrint(title)
    intro = """
Act I: The Case Unveiled
Rain pounded the cracked pavement outside as Veronica "Ronnie" Malone leaned against the dimly lit hallway lockers, her hood low over her eyes. The teenage private investigator learned her detective skills from her father, a grizzled P.I. named Jack Malone. Ronnie had her own side hustle, taking on cases from her high school peers when needed.

Ronnie didn't work alone; she had a ragtag group of friends who helped her. There was Max, the tech genius who could hack into anything; Maeve, the bookworm with an uncanny ability to dig up information; and Theo, the fearless daredevil with a knack for getting them out of tight spots.

On that gloomy morning, a frantic girl named Lily approached Ronnie in hushed tones. "Veronica, you have to help me. My friend, Emily, she's gone. Disappeared without a trace."
"""
    helper.typingPrint(intro)


def act_one(cache) -> List[Dict[str, str]]:
    """
    Run the first act of the game.

    Args:
        cache: List[Dict[str, str]]: Player's initial inventory

    Returns:
        cache: List[Dict[str, str]]: Player's updated inventory
    """
    # Initialize locations and items
    locations, items = initialize_act_one()

    while True:
        print("\nWhere do you want to go?")
        action_location = helper.get_location(locations)

        if action_location == "Quit Game":
            sys.exit()
        elif action_location == "Hawkins Factory":
            break

        leave_location = helper.handle_location_options(action_location, cache)
        if leave_location:
            continue

        rooms = helper.get_rooms_for_location(action_location, locations)

        while True:
            print("What room do you want to go to?")
            action_room = helper.get_room(
                rooms,
                (
                    action_location.location
                    if isinstance(action_location, Location)
                    else action_location
                ),
            )

            if isinstance(action_room, str) and action_room.startswith("Leave"):
                break

            print(f"Going to {action_room.room}!\n")
            print(f"{action_room}\n")

            while True:
                print("What do you want to do?")
                index = helper.get_action(action_room, cache)
                result = helper.check_room_action(index, action_room, items, cache)

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
    helper.typingPrint(one_outro)
    return cache


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

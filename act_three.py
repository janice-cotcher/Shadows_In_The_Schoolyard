import helper
import sys
from typing import List, Dict, Union, Tuple, Optional

from map import Location, Room
from inventory import Inventory

solve_code: bool = False
basement_visit: bool = False


def act_three(cache: List[Dict[str, str]]):
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

    intro_text = "Act III: Unveiling the Horror\nThreats started closing in around them. Ronnie's friends began receiving ominous messages, taunting them to stop their investigation or face dire consequences. The stakes had never been higher.\n"
    helper.typingPrint(intro_text)
    print(get_instructions())

    locations, items = initialize_act_three()

    while hours > 0:
        print(f"You have {hours} hours left.")
        print("Where do you want to go?")
        action_location = helper.get_location(locations)

        if action_location == "Quit Game":
            sys.exit()

        leave_location = helper.handle_location_options(action_location, cache)
        if leave_location:
            hours -= 1
            continue

        rooms = helper.get_rooms_for_location(action_location, locations)

        while True:
            location_name = (
                action_location.location
                if isinstance(action_location, Location)
                else action_location
            )
            action_room = helper.get_room(rooms, location_name)

            if isinstance(action_room, str) and action_room.startswith("Leave"):
                break

            print(f"Going to {action_room.room}!\n")
            print(f"{action_room}\n")

            while True:
                print("What do you want to do?")
                index = helper.get_action(action_room, cache, money)

                # Handle special cases for different locations
                if action_location == retirement:
                    handle_retirement_manor(
                        action_room,
                        index,
                        attempts_trinity,
                        salt_bool,
                        blessed_salt_bool,
                        cache,
                    )
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
                    helper.handle_school(action_room)
                elif action_location == max:
                    handle_max(action_room, max_bool)
                elif action_location == occult:
                    handle_occult(index, money, cache)
                elif action_location == palm:
                    handle_palm(index, money)
                elif action_location == box:
                    handle_magic_box(
                        index, hours, attempts_giles, money, blessed_salt_bool, cache
                    )
                elif action_location == library:
                    handle_library(index, locations)
                elif action_location == theatre:
                    handle_theatre(index, cache, amulet_bool)
                elif action_location == mall:
                    handle_mall(index, money, cache, salt_bool)
                elif action_location == cemetery:
                    handle_cemetery(
                        theo_bool, max_bool, cache, amulet_bool, blessed_salt_bool
                    )

                result = helper.check_room_action(index, action_room, items, cache)
                if isinstance(result, tuple):
                    returned_dict, returned_bool = result
                    cache.append(returned_dict)
                else:
                    returned_bool = result

                if returned_bool:
                    break

        hours -= 1

    helper.game_over("You are too late and the time of Tsathoggua has come.")


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


def handle_retirement_manor(
    room: Room,
    index: str,
    attempts_trinity: int,
    salt_bool: bool,
    blessed_salt_bool: bool,
    cache: List[Dict[str, str]],
) -> Tuple[int, bool, bool, List[Dict[str, str]], Optional[Room]]:
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
            cache.append(
                {"item": "blessed salt", "description": "salt blessed by a priest"}
            )
            cache = [item for item in cache if item["item"] != "salt"]
        else:
            room.text = "Where's the salt you want me to bless?"

    return attempts_trinity, salt_bool, blessed_salt_bool, cache, new_room


def handle_retirement_herring(
    action_room: Room, index: str, attempts_carehome: int
) -> int:
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
                if hasattr(action_room, "location") and isinstance(
                    action_room.location, Location
                ):
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
        helper.typingPrint(text_sean)
        print("\n")
        helper.print_csv("priests.csv")


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
            helper.typingPrint(text_malone)
            print()
            money += 10
            helper.typingPrint("Ronnie's dad gives her $10")
            attempts_jack += 1
        else:
            text_malone = '"More money? No chance. Get out of here." Jack Malone says.'
            helper.typingPrint(text_malone)
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
        print(
            "You see Max's grandparents are there to visit the family. He has to stay home and visit."
        )
        return False
    return max_bool


def handle_occult(
    index: str, money: int, cache: List[Dict[str, str]]
) -> Tuple[int, List[Dict[str, str]]]:
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
            text_collins = input(
                "Of course, I have the perfect thing for you! It's The Amulet of the Yoth. If you break it, I'm sure it will do the job. It costs $100. \nDo you want to buy the amulet? y/n "
            )
            if text_collins.lower() in ["yes", "y"]:
                money -= 100
                cache.append(
                    {
                        "item": "The Amulet of the Yoth",
                        "description": "A dark circle embedded in a red stone - made to look like an eye",
                    }
                )
            else:
                print(
                    "Not knowing anything about amulets, you are hesitant to make such an expensive purchase. You decide to look for a second opinion."
                )
        else:
            print(
                "I have the perfect thing for you, but you do not have enough money for it."
            )

    elif index == "Question Lady Drusilla":
        if money >= 20:
            teller_input = input(
                "Would you like your fortune told? It doesn't cost much, but it will take some time.\nWould you like your fortune told? It will cost you $20 and an extra hour. y/n "
            )
            if teller_input.lower() in ["yes", "y"]:
                money -= 20
                fortune = "You have a very important task to complete and it's important to stay together -- even loved ones will try to stop you from your true calling. I see a hooded figure, he reveals his face and you recognize him as an authority figure. Now, I see a precious thing lying, waiting for you in the rubble. I hear an unearthly screeching noise, but you stop it with a machine. I see chaos, a fight ensues, but you triumph because you say the words."
                helper.typingPrint(fortune)
            else:
                helper.typingPrint(
                    "You say you don't have the time to have your fortune told."
                )
        else:
            print(
                "Unfortunately you do not have enough money to have your fortune told."
            )

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
            reading_request = input(
                "Of course, I can do a palm reading....for the right price.\nDo you want a reading for $60? y/n "
            )
            if reading_request.lower() in ["yes", "y"]:
                money -= 60
                print()
                palm_reading = "I can tell you have fire hands by your long palms and short fingers. You are known to be passionate, confident, and industrious. You're driven by your desires and on a bad day you may lack tactfulness and empathy."
                helper.typingPrint(palm_reading)
                print()
                print("You leave disappointed by the lack of information\n")
            else:
                print()
                print("You politely decline the offer.")
        else:
            print("You do not have enough money for a palm reading")
    return money


def handle_magic_box(
    index: str,
    hours: int,
    attempts_giles: int,
    money: int,
    blessed_salt_bool: bool,
    cache: List[Dict[str, str]],
) -> Tuple[int, int, int, bool, List[Dict[str, str]]]:
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
        book_input = input(
            "A cursory glance of the books reveals no new information. If you spent more time, you could learn more.\nDo you want to spend more time studying the books? It will cost you 1 hour. y/n "
        )
        if book_input.lower() in ["yes", "y"]:
            hours -= 1
            helper.typingPrint(
                "Spending more time studying the books in The Magic Box paid off: You discover an old map of Hawkins and The Old Forrest is located where Whispering Pines Cemetery is now."
            )
            print()

    elif index == "Question Rupert Giles":
        if money >= 100 and attempts_giles < 2:
            print("I'm hesitant to sell you because I know what it can be used for.")
            attempts_giles += 1
        elif money >= 100 and attempts_giles >= 2:
            text_giles = input(
                "You have me convinced, you obviously know what you are doing.\nDo you still want to buy the blessed salt for $100? y/n "
            )
            if text_giles.lower() in ["yes", "y"]:
                money -= 100
                blessed_salt_bool = True
                cache.append(
                    {"item": "blessed salt", "description": "salt blessed by a priest"}
                )
                cache = [item for item in cache if item["item"] != "salt"]
                print(
                    "A word of advice: I know Mystic Minds has some amulets that are fake and won't prevent the coming of Tsathoggua. Unfortunately, I don't know where you can get the amulet that will work."
                )
            else:
                print("Good luck in your journey")
        else:
            print(
                "You don't have enough money to buy blessed salt and it's probably good you don't."
            )

    elif index == "Examine an old wooden door":
        if helper.check_lock(cache):
            pick = input("Do you want to pick the lock to open the door? y/n ")
            if pick.lower() in ["yes", "y"]:
                helper.game_over(
                    "The largest wolf you have ever laid eyes on bursts through the door and immediately consumes all of you."
                )
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
        cemetery = Location(
            "Whispering Pine Cemetery",
            [
                Room(
                    "Whispering Pine Cemetery",
                    "A clearing in the middle of the cemetery",
                )
            ],
        )
        if cemetery not in locations:
            locations.insert(0, cemetery)


def handle_theatre(
    index: str, cache: List[Dict[str, str]], amulet_bool: bool
) -> Tuple[List[Dict[str, str]], bool]:
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
        cache.append(
            {
                "item": "a shattered amulet",
                "description": "Among the rubble in the basement of the dilapidated theatre, you find a broken amulet. You wished that you had looked at the artifacts more carefully when you were here before.",
            }
        )
        return cache, True
    return cache, amulet_bool


def handle_mall(
    index: str, money: int, cache: List[Dict[str, str]], salt_bool: bool
) -> Tuple[int, List[Dict[str, str]], bool]:
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
                cache.append({"item": "salt", "description": "ordinary table salt"})
                salt_bool = True
            else:
                print("You put the salt down and leave")
        else:
            print("You don't have enough money for the salt.")
    return money, cache, salt_bool


def handle_cemetery(
    theo_bool: bool,
    max_bool: bool,
    cache: List[Dict[str, str]],
    amulet_bool: bool,
    blessed_salt_bool: bool,
):
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
        helper.game_over(
            "Amidst the chaos, Mr. Sinclair, the cult's leader, revealed himself as a formidable adversary. He possessed unnatural strength and knowledge and intended to become Tsathoggua's favoured disciple. You see Mr. Sinclair orchestrating the ritual, without Theo there, you are unable to stop the ritual."
        )

    helper.typingPrint(
        "Amidst the chaos, Mr. Sinclair, the cult's leader, revealed himself as a formidable adversary. He possessed unnatural strength and knowledge and intended to become Tsathoggua's favoured disciple. Despite his strength, he is no match for Theo's wits. In a heart-pounding battle, Theo used his quick thinking to disarm the cult leader, ending his reign of terror."
    )
    print()

    if max_bool:
        blocker_found = any(item["item"] == "a signal jammer" for item in cache)
        if blocker_found:
            helper.typingPrint(
                "Max sees the ring of speakers and gets the idea to cause interference using the signal jammer. Max hacked into the cult's speakers, blaring an ear-piercing frequency that disrupted their concentration."
            )
            print()
        else:
            helper.game_over(
                "Max sees the ring of speakers and gets the idea that he could cause interference using the signal jammer. Unfortunately, you never thought to pick up Jack Malone's signal jammer from his office. Unable to stop the speakers, you fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
            )
    else:
        helper.game_over(
            "Without Max there, your group doesn't know how to stop the cult's equipment from opening the portal for Tsathoggua. You are unable to stop the ritual."
        )

    if amulet_bool:
        if blessed_salt_bool:
            chant = input("What does Ronnie say? ")
            if chant.lower() in ["away tsathoggua", "away tsathoggua!"]:
                victory_sequence()
            else:
                helper.game_over(
                    "Ronnie fails to say the chant correctly and in time. You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
                )
        else:
            helper.game_over(
                "Without the salt blessed by a priest, you are unable to stop the ritual. You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
            )
    else:
        helper.game_over(
            "Without the correct amulet, you are unable to stop the ritual. You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
        )


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
    helper.typingPrint(victory_text)
    sys.exit()


# Locations
retirement = Location("Trinity Manor", [Room("Trinity Manor", "Main Desk")])
retirement_herring = Location(
    "Hawkins Continuing-Care Community",
    [Room("Hawkins Continuing-Care Community", "Security Desk")],
)
restaurant = Location("Benny's Burgers", [Room("Benny's Burgers", "Diner Counter")])
archdiocese = Location(
    "Archdiocese of Hawkins", [Room("Archdiocese of Hawkins", "Chancery")]
)
agency = Location(
    "Malone's Detective Agency", [Room("Malone's Detective Agency", "Front Reception")]
)
maeve = Location(
    "Maeve's House",
    [Room("Maeve's House", "Kitchen"), Room("Maeve's House", "Maeve's Bedroom")],
)
theo = Location("Theo's House", [Room("Theo's House", "Kitchen")])
school = Location(
    "Hawkins Collegiate",
    [
        Room("Hawkins Collegiate", "Journalism Classroom"),
        Room("Hawkins Collegiate", "Front Office"),
        Room("Hawkins Collegiate", "Lunch Room"),
    ],
)
occult = Location(
    "Mystic Minds",
    [Room("Mystic Minds", "Store Front"), Room("Mystic Minds", "Fortune Teller Room")],
)
palm = Location(
    "Mme. Avalonia's Palm Readings",
    [Room("Mme. Avalonia's Palm Readings", "Palm Reading Room")],
)
box = Location(
    "The Magic Box",
    [Room("The Magic Box", "Retail Space"), Room("The Magic Box", "Backroom")],
)
library = Location(
    "Hawkins Public Library",
    [
        Room("Hawkins Public Library", "Mythology Section"),
        Room("Hawkins Public Library", "Local Maps"),
    ],
)
theatre = Location(
    "Orpheum Theater",
    [
        Room("Orpheum Theater", "Concession Stand"),
        Room("Orpheum Theater", "Auditorium"),
        Room("Orpheum Theater", "Theatre Basement"),
    ],
)
mall = Location(
    "Hawkins Shopping Centre",
    [Room("Hawkins Shopping Centre", "Hawkins Grocery & More")],
)
cemetery = Location(
    "Whispering Pine Cemetery",
    [Room("Whispering Pine Cemetery", "A clearing in the middle of the cemetery")],
)
factory = Location(
    "Hawkins Factory",
    [
        Room("Hawkins Factory", "Manager's Office"),
        Room("Hawkins Factory", "Rotting machinery"),
        Room("Hawkins Factory", "Catwalk - a narrow walkway above the factory floor"),
    ],
)
police = Location(
    "Hawkins Police Station", [Room("Hawkins Police Station", "Front Reception")]
)
catholic = Location(
    "St. Patrick's Parish Church",
    [
        Room("St. Patrick's Parish Church", "Administration Office"),
        Room("St. Patrick's Parish Church", "Cathedral's Basement"),
    ],
)
# Inventory

kit = Inventory("a lock pick kit", "Tools to unlock a locked door")
blocker = Inventory(
    "a signal jammer",
    "A hand-held, portable device that prevents wireless communications within a 15-meter radius.",
)
amulet = Inventory(
    "a shattered amulet",
    "Among the rubble in the basement of the dilapidated theatre, you find a broken amulet.",
)
salt_shaker = Inventory("salt", "ordinary table salt")

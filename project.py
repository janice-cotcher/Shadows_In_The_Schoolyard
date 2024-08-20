import sys
from map import Location, Room
from inventory import Inventory
from time import sleep
from act_three import act_three

cache = []
solve_code = False


def main():
    intro_text()
    act_one()
    print()
    act_two()
    print()
    act_three(cache)


def act_one():
    """Print an action menu and allow for continuous gameplay for act one"""
    # Act 1 locations
    text_sinclair = "All I know is Emily was researching gang activity in the school before she disappeared."
    journalism = Room(
        "Hawkins Collegiate",
        "Journalism Classroom",
        "Mr. Sinclair",
        "the journalism teacher",
        text_sinclair,
    )
    text_douglas = "Emily asked me for attendance records for four students. I told her I am not allowed to give out that information."
    school_reception = Room(
        "Hawkins Collegiate",
        "Front Office",
        "Mx. Douglas",
        "the receptionist",
        text_douglas,
    )
    text_kai = "She was being really secretive and distracted before she disappeared. She always had her nose in her notebook, trying to solve puzzles. Maybe her boss at the newspaper will know more."
    school_lunch = Room(
        "Hawkins Collegiate", "Lunch Room", "Kai", "Emily's friend", text_kai
    )
    school = Location(
        "Hawkins Collegiate",
        [school_lunch.room, journalism.room, school_reception.room],
    )

    posters = Inventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    text_forry = "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters."
    police_reception = Room(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    police = Location("Hawkins Police Station", [police_reception.room])

    paper = Inventory(
        "a torn piece of paper", 'The torn piece of paper reads: "Shift 7  a->h."'
    )
    text_editor = "Before she went missing, she was investigating the connection between the string of teen disappearance to the abandoned Hawkins Factory. I don't know much else, but you can check her desk."
    editor = Room(
        "Hawkins Daily News",
        "Editor's Office",
        "Sarah Bartlett",
        "Emily's boss",
        text_editor,
    )
    desk = Room(
        "Hawkins Daily News",
        "Emily's Desk",
        items=paper.item,
        item_description=paper.description,
    )
    newspaper = Location("Hawkins Daily News", [editor.room, desk.room])

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
        [agency_reception.room, agency_office.room, agency_closet.room],
    )

    act1_locations = [
        school.location,
        police.location,
        newspaper.location,
        agency.location,
    ]
    school_locations = [journalism, school_reception, school_lunch]
    police_locations = [police_reception]
    newspaper_locations = [editor, desk]
    agency_locations = [agency_reception, agency_office, agency_closet]
    act1_items = [paper, kit, blocker]

    while True:
        print()
        print("Where do you want to go first?")
        if "Quit Game" not in act1_locations:
            act1_locations.append("Quit Game")
        action_location = get_location(act1_locations)
        if action_location == school.location:
            rooms = school_locations
        elif action_location == police.location:
            rooms = police_locations
        elif action_location == newspaper.location:
            rooms = newspaper_locations
        elif action_location == agency.location:
            rooms = agency_locations
        elif action_location == "Quit Game":
            sys.exit()
        elif action_location == "Hawkins Factory":
            break
        if f"Leave {action_location}" not in rooms:
            rooms.append(f"Leave {action_location}")
        while True:
            print("What room do you want to go to?")
            action_room = get_room(rooms)
            if action_room == f"Leave {action_location}":
                break
            print(f"Going to {action_room.room}!\n")
            if action_room.room == "Emily's Desk":
                print(f"You are at Hawkins Daily News at Emily's Desk. You see a torn piece of paper.\n")
            else:
                print(f"{action_room}\n")
            while True:
                print("What do you want to do?")
                index = get_action(action_room)
                if action_room.person == f"Sarah Bartlett":
                    if "Hawkins Factory" not in act1_locations:
                        if "Quit Game" in act1_locations:
                            act1_locations.insert(
                                len(act1_locations) - 1, "Hawkins Factory"
                            )
                        else:
                            act1_locations.append("Hawkins Factory")
                result = check_room_action(index, action_room, act1_items)
                if isinstance(result, tuple):
                    returned_dict, returned_bool = result
                    cache.append(returned_dict)
                else:
                    returned_bool = result

                if returned_bool:
                    break
                else:
                    pass
    one_outro = """
The only lead they had was that Emily had been investigating the abandoned Hawkins Factory on the outskirts of town. Determined, they set out for the factory, rain-soaked streets giving way to overgrown paths.
"""
    typingPrint(one_outro)


def act_two():
    global solve_code
    basement_visit = False
    two_intro = """
Act II: A Whisper of Shadows
The Hawkins Factory was a dilapidated structure that loomed like a forgotten sentinel on the edge of town. As they entered its decaying interior, the air was thick with an eerie stillness; broken windows and graffiti-covered walls greeted Ronnie and her team.
"""
    typingPrint(two_intro)
    print()
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
    factory = Location("Hawkins Factory", [manager.room, machinery.room, catwalk.room])
    factory_locations = [
        manager,
        machinery,
        catwalk,
        "Leave Hawkins Factory",
        "Quit Game",
    ]

    kit = Inventory("a lock pick kit", "Tools to unlock a locked door")
    agency_reception = Room("Malone's Detective Agency", "Front Reception")
    text_malone = "What did I tell you kids about coming here after hours? I'm calling your parents and you are going straight home."
    agency_office = Room(
        "Malone's Detective Agency",
        "Office",
        "Jack Malone",
        "private investigator and Ronnie's father",
        text_malone,
    )
    agency_closet = Room(
        "Malone's Detective Agency",
        "Supply Closet",
        items=kit.item,
        item_description=kit.description,
    )
    agency = Location(
        "Malone's Detective Agency",
        [agency_reception.room, agency_office.room, agency_closet.room],
    )
    journalism = Room(
        "Hawkins Collegiate",
        "Journalism Classroom",
    )
    computer_break = "Max hacks into the receptionist's computer while Theo stands outside on the lookout. Looking up all the missing students, they all had one thing in common: they are all enrolled in the same Journalism class."
    computer = Inventory("the receptionist's computer", computer_break)
    school_reception = Room(
        "Hawkins Collegiate",
        "Front Office",
        items=computer.item,
        item_description=computer.description,
    )
    school_lunch = Room(
        "Hawkins Collegiate",
        "Lunch Room",
    )
    school = Location(
        "Hawkins Collegiate",
        [school_lunch.room, journalism.room, school_reception.room],
    )

    posters = Inventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg.",
    )
    text_forry = "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters."
    police_reception = Room(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    police = Location("Hawkins Police Station", [police_reception.room])

    paper = Inventory(
        "a torn piece of paper", 'The torn piece of paper reads: "Shift 7  a->h."'
    )
    editor = Room(
        "Hawkins Daily News",
        "Editor's Office",
    )
    desk = Room(
        "Hawkins Daily News",
        "Emily's Desk",
        items=paper.item,
        item_description=paper.description,
    )
    newspaper = Location("Hawkins Daily News", [editor.room, desk.room])

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
    theatre = Location(
        "Orpheum Theater", [auditorium.room, basement.room, concession.room]
    )

    school_locations = [journalism, school_reception, school_lunch]
    police_locations = [police_reception]
    agency_locations = [agency_reception, agency_office, agency_closet]
    theatre_locations = [concession, auditorium, basement]
    act2_locations = [
        factory.location,
        agency.location,
        school.location,
        police.location,
        newspaper.location,
    ]
    act2_items = [kit, diary]
    navigate_factory(
        factory_locations, manager, secret, act2_locations, theatre, act2_items
    )

    while True:
        print()
        if basement_visit and solve_code:
            break
        print("Where do you want to go?")
        if "Quit Game" not in act2_locations:
            act2_locations.append("Quit Game")
        action_location = get_location(act2_locations)
        if action_location == school.location:
            if not check_lock():
                continue
            else:
                rooms = school_locations
        elif action_location == police.location:
            rooms = police_locations
        elif action_location == newspaper.location:
            if not check_lock():
                continue
            else:
                typingPrint(
                    "The newspaper is closed for the evening and the door is locked. Luckily you have your dad's lock pick kit, so you easily unlock the door. Suddenly an alarm goes off, and security comes running. You are detained until the police come and arrest you for breaking and entering."
                )
                print()
                typingPrint("You lose!")
                sys.exit()
        elif action_location == factory.location:
            rooms = factory_locations
            navigate_factory(
                factory_locations, manager, secret, act2_locations, theatre, act2_items
            )

            if solve_code and basement_visit:
                break
            else:
                continue
        elif action_location == agency.location:
            rooms = agency_locations
        elif action_location == theatre.location:
            if not check_lock():
                continue
            else:
                rooms = theatre_locations
        if action_location == "Quit Game":
            sys.exit()
        if f"Leave {action_location}" not in rooms:
            rooms.append(f"Leave {action_location}")
        while True:
            if solve_code and basement_visit:
                break
            print("What room do you want to go to?")
            action_room = get_room(rooms)
            if action_room == f"Leave {action_location}":
                break
            print(f"Going to {action_room.room}!\n")
            if action_room.room == agency_office.room:
                typingPrint(
                    "You enter your dad's office to find his signal jammer. To your surprise, your father is there sitting at the desk.\n"
                )
                typingPrint(f"{text_malone}\n")
                typingPrint("You lose!")
                sys.exit()
            print(f"{action_room}\n")
            while True:
                print("What do you want to do?")
                index = get_action(action_room)
                if index == f"Examine a diary":
                    print("You find the following text in the diary:")
                    with open("cipher.txt", "r") as file:
                        lines = file.readlines()
                        print()
                        for line in lines:
                            print(line, end="")
                        print("\n")
                    solve_code = check_cipher(index, action_room)
                    if solve_code and basement_visit:
                        break
                result = check_room_action(index, action_room, act2_items)
                if isinstance(result, tuple):
                    returned_dict, returned_bool = result
                    cache.append(returned_dict)
                else:
                    returned_bool = result

                if returned_bool:
                    break
                else:
                    pass
                if action_room == basement:
                    basement_visit = True
                if index == f"Examine a graffitied wall":
                    typingPrint(
                        "Performing a reverse image search on the mural, Maeve uncovered obscure texts on the Cthulhu mythos and Tsathoggua's insatiable hunger for power. Here, they realized a cult was determined to bring this eldritch horror into their world."
                    )
                    print()
                    pass


def intro_text():
    """Prints title of the game in a typewriter-style"""
    title = "Shadows in the Schoolyard\n\n"
    typingPrint(title)
    intro = """
Act I: The Case Unveiled
Rain pounded the cracked pavement outside as Veronica "Ronnie" Malone leaned against the dimly lit hallway lockers, her hood low over her eyes. The teenage private investigator learned her detective skills from her father, a grizzled P.I. named Jack Malone. Ronnie had her own side hustle, taking on cases from her high school peers when needed.

Ronnie didn't work alone; she had a ragtag group of friends who helped her. There was Max, the tech genius who could hack into anything; Maeve, the bookworm with an uncanny ability to dig up information; and Theo, the fearless daredevil with a knack for getting them out of tight spots.

On that gloomy morning, a frantic girl named Lily approached Ronnie in hushed tones. "Veronica, you have to help me. My friend, Emily, she's gone. Disappeared without a trace."
"""
    typingPrint(intro)


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


def decoded(index, action_room):
    if index == f"Examine {action_room.items}":
        print("What does the coded message say? Ctrl-D to save it.")
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


def get_commands(message, length):
    """Get user input and convert the string to title case"""
    action_input = 0
    while True:
        try:
            action_input = int(input(message))
        except ValueError:
            pass
        if action_input <= 0 or action_input > length:
            pass
        else:
            return action_input


def navigate_factory(
    factory_locations, manager, secret, act2_locations, theatre, act2_items
):
    global solve_code
    while True:
        print("Where do you want to go?")
        action_room = get_room(factory_locations)
        if action_room == "Leave Hawkins Factory":
            break
        if action_room == "Quit Game":
            sys.exit()
        if action_room == manager:
            if not check_lock():
                continue
        print(f"Going to {action_room.room}!\n")
        if action_room == secret:
            print(
                "The walls were adorned with cryptic symbols, and on the floor lay a diary with pages filled with strange writings."
            )
            print(
                "Maeve remembers seeing one of those symbols spray painted above the back entrance of the dilapidated Orpheum Theater."
            )
            if theatre.location not in act2_locations:
                act2_locations.insert(0, theatre.location)

        print(f"{action_room}\n")
        while True:
            print("What do you want to do?")
            index = get_action(action_room)
            if index == f"Examine an old computer":
                solve_code = check_cipher(index, action_room)
                break

            if index == f"Examine a shiny lever on a rusted machine":
                print(
                    "You pull the lever and it opens a secret passage in the floor.\n"
                )
                if secret not in factory_locations:
                    factory_locations.insert(0, secret)
                break
            result = check_room_action(index, action_room, act2_items)
            if isinstance(result, tuple):
                returned_dict, returned_bool = result
                cache.append(returned_dict)
            else:
                returned_bool = result

            if returned_bool:
                break
            else:
                pass


def get_location(locations):
    for location in locations:
        print(f"{locations.index(location) + 1}. {location}")
    print()
    action_input = get_commands("Location: ", len(locations))
    print()
    action_location = locations[action_input - 1]
    print(f"Going to {action_location}!\n")
    return action_location


def get_room(rooms):
    for room in rooms:
        if isinstance(room, str):
            print(f"{rooms.index(room) + 1}. {room}")
        else:
            print(f"{rooms.index(room) + 1}. {room.room}")
    print()
    action_input = get_commands("Room: ", len(rooms))
    print()
    return rooms[action_input - 1]


def get_action(action_room):
    actions = []
    if action_room.person is not None:
        actions.append(f"Question {action_room.person}")
    if action_room.items is not None:
        actions.append(f"Examine {action_room.items}")
    if action_room.room is not None:
        actions.append(f"Leave {action_room.room}")
    if cache:
        actions.append(f"Check Inventory")
    for i in actions:
        print(f"{actions.index(i) + 1}. {i}")
    print()
    action_input = get_commands("Action: ", len(actions))
    return actions[action_input - 1]


def check_room_action(index, action_room, items):
    global cache, solve_code
    if index == f"Question {action_room.person}":
        print(f"{action_room.text}\n")
        return False
    if index == f"Examine a diary":
        print("You find the following text in the diary:")
        with open("cipher.txt", "r") as file:
            lines = file.readlines()
            print()
            for line in lines:
                print(line, end="")
            print()
            solve_code = decoded(index, action_room)
            print()
        temp_dict = {
            "item": action_room.items,
            "description": action_room.item_description,
        }
        if temp_dict not in cache:
            cache.append(temp_dict)
        return False

    if index == f"Examine {action_room.items}":
        print(f"{action_room.items}: {action_room.item_description}\n")
        # Create a temporary dictionary with the key-value pair
        for item in items:
            if action_room.items == item.item:
                temp_dict = {
                    "item": action_room.items,
                    "description": action_room.item_description,
                }
                # Check if the temporary dictionary is in the cache
                if temp_dict not in cache:
                    return temp_dict, False
        return False
    if index == f"Check Inventory":
        print("Inventory:")
        for item in cache:
            print(f"{item['item']}: {item['description']}")
        print()
        return False
    if index == f"Leave {action_room.room}":
        return True


def check_lock():
    found = False
    for dict in cache:
        if dict["item"] == "a lock pick kit":
            found = True
            print("The door was locked, but you used the lock pick kit to get in.\n")
            return found
    if not found:
        print("The door is locked, so you can't get in.\n")
        return found


# Typewriter effect. Source: https://www.101computing.net/python-typing-text-effect/


def typingPrint(text):
    text = text.lstrip()
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        sleep(0.05)


if __name__ == "__main__":
    main()

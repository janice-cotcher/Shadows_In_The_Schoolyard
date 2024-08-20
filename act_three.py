import sys
from map import Location, Room
from inventory import Inventory
from time import sleep
import csv
from tabulate import tabulate


def act_three(cache):
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
    typingPrint(intro_text)
    instructions = """
It is noon and Ronnie thinks that the ritual will take place tonight. There a couple of problems:
- you don't know where The Old Woods are
- you need a piece of a shattered amulet, but which amulet?
- you need salt blessed by a local priest
- each place you visit will make 1-hour pass and you only have 12 hours until midnight (no time penalty for visiting rooms within a location)
"""
    print(instructions)

    # Act 3 Locations
    posters = Inventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    text_forry = "Sorry, I don't have anymore information."
    police_reception = Room(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    police = Location("Hawkins Police Station", [police_reception])

    kit = Inventory("a lock pick kit", "Tools to unlock a locked door")
    blocker = Inventory(
        "a signal jammer",
        "A hand-held, portable device that prevents wireless communications within a 15-meter radius.",
    )
    agency_reception = Room("Malone's Detective Agency", "Front Reception")

    agency_office = Room(
        "Malone's Detective Agency",
        "Office",
        "Jack Malone",
        "private investigator and Ronnie's father",
        text='"Now get out of here," Jack Malone says.',
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
    manager = Room("Hawkins Factory", "Manager's Office")
    machinery = Room(
        "Hawkins Factory",
        "Rotting machinery",
    )
    catwalk = Room(
        "Hawkins Factory", "Catwalk - a narrow walkway above the factory floor"
    )
    secret = Room("Hawkins Factory", "Secret Room")
    factory = Location("Hawkins Factory", [manager, machinery, catwalk, secret])

    text_sinclair = """
You are surprised to see Mr. Sinclair and a dozen other adults all in hooded black cloaks removing large speakers from the music room. They drop what they are doing and overpower each of you.
Hours later you wake up in the back of a van; it is dark and you don't know where you are. The doors suddenly open and people in hooded black cloaks pull you out of the van. Outside you see you are at Whispering Pines Cemetery and Emily, Abed Nadir, Freya Day, Huan Li, and Grace Rosberg are tied up at the centre of a clearing.
As the ceremony begins, you and the other teens are sacrificed to Tsathoggua. In your dying breaths, you see a huge portal open and an expansive being with skin like a bat and a head like a toad.
"""
    music = Room(
        "Hawkins Collegiate",
        "Music Room",
        "Mr. Sinclair",
        "journalism teacher",
        text_sinclair,
    )
    open_door = Inventory(
        "open door",
        "You are surprised to see the Journalism Room's door open, but no one is inside. You hear noises coming from the music room.",
    )
    journalism = Room(
        "Hawkins Collegiate",
        "Journalism Classroom",
        items=open_door.item,
        item_description=open_door.description,
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
        [school_lunch, journalism, school_reception, music],
    )

    amulet_text = "Among the rubble in the basement of the dilapidated theatre, you find a broken amulet. You wished that you had looked at the artifacts more carefully when you were here before."
    amulet = Inventory("a shattered amulet", amulet_text)
    concession = Room("Orpheum Theater", "Concession Stand")
    auditorium = Room("Orpheum Theater", "Auditorium")
    basement = Room(
        "Orpheum Theater",
        "Theatre Basement",
        items=amulet.item,
        item_description=amulet.description,
    )
    theatre = Location("Orpheum Theater", [auditorium, basement, concession])

    foyer = Room("Church", "Foyer")
    baptist = Location("Hawkins Baptist Congregation", [foyer])
    fellowship = Location("Hawkins Fellowship Assembly", [foyer])
    lutheran = Location("First Lutheran Church", [foyer])
    presbyterian = Location("Second Presbyterian Church of Hawkins", [foyer])
    pentecostal = Location("The Good Shepherd's Flock", [foyer])
    orthodox = Location("St. Andrew's Greek Orthodox Church", [foyer])
    ascension = Location("Ascension Catholic Church", [foyer])
    assumption = Location("Cathedral of Assumption", [foyer])
    lady = Location("Church of Our Lady", [foyer])
    conception = Location("Immaculate Conception Catholic Church", [foyer])

    text_murphy = "Bless some salt? You might be able to find someone at St. Patrick's Parish Church who would be willing."
    church_foyer = Room(
        "Church of St. Peter the Rock",
        "Church Foyer",
        "Father Murphy",
        "priest",
        text=text_murphy,
    )
    peter = Location("Church of St. Peter the Rock", [church_foyer])

    text_ronald = "You want a priest to bless salt? That's a strange request. Sorry, I don't think we can complete that request."
    office = Room(
        "St. Patrick's Parish Church",
        "Administration Office",
        "Ronald Meredith",
        "parish administrative assistant",
        text_ronald,
    )
    text_ross = "Hmmm, if you want salt blessed by a priest it's best to check the Archdiocese's records. I think a vicar from about 20 years ago will be able to help you. Forget his name."
    church_basement = Room(
        "St. Patrick's Parish Church",
        "Cathedral's Basement",
        "Ross MacGarry",
        "parish custodian",
        text_ross,
    )
    catholic = Location("St. Patrick's Parish Church", [foyer, office, church_basement])

    text_tony = "You want me to bless some salt? I don't feel comfortable doing that."
    ministry = Room(
        "Archdiocese of Hawkins",
        "Ministries & Services",
        "Father Anthony Deutscher",
        "youth minister",
        text_tony,
    )

    chancery = Room(
        "Archdiocese of Hawkins",
        "Chancery",
        "Very Rev. Sean Fitzgerald",
        "vicar",
        '\n"Hope this helps," the vicar says.',
    )
    archdiocese = Location("Archdiocese of Hawkins", [ministry, chancery])

    main_desk = Room(
        "Trinity Manor", "Main Desk", "Phil Callahan", "security guard", "text_phil"
    )
    retirement_rooms = [main_desk]  # append bedroom

    retirement = Location("Trinity Manor", retirement_rooms)

    text_sonny = "Who are you? Bless your salt? Kids today and their strange fads."

    herring_reception = Room(
        "Hawkins Continuing-Care Community",
        "Security Desk",
        "Laurence Tureaud",
        "security guard",
        "text_t",
    )

    herring_rooms = [herring_reception]  # append bedroom
    retirement_herring = Location("Hawkins Continuing-Care Community", herring_rooms)

    # occult store rooms
    fake_amulet = Inventory(
        "The Amulet of the Yoth",
        "A dark circle embedded in a red stone - made to look like an eye",
    )

    storefront = Room(
        "Mystic Minds",
        "Store Front",
        "Bridgett Collins",
        "shop owner",
        "text_collins",
        fake_amulet.item,
        fake_amulet.description,
    )

    teller = Room(
        "Mystic Minds",
        "Fortune Teller Room",
        "Lady Drusilla",
        "fortune teller",
        "lady_text",
    )
    occult = Location("Mystic Minds", [storefront, teller])

    reading = Room(
        "Mme. Avalonia's Palm Readings",
        "Palm Reading Room",
        "Mme. Avalonia",
        "palm reader",
        "text_palm",
    )
    palm = Location("Mme. Avalonia's Palm Readings", [reading])

    books = Inventory("Books on Demons, Magic, and Supernatural Creatures")

    box_library = Room(
        "The Magic Box", "Library", items=books.item, item_description=books.description
    )
    # locked door with a monster behind it
    door = Inventory(
        "an old wooden door",
        "The door has a large, ancient padlock. It should be easy to pick.",
    )
    box_basement = Room(
        "The Magic Shop",
        "The Magic Shop's Basement",
        items=door.item,
        item_description=door.description,
    )
    salt_shaker = Inventory("salt", "ordinary table salt")
    blessed_salt = Inventory("blessed salt", "salt blessed by a priest")
    shop = Room(
        "The Magic Shop",
        "Retail Space",
        "Rupert Giles",
        "shop co-owner",
        "text_giles",
        items=blessed_salt.item,
        item_description=blessed_salt.description,
    )
    text_anya = "You aren't allowed back here! Leave immediately."
    backroom = Room(
        "The Magic Shop", "Backroom", "Anya Jenkins", "shop co-owner", text_anya
    )
    box = Location("The Magic Box", [box_library, box_basement, shop, backroom])
    grocery = Room(
        "Hawkins Shopping Centre",
        "Hawkins Grocery & More",
        items=salt_shaker.item,
        item_description=salt_shaker.description,
    )
    mall = Location("Hawkins Shopping Centre", [grocery])

    myth = Room("Hawkins Public Library", "Mythology Section")
    old_map = Inventory(
        "a replica map of Hawkins from 1873",
        "The oldest town map you can find shows The Old Forrest where The Whispering Pines Cemetery is today.",
    )
    map_section = Room(
        "Hawkins Public Library",
        "Local Maps",
        items=old_map.item,
        item_description=old_map.description,
    )
    library = Location("Hawkins Public Library", [map_section, myth])

    dining = Room(
        "Benny's Burgers",
        "Diner Counter",
        items=salt_shaker.item,
        item_description=salt_shaker.description,
    )
    restaurant = Location("Benny's Burgers", [dining])
    theo_kitchen = Room("Theo's House", "Kitchen")
    theo = Location("Theo's House", [theo_kitchen])

    max_kitchen = Room("Max's House", "Kitchen")
    max = Location("Max's House", [max_kitchen])
    cupboard = Inventory(
        "Kitchen Cupboard",
        "The cupboard contains no salt, but Maeve remembers she has money in her bedroom.",
    )
    maeve_kitchen = Room(
        "Maeve's House",
        "Kitchen",
        items=cupboard.item,
        item_description=cupboard.description,
    )

    piggybank = Inventory("Maeve's Piggybank", "A ceramic pig that holds money")
    maeve_bedroom = Room(
        "Maeve's House",
        "Maeve's Bedroom",
        items=piggybank.item,
        item_description=piggybank.description,
    )
    maeve = Location("Maeve's House", [maeve_kitchen, maeve_bedroom])

    speakers = Inventory(
        "Speakers from the School",
        "A circle of large speakers in the middle of the cemetery",
    )
    centre = Room(
        "Whispering Pine Cemetery",
        "A clearing in the middle of the cemetery",
        items=speakers.item,
        item_description=speakers.description,
    )
    cemetery = Location("Whispering Pine Cemetery", [centre])
    act3_locations = [
        school,
        factory,
        theatre,
        police,
        agency,
        baptist,
        fellowship,
        lutheran,
        presbyterian,
        pentecostal,
        orthodox,
        ascension,
        assumption,
        lady,
        conception,
        peter,
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
        max,
        maeve,
    ]
    act3_locations.sort(key=lambda instance: instance.location)

    act3_items = [kit, blocker, amulet, salt_shaker]
    num_input = 0
    while True:
        if hours <= 0:
            typingPrint("You are too late and the time of Tsathoggua has come.")
            typingPrint("You lose")
            sys.exit()
        print(f"You have {12 - num_input} hours left.")
        num_input += 1
        print("Where do you want to go?")
        if "Quit Game" not in act3_locations:
            act3_locations.append("Quit Game")
        action_location = get_location(act3_locations)
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
                # Get into Trinity Manor
                if action_location == retirement:
                    if index == "Question Phil Callahan":
                        if attempts_trinity < 3:
                            text_phil = input("Who are you here to see? ")
                            attempts_trinity += 1
                        else:
                            main_desk.text = (
                                "You obviously don't know anyone here, please leave."
                            )
                        if text_phil.strip() == "Zachariah Dowey":
                            retirement_bedroom = Room(
                                "Trinity Manor",
                                "Zachariah Dowey's Bedroom",
                                "Zachariah Dowey",
                                "retired priest,
                            )
                            if retirement_bedroom not in retirement_rooms:
                                retirement_rooms.append(retirement_bedroom)
                            break
                        else:
                            print("There's no one here by that name.")
                            pass
                    if index == "Question Zachariah Dowey":
                        if salt_bool:
                            retirement_bedroom.text = "Has it been twenty years already? We had a heck of a time trying to stop the Cult of Tsathoggua. Let me bless that salt for you."
                            blessed_salt_bool = True
                            temp_dict = {
                                "item": blessed_salt.item,
                                "description": blessed_salt.description,
                            }
                            cache.append(temp_dict)
                            # source: https://www.geeksforgeeks.org/python-removing-dictionary-from-list-of-dictionaries/
                            for i in range(len(cache)):
                                if cache[i]["item"] == "salt":
                                    del cache[i]
                                    break
                        else:
                            retirement_bedroom.text = (
                                "Where's the salt you want me to bless?"
                            )

                # Redherring Priest location - Hawkins Continuing-Care Community
                elif action_location == retirement_herring:
                    if index == "Question Laurence Tureaud":
                        if attempts_carehome < 3:
                            text_t = input("Who are you here to see? ")
                            attempts_carehome += 1
                            if text_t.strip() == "Sonny O'Sullivan":
                                herring_bedroom = Room(
                                    "Hawkins Continuing-Care Community",
                                    "Sonny O'Sullivan's Bedroom",
                                    "Sonny O'Sullivan",
                                    "reitred priest",
                                    text_sonny,
                                )
                                if herring_bedroom not in herring_rooms:
                                    herring_rooms.append(herring_bedroom)
                                    break
                            else:
                                print("There is no one here by that name.")
                                pass
                        else:
                            herring_reception.text = (
                                "You obviously don't know anyone here, please leave."
                            )

                elif action_location == restaurant:
                    if index == "Examine salt":
                        print("You pick up the salt and put in your pocket")
                        salt_bool = True
                # Get records from the Archdioceses
                elif action_location == archdiocese:
                    if index == "Question Very Rev. Sean Fitzgerald":
                        text_sean = "You are looking for priests that can bless salt? Maybe one of the retired priests will be able to help you. I'll print out the records."
                        typingPrint(text_sean)
                        print("\n")
                        print_csv("priests.csv")
                elif action_location == agency:
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
                elif action_location == maeve:
                    if index == "Examine Maeve's Piggybank":
                        if attempts_piggybank == 0:
                            print("The piggybank has $100")
                            money += 100
                            attempts_piggybank += 1
                        else:
                            print("The piggybank has no money")
                elif action_location == theo:
                    if action_room.room == theo_kitchen.room:
                        print(
                            "You see Theo's mom and she says he has to stay home and do homework."
                        )
                        theo_bool = False
                elif action_location == school:
                    if action_room.room == music.room:
                        typingPrint(text_sinclair)
                        typingPrint("You lose")
                        sys.exit()
                elif action_location == max:
                    if action_room.room == max_kitchen.room:
                        print(
                            "You see Max's grandparents are there to visit the family. He has to stay home and visit."
                        )
                        max_bool = False

                # Mystic Minds Storefront
                elif action_location == occult:
                    if (
                        index == "Examine The Amulet of the Yoth"
                        or index == "Question Bridgett Collins"
                    ):
                        if money >= 100:
                            text_collins = input(
                                "Of course, I have the perfect thing for you! It's The Amulet of the Yoth. If you break it, I'm sure it will do the job. It costs $100. \n Do you want to buy the amulet? y/n "
                            )
                            storefront.text = text_collins
                            if text_collins.lower() in ["yes", "y"]:
                                money = money - 100
                                temp_dict = {
                                    "item": fake_amulet.item,
                                    "description": fake_amulet.description,
                                }
                                if temp_dict not in cache:
                                    cache.append(temp_dict)
                                storefront.text = "Sorry, I can't help you with anymore"
                            else:
                                storefront.text = "Not knowing anything about amulets, you are hesitant to make such an expensive purchase. You decide to look for a second opinion.\n"
                        else:
                            storefront.text = "I have the perfect thing for you, but you do not have enough money for it."
                    # Mystic Minds fortune told
                    if index == "Question Lady Drusilla":
                        if money > 20:
                            teller_input = input(
                                "Would you like your fortune told? It doesn't cost much, but it will take some time.\n Would like your fortune told? It will cost you $20 and an extra hour. y/n "
                            )
                            teller.text = teller_input
                            if teller_input in ["yes", "y"]:
                                money -= 20
                                hours -= 1
                                fortune = "You have a very important task to complete and it's important to stay together -- even loved ones will try to stop you from your true calling. I see a hooded figure, he reveals his face and you recognize him as an authority figure. Now, I see a precious thing lying, waiting for you in the rubble. I hear an unearthly screeching noise, but you stop it with a machine. I see chaos, a fight ensues, but you triumph because you say the words."
                                typingPrint(fortune)
                                teller.text = "I can't help you with anything else."
                            else:
                                typingPrint(
                                    "You say you don't have the time to have your fortune told."
                                )
                                teller.text = "I can't help you with anything else."
                        else:
                            teller.text = "Unfortunately you do not have enough money to have your fortune told."

                # Palming reading
                elif action_location == palm:
                    if index == "Question Mme. Avalonia":
                        if money > 60:
                            reading_request = input(
                                "Of course, I can do a palm reading....for the right price.\n Do you want a reading for $60? y/n "
                            )
                            reading.text = reading_request
                            if reading_request.lower() in ["yes", "y"]:
                                money = money - 60
                                print()
                                palm_reading = "I can tell you have fire hands by your long palms and short fingers. You are known to be passionate, confident, and industrious. You're driven by your desires and on a bad day you may lack tactfulness and empathy."
                                typingPrint(palm_reading)
                                print()
                                print(
                                    "You leave disappointed by the lack of information\n"
                                )
                                reading.text = '"Sorry, I can\'t help you with anything else" says the palm reader.'
                            else:
                                print()
                                print("You politely decline the offer.")
                                reading.text = '"Sorry, I can\'t help you with anything else" says the palm reader.'
                        else:
                            reading.text = (
                                "You do not have enough money for a palm reading"
                            )

                # Magic Box Library
                elif action_location == box:
                    if (
                        index
                        == "Examine Books on Demons, Magic, and Supernatural Creatures"
                    ):
                        book_input = input(
                            "A cursory glance of the books reveals no new information. If you spent more time, you could learn more.\n Do you want to spend more time studying the books? It will cost you 1 hour. y/n "
                        )
                        books.description = book_input
                        if book_input.lower() in ["yes", "y"]:
                            hours -= 1
                            typingPrint(
                                "Spending more time studying the books in The Magic Box paid off: You discover an old map of Hawkins and The Old Forrest is located where Whispering Pines Cemetery is now."
                            )
                            print()
                            if cemetery not in act3_locations:
                                act3_locations.insert(0, cemetery)
                    if index == "Question Rupert Giles":
                        if money >= 100 and attempts_giles < 2:
                            shop.text = "I'm hesitant to sell you because I know what I can be used for."
                            attempts_giles += 1
                        elif money >= 100 and attempts_giles >= 2:
                            text_giles = input(
                                "You have me convinced, you obviously know what you are doing.\n Do you still want to buy the blessed salt for $100? y/n "
                            )
                            shop.text = text_giles
                            if text_giles.lower() in ["yes", "y"]:
                                money -= 100
                                blessed_salt_bool = True
                                temp_dict = {
                                    "item": blessed_salt.item,
                                    "description": blessed_salt.description,
                                }
                                if temp_dict not in cache:
                                    cache.append(temp_dict)
                                # source: https://www.geeksforgeeks.org/python-removing-dictionary-from-list-of-dictionaries/
                                for i in range(len(cache)):
                                    if cache[i]["item"] == "salt":
                                        del cache[i]
                                        break
                                shop.text = "A word of advice: I know Mystic Minds has some amulets that are fake and won't prevent the coming of Tsathoggua. Unfortunately, I don't know where you can get the amulet that will work."
                            else:
                                shop.text = "Good luck in your journey"
                        else:
                            shop.text = "You don't have enough money to buy blessed salt and it's probably good you don't."
                    if index == "Examine an old wooden door":
                        if check_lock(cache):
                            pick = input(
                                "Do you want to pick the lock to open the door? y/n "
                            )
                            if pick.lower() in ["yes", "y"]:
                                typingPrint(
                                    "The largest wolf you have ever laid eyes on bursts through the door and immediately consumes all of you."
                                )
                                typingPrint("You lose")
                                sys.exit()
                            else:
                                print("You decide against anymore snooping.")
                        else:
                            print("The door is locked and you are unable to get in.")
                elif action_location == library:
                    if index == "Examine a replica map of Hawkins from 1873":
                        act3_locations.insert(0, cemetery)
                elif action_location == theatre:
                    if index == "Examine a shattered amulet":
                        temp_dict = {
                            "item": amulet.item,
                            "description": amulet.description,
                        }
                        cache.append(temp_dict)
                        amulet_bool = True
                elif action_location == mall:
                    if index == "Examine salt":
                        if money >= 2:
                            buy_salt = input(
                                "Would you like to buy salt? It costs $2. y/n "
                            )
                            if buy_salt in ["y", "yes"]:
                                money -= 2
                                temp_dict = {
                                    "item": salt_shaker.item,
                                    "description": salt_shaker.description,
                                }
                                cache.append(temp_dict)
                                salt_bool = True
                            else:
                                print("You put the salt down and leave")
                        else:
                            print("You don't have enough money for the salt.")
                elif action_location == cemetery:
                    if theo_bool:
                        typingPrint(
                            "Amidst the chaos, Mr. Sinclair, the cult's leader, revealed himself as a formidable adversary. He possessed unnatural strength and knowledge and intended to become Tsathoggua's favoured disciple. Despite his strength, he is no match for Theo's wits. In a heart-pounding battle, Theo used his quick thinking to disarm the cult leader, ending his reign of terror."
                        )
                        print()
                    else:
                        typingPrint(
                            "Amidst the chaos, Mr. Sinclair, the cult's leader, revealed himself as a formidable adversary. He possessed unnatural strength and knowledge and intended to become Tsathoggua's favoured disciple. You see Mr. Sinclair orchestrating the ritual, without Theo there, you are unable to stop the ritual."
                        )
                        print()
                        typingPrint("You lose")
                        print()
                        sys.exit()
                    if max_bool:
                        blocker_found = False
                        for item in cache:
                            if item["item"] == "a signal jammer":
                                typingPrint(
                                    "Max sees the ring of speakers and gets the idea to cause interference using the signal jammer. Max hacked into the cult's speakers, blaring an ear-piercing frequency that disrupted their concentration."
                                )
                                print()
                                blocker_found = True
                                break
                        if not blocker_found:
                            typingPrint(
                                "Max sees the ring of speakers and gets the idea that he could cause interference using the signal jammer. Unfortunately, you never thought to pick up Jack Malone's signal jammer from his office."
                            )
                            print()
                            typingPrint(
                                "Unable to stop the speakers, you fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
                            )
                            print()
                            typingPrint("You lose")
                            print()
                            sys.exit()
                    else:
                        typingPrint(
                            "Without Max there, your group doesn't know how to stop the cult's equipment from opening the portal for Tsathoggua. You are unable to stop the ritual."
                        )
                        print()
                        typingPrint("You lose")
                        print()
                        sys.exit()
                    if amulet_bool:
                        if blessed_salt_bool:
                            chant = input("What does Ronnie say? ")
                            if (
                                chant == "Away Tsathoggua"
                                or chant == "Away Tsathoggua!"
                            ):
                                typingPrint(
                                    "Ronnie read an incantation that weakened the cultists' connection to Tsathoggua, causing their summoned portal to falter."
                                )
                                print()
                                typingPrint(
                                    """
As the portal closed and Tsathoggua's monstrous form receded, Ronnie knew they had averted a catastrophe. The authorities arrived to apprehend the cultists, and peace was restored to their town.

With the threat vanquished, Ronnie, Max, Maeve, and Theo looked at each other, their friendship stronger than ever. The shadows that had once loomed over their high school had been banished, but they knew that as supernatural detectives, they would always be ready to face whatever darkness lurked in the future.

As they left the cemetery, raindrops continued falling, symbolizing renewal and hope. With her hood pulled low, Ronnie looked ahead, ready for the next case that would come their way.
"""
                                )
                                print()
                                sys.exit()
                            else:
                                typingPrint(
                                    "Ronnie fails to say the chant correctly and in time."
                                )
                                print()
                                typingPrint(
                                    "You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
                                )
                                print()
                                typingPrint("You lose")
                                print()
                                sys.exit()
                        else:
                            typingPrint(
                                "Without the salt blessed by a priest, you are unable to stop the ritual."
                            )
                            print()
                            typingPrint(
                                "You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
                            )
                            print()
                            typingPrint("You lose")
                            print()
                            sys.exit()
                    else:
                        typingPrint(
                            "Without the correct amulet, you are unable to stop the ritual."
                        )
                        print()
                        typingPrint(
                            "You fail to stop the ritual, and Tsathoggua comes through the portal and destroys the Earth."
                        )
                        print()
                        typingPrint("You lose")
                        print()
                        sys.exit()
                result = check_room_action(index, action_room, act3_items, cache)
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
    first = locations[::3]
    second = locations[1::3]
    third = locations[2::3]
    for a, b, c in zip(first, second, third):
        print(
            "{:<50} {:<50} {:<50}".format(
                get_location_string(a, locations),
                get_location_string(b, locations),
                get_location_string(c, locations),
            )
        )
    if len(locations) == 31:
        print("{:<50}".format(get_location_string(locations[-1], locations)))
    elif len(locations) == 32:
        print(
            "{:<50} {:<50}".format(
                get_location_string(locations[-2], locations),
                get_location_string(locations[-1], locations),
            )
        )
    print()
    action_input = get_commands("Location: ", len(locations))
    print()
    action_location = locations[action_input - 1]
    if isinstance(action_location, Location):
        print(f"Going to {action_location.location}!\n")
    return action_location


def get_location_string(location, locations):
    if isinstance(location, Location):
        return f"{locations.index(location) + 1}. {location.location}"
    else:
        return f"{locations.index(location) + 1}. {location}"


def get_commands(message, length):
    """Get user input and convert the string to titlecase"""
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


def get_action(action_room, money, cache):
    actions = []
    if action_room.person is not None:
        actions.append(f"Question {action_room.person}")
    if action_room.items is not None:
        actions.append(f"Examine {action_room.items}")
    if action_room.room is not None:
        actions.append(f"Leave {action_room.room}")
    if money > 0:
        print(f"You have ${money}.")
    if cache:
        actions.append(f"Check Inventory")
    for i in actions:
        print(f"{actions.index(i) + 1}. {i}")
    print()
    action_input = get_commands("Action: ", len(actions))
    return actions[action_input - 1]


def print_csv(file):
    with open(file, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        print(tabulate(data, headers="firstrow"))


def typingPrint(text):
    text = text.lstrip()
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        sleep(0.05)


def check_lock(cache):
    found = False
    for dict in cache:
        if dict["item"] == "a lock pick kit":
            found = True
            print("The door was locked, but you used the lock pick kit to get in.\n")
            return found
    if not found:
        print("The door is locked, so you can't get in.\n")
        return found


def check_room_action(index, action_room, items, cache):
    if index == f"Question {action_room.person}":
        print(f"{action_room.text}\n")
        return False
    if index == f"Examine {action_room.items}":
        if action_room.item_description:
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
            # print(item)
            print(f"{item['item']} : {item['description']}")
        print()
        return False
    if index == f"Leave {action_room.room}":
        return True


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


# act_three(cache)

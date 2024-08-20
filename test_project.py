import project
from act_three import act_three
import pytest
from unittest.mock import patch


class MockInventory:
    def __init__(self, item, description=None):
        self.item = item
        self.description = description

    def __str__(self):
        return f"{self.item}"


class MockRoom:
    def __init__(
        self,
        location,
        room,
        person=None,
        description=None,
        text=None,
        items=None,
        item_description=None,
    ):
        self.location = location
        self.room = room
        self.person = person
        self.description = description
        self.items = items
        self.text = text
        self.item_description = item_description

    def __str__(self):
        if self.person and self.items:
            return f"You are at {self.location} in the {self.room}. You see {self.person}, {self.description}. You also see {self.items}."
        elif self.person and not self.items:
            return f"You are at {self.location} in the {self.room}. You see {self.person}, {self.description}."
        elif not self.person and self.items:
            return (
                f"You are at {self.location} in the {self.room}. You see {self.items}."
            )
        else:
            return f"You are at {self.location} in the {self.room}. You see no one or no items of interest."


def test_act_one_quit(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Quit Game")


def test_act_one_factory(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Hawkins Factory")


def test_act_one_school_journalism(monkeypatch):
    inputs = iter(
        [
            "Hawkins Collegiate",
            "Journalism Classroom",
            "Question Mr. Sinclair",
            "Leave Journalism Classroom",
            "Leave Hawkins Collegiate",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_one_police(monkeypatch):
    inputs = iter(
        [
            "Hawkins Police Station",
            "Front Reception",
            "Question Officer Braydon Forry",
            "Examine Missing posters",
            "Leave Front Reception",
            "Leave Hawkins Police Station",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_one_agency(monkeypatch):
    inputs = iter(
        [
            "Malone's Detective Agency",
            "Office",
            "Examine a signal jammer",
            "Check Inventory",
            "Leave Office",
            "Leave Malone's Detective Agency",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_one_news(monkeypatch):
    inputs = iter(
        [
            "Hawkins Daily News",
            "Editor's Office",
            "Question Sarah Bartlett",
            "Leave Editor's Office",
            "Leave Hawkins Daily News",
            "Hawkins Factory",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_two_factory_diary(monkeypatch):
    with open("decoded.txt", "r") as file:
        inputs = [
            "Hawkins Daily News",
            "Editor's Office",
            "Question Sarah Bartlett",
            "Leave Editor's Office",
            "Leave Hawkins Daily News",
            "Hawkins Factory",
            "Rotting machinery",
            "Examine a shiny lever on a rusted machine",
            "Secret Room",
            "Examine a diary",
        ]
        inputs.extend(file.readlines())
        inputs = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_two(monkeypatch):
    with open("decoded.txt", "r") as file:
        inputs = [
            "Malone's Detective Agency",
            "Office",
            "Examine a signal jammer",
            "Leave Office",
            "Supply Closet",
            "Examine a lock pick kit",
            "Leave Supply Closet",
            "Leave Malone's Detective Agency",
            "Hawkins Daily News",
            "Editor's Office",
            "Question Sarah Bartlett",
            "Leave Editor's Office",
            "Leave Hawkins Daily News",
            "Hawkins Factory",
            "Rotting machinery",
            "Examine a shiny lever on a rusted machine",
            "Secret Room",
            "Examine a diary",
        ]
        inputs.extend(file.readlines())
        inputs.extend(
            [
                "Leave Secret Room",
                "Leave Hawkins Factory",
                "Orpheum Theater",
                "Theatre Basement",
                "Examine a graffitied wall",
                "Leave Theatre Basement",
                "Leave Orpheum Theater",
            ]
        )
        inputs = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_three(monkeypatch):
    with open("decoded.txt", "r") as file:
        inputs = [
            "Malone's Detective Agency",
            "Office",
            "Examine a signal jammer",
            "Leave Office",
            "Supply Closet",
            "Examine a lock pick kit",
            "Leave Supply Closet",
            "Leave Malone's Detective Agency",
            "Hawkins Daily News",
            "Editor's Office",
            "Question Sarah Bartlett",
            "Leave Editor's Office",
            "Leave Hawkins Daily News",
            "Hawkins Factory",
            "Rotting machinery",
            "Examine a shiny lever on a rusted machine",
            "Secret Room",
            "Examine a diary",
        ]
        inputs.extend(file.readlines())
        inputs.extend(
            [
                "Leave Secret Room",
                "Leave Hawkins Factory",
                "Orpheum Theater",
                "Theatre Basement",
                "Examine a graffitied wall",
                "Leave Theatre Basement",
                "Leave Orpheum Theater",
                "Benny's Burgers",
                "Diner Counter",
                "Examine salt",
                "Leave Diner Counter",
                "Leave Benny's Burgers",
                "St. Patrick's Parish Church",
                "Cathedral's Basement",
                "Question Ross MacGarry",
                "Leave Cathedral's Basement",
                "Leave St. Patrick's Parish Church",
                "Archdiocese of Hawkins",
                "Chancery",
                "Question Very Rev. Sean Fitzgerald",
                "Leave Chancery",
                "Leave Archdiocese of Hawkins",
                "Trinity Manor",
                "Main Desk",
                "Question Phil Callahan",
                "Zachariah Dowey",
                "Zachariah Dowey's Bedroom",
                "Question Zachariah Dowey",
                "Leave Zachariah Dowey's Bedroom",
                "Leave Trinity Manor",
                "Orpheum Theater",
                "Theatre Basement",
                "Examine a shattered amulet",
                "Leave Theatre Basement",
                "Leave Orpheum Theater",
                "Hawkins Public Library",
                "Local Maps",
                "Examine a replica map of Hawkins from 1873",
                "Leave Local Maps",
                "Leave Hawkins Public Library",
                "Whispering Pine Cemetery",
                "A clearing in the middle of the cemetery",
                "Examine Speakers from the School",
                "Away Tsathoggua",
            ]
        )
        inputs = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def test_act_three_12_times(monkeypatch):
    with open("decoded.txt", "r") as file:
        inputs = [
            "Malone's Detective Agency",
            "Office",
            "Examine a signal jammer",
            "Leave Office",
            "Supply Closet",
            "Examine a lock pick kit",
            "Leave Supply Closet",
            "Leave Malone's Detective Agency",
            "Hawkins Daily News",
            "Editor's Office",
            "Question Sarah Bartlett",
            "Leave Editor's Office",
            "Leave Hawkins Daily News",
            "Hawkins Factory",
            "Rotting machinery",
            "Examine a shiny lever on a rusted machine",
            "Secret Room",
            "Examine a diary",
        ]
        inputs.extend(file.readlines())
        inputs.extend(
            [
                "Leave Secret Room",
                "Leave Hawkins Factory",
                "Orpheum Theater",
                "Theatre Basement",
                "Examine a graffitied wall",
                "Leave Theatre Basement",
                "Leave Orpheum Theater",
            ]
        )
        inputs.extend(["3", "2"] * 12)
        inputs = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        with pytest.raises(SystemExit):
            act_three(project.cache)


def input_generator(test_input):
    for line in test_input.splitlines():
        yield line
    raise EOFError


def test_check_cipher_correct():
    test_input = """Aol Vsk Dvvkz, Tpkupnoa
- h wpljl vm h zohaalylk htbsla
- h cphs vm zhsa islzzlk if h svjhs wyplza
Johua: Hdhf Azhaovnnbh!"""
    index = "Examine an old computer"
    action_room = MockRoom(
        "Hawkins Factory", "Manager's Office", items="an old computer"
    )
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        assert project.check_cipher(index, action_room) == True


def test_check_cipher_correct_print(capsys):
    test_input = """Aol Vsk Dvvkz, Tpkupnoa
- h wpljl vm h zohaalylk htbsla
- h cphs vm zhsa islzzlk if h svjhs wyplza
Johua: Hdhf Azhaovnnbh!"""
    index = "Examine an old computer"
    action_room = MockRoom(
        "Hawkins Factory", "Manager's Office", items="an old computer"
    )

    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        project.check_cipher(index, action_room)
        captured = capsys.readouterr()
        assert (
            captured.out
            == """Enter/Paste your content. Ctrl-D to save it.

The Old Woods, Midnight
- a piece of a shattered amulet
- a vial of salt blessed by a local priest
Chant: Away Tsathoggua!

"""
        )


def test_check_cipher_fail():
    test_input = "test"
    index = "Examine an old computer"
    action_room = MockRoom(
        "Hawkins Factory", "Manager's Office", items="an old computer"
    )
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        assert project.check_cipher(index, action_room) == False


def test_check_cipher_fail_print(capsys):
    test_input = "test"
    index = "Examine an old computer"
    action_room = MockRoom(
        "Hawkins Factory", "Manager's Office", items="an old computer"
    )

    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        project.check_cipher(index, action_room)
        captured = capsys.readouterr()
        assert (
            captured.out
            == """Enter/Paste your content. Ctrl-D to save it.
Input not recognize
"""
        )


def test_decoded_correct():
    test_input = """The Old Woods, Midnight
- a piece of a shattered amulet
- a vial of salt blessed by a local priest
Chant: Away Tsathoggua!"""
    index = "Examine a diary"
    diary = MockInventory("a diary", "a diary with pages filled with strange writings")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        assert project.decoded(index, action_room) == True


def test_decoded_correct_print(capsys):
    test_input = """The Old Woods, Midnight
- a piece of a shattered amulet
- a vial of salt blessed by a local priest
Chant: Away Tsathoggua!"""
    index = "Examine a diary"
    diary = MockInventory("a diary", "a diary with pages filled with strange writings")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        project.decoded(index, action_room)
        captured = capsys.readouterr()
        assert (
            captured.out
            == """What does the coded message say? Ctrl-D to save it.

Correct

"""
        )


def test_decoded_fail():
    test_input = "test"
    index = "Examine a diary"
    diary = MockInventory("a diary", "a diary with pages filled with strange writings")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        assert project.decoded(index, action_room) == False


def test_decoded_fail_print(capsys):
    test_input = "test"
    index = "Examine a diary"
    diary = MockInventory("a diary", "a diary with pages filled with strange writings")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        project.decoded(index, action_room)
        captured = capsys.readouterr()
        assert (
            captured.out
            == """What does the coded message say? Ctrl-D to save it.
Input not recognized
"""
        )


def test_get_commands_pass():
    message = "test"
    length = 2
    with patch("builtins.input", return_value="1"):
        assert project.get_commands(message, length) == 1


def test_get_commands_ValueError():
    message = "test"
    length = 2
    with patch("builtins.input", side_effect=["a", "1"]):
        result = project.get_commands(message, length)
        assert result == 1


def test_get_commands_outofrange():
    message = "test"
    length = 2
    with patch("builtins.input", side_effect=["-1", "0", "4", "1"]):
        result = project.get_commands(message, length)
        assert result == 1


def test_get_location():
    locations = ["farm", "library", "train"]
    input = "1"
    with patch("builtins.input", return_value=input):
        result = project.get_location(locations)
        assert result == locations[int(input) - 1]


def test_get_location_outofrange():
    locations = ["farm", "library", "train"]
    input = ["-1", "0", "1"]
    with patch("builtins.input", side_effect=input):
        result = project.get_location(locations)
        assert result == locations[int(input[-1]) - 1]


def test_get_location_ValueError():
    locations = ["farm", "library", "train"]
    input = ["a", "1"]
    with patch("builtins.input", side_effect=input):
        result = project.get_location(locations)
        assert result == locations[int(input[-1]) - 1]


def test_get_rooms():
    secret = MockRoom("Hawkins Factory", "Secret Room")
    rooms = [secret, "quit"]
    input = "1"
    with patch("builtins.input", return_value=input):
        result = project.get_room(rooms)
        assert result == rooms[int(input) - 1]


def test_get_rooms_ValueError():
    secret = MockRoom("Hawkins Factory", "Secret Room")
    rooms = [secret, "quit"]
    input = ["a", "1"]
    with patch("builtins.input", side_effect=input):
        result = project.get_room(rooms)
        assert result == rooms[int(input[-1]) - 1]


def test_get_rooms_outofrange():
    secret = MockRoom("Hawkins Factory", "Secret Room")
    rooms = [secret, "quit"]
    input = ["-1", "0", "1"]
    with patch("builtins.input", side_effect=input):
        result = project.get_room(rooms)
        assert result == rooms[int(input[-1]) - 1]


def test_get_actions():
    posters = MockInventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    project.cache = [posters]
    text_forry = "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters."
    action_room = MockRoom(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    input = "1"
    with patch("builtins.input", return_value=input):
        result = project.get_action(action_room)
        assert result == f"Question {action_room.person}"


def test_get_actions_inventory():
    original_cache = project.cache

    posters = MockInventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    project.cache = [posters]
    text_forry = "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters."
    action_room = MockRoom(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    input = 4
    with patch("project.get_commands", return_value=input):
        result = project.get_action(action_room)
        print(result)
        assert result == "Check Inventory"
    project.cache = original_cache


def test_check_room_action_question():
    posters = MockInventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    items = [posters]
    text_forry = "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters."
    action_room = MockRoom(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    index = f"Question {action_room.person}"
    result = project.check_room_action(index, action_room, items)
    assert result == False


def test_check_room_action_question_print(capsys):
    posters = MockInventory(
        "Missing posters",
        "The missing posters in the police station show that four teenagers from Hawkins have gone missing in the last month. Their names are Abed Nadir, Freya Day, Huan Li, and Grace Rosberg",
    )
    items = [posters]
    text_forry = "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters."
    action_room = MockRoom(
        "Hawkins Police Station",
        "Front Reception",
        "Officer Braydon Forry",
        "the desk sergeant",
        text_forry,
        posters.item,
        posters.description,
    )
    index = f"Question {action_room.person}"
    project.check_room_action(index, action_room, items)
    captured = capsys.readouterr()
    # print('captured output:', captured.out)
    # print('captured errors:', captured.err)
    assert (
        captured.out
        == "Yeah, I remember her. She wanted some information about some missing students from her school. I directed her to the Missing Posters.\n\n"
    )


def test_check_room_action_exam_diary():
    test_input = """The Old Woods, Midnight
- a piece of a shattered amulet
- a vial of salt blessed by a local priest
Chant: Away Tsathoggua!"""
    index = "Examine a diary"
    diary = MockInventory("a diary", "a diary with pages filled with strange writings")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=diary.item,
        item_description=diary.description,
    )
    items = [diary]
    with patch(
        "builtins.input",
        return_value=test_input,
        side_effect=input_generator(test_input),
    ):
        assert project.check_room_action(index, action_room, items) == False


def test_check_room_action_exam_add_item():
    temp_cache = project.cache
    test = MockInventory("a test", "test description")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=test.item,
        item_description=test.description,
    )
    index = f"Examine {action_room.items}"
    items = [test]
    project.cache = []
    assert project.check_room_action(index, action_room, items) == (
        {"description": "test description", "item": "a test"},
        False,
    )
    project.cache = temp_cache


def test_check_room_action_exam_add_item():
    project.cache = []
    temp_cache = project.cache
    test = MockInventory("a test", "test description")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=test.item,
        item_description=test.description,
    )
    index = f"Examine {action_room.items}"
    items = [test]
    project.cache.append({"item": "a test", "description": "test description"})
    assert project.check_room_action(index, action_room, items) == False
    project.cache = temp_cache


def test_check_room_action_inventory_print(capsys):
    project.cache = []
    temp_cache = project.cache
    test = MockInventory("a test", "test description")
    diary = MockInventory("a diary", "a diary with pages filled with strange writings")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=test.item,
        item_description=test.description,
    )
    index = f"Check Inventory"
    items = [test, diary]
    project.cache.append({"item": "a test", "description": "test description"})
    project.cache.append(
        {
            "item": "a diary",
            "description": "a diary with pages filled with strange writings",
        }
    )
    project.check_room_action(index, action_room, items)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """Inventory:
a test: test description
a diary: a diary with pages filled with strange writings

"""
    )
    project.cache = temp_cache


def test_check_room_action_inventory():
    project.cache = []
    temp_cache = project.cache
    test = MockInventory("a test", "test description")
    action_room = MockRoom(
        "Hawkins Factory",
        "Secret Room",
        items=test.item,
        item_description=test.description,
    )
    index = f"Check Inventory"
    items = [test]
    project.cache.append({"item": "a test", "description": "test description"})
    assert project.check_room_action(index, action_room, items) == False
    project.cache = temp_cache


def test_check_lock_false():
    project.cache = []
    temp_cache = project.cache
    assert project.check_lock() == False
    project.cache = temp_cache


def test_check_lock_true():
    project.cache = []
    temp_cache = project.cache
    project.cache.append(
        {"item": "a lock pick kit", "description": "Tools to unlock a locked door"}
    )
    assert project.check_lock() == True
    project.cache = temp_cache

import pytest
from unittest.mock import patch, mock_open
from project import (
    get_commands,
    get_location,
    get_room,
    get_action,
    get_rooms_for_location,
    check_room_action,
    check_lock,
    typingPrint,
    handle_retirement_manor,
    handle_retirement_herring,
    handle_restaurant,
    handle_archdiocese,
    handle_basement_visit,
    handle_agency,
    handle_maeve,
    handle_theo,
    handle_school,
    handle_max,
    handle_occult,
    handle_palm,
    handle_magic_box,
    handle_library,
    handle_theatre,
    handle_mall,
    handle_cemetery,
    get_rooms_for_location,
    handle_basement_visit,
    initialize_act_three,
    decoded,
    print_csv
)
from map import Location, Room
from inventory import Inventory

@pytest.fixture
def sample_location():
    return Location("Test Location", [
        Room("Test Location", "Room 1"),
        Room("Test Location", "Room 2"),
    ])

@pytest.fixture
def sample_room():
    return Room(
        "Test Location",
        "Test Room",
        "Test Person",
        "Test Description",
        "Test Text",
        "Test Item",
        "Test Item Description"
    )

@pytest.fixture
def sample_inventory():
    return Inventory("Test Item", "Test Description")

def test_get_commands():
    with patch('builtins.input', return_value='2'):
        assert get_commands("Test prompt", 3) == 2

def test_get_commands_invalid_input():
    with patch('builtins.input', side_effect=['a', '0', '4', '2']):
        assert get_commands("Test prompt", 3) == 2

def test_get_location(sample_location):
    locations = [sample_location, "Quit Game"]
    with patch('project.get_commands', return_value=1):
        result = get_location(locations)
        assert result == sample_location

def test_get_room(sample_room):
    rooms = [sample_room, "Leave Test Location"]
    with patch('project.get_commands', return_value=1):
        result = get_room(rooms)
        assert result == sample_room

def test_get_action(sample_room):
    with patch('project.get_commands', return_value=1):
        result = get_action(sample_room)
        assert result == f"Question {sample_room.person}"

def test_check_room_action(sample_room, sample_inventory):
    result = check_room_action(f"Question {sample_room.person}", sample_room, [sample_inventory], [])
    assert result == False

def test_check_lock():
    cache = [{"item": "a lock pick kit", "description": "Test description"}]
    assert check_lock(cache) == True

def test_typingPrint(capsys):
    typingPrint("Test message")
    captured = capsys.readouterr()
    assert captured.out == "Test message"

def test_handle_retirement_manor():
    room = Room("Trinity Manor", "Main Desk", "Phil Callahan", "security guard")
    with patch('builtins.input', return_value="Zachariah Dowey"):
        attempts_trinity, salt_bool, blessed_salt_bool, cache, new_room = handle_retirement_manor(
            room, "Question Phil Callahan", 0, False, False, []
        )
        assert attempts_trinity == 1
        assert new_room is not None
        assert new_room.room == "Zachariah Dowey's Bedroom"
        assert new_room.person == "Zachariah Dowey"
        assert new_room.description == "retired priest"

def test_handle_retirement_herring():
    location = Location("Hawkins Continuing-Care Community", [])
    room = Room("Hawkins Continuing-Care Community", "Security Desk", "Laurence Tureaud", "security guard")
    room.location = location  # Set the location attribute of the room

    # Test when the correct name is provided
    with patch('builtins.input', return_value="Sonny O'Sullivan"):
        attempts_carehome = handle_retirement_herring(room, "Question Laurence Tureaud", 0)
        assert attempts_carehome == 1
        assert len(location.rooms) == 1
        new_room = location.rooms[0]
        assert new_room.room == "Sonny O'Sullivan's Bedroom"
        assert new_room.person == "Sonny O'Sullivan"
        assert new_room.description == "retired priest"
        assert new_room.text == "Who are you? Bless your salt? Kids today and their strange fads."

    # Test when an incorrect name is provided
    with patch('builtins.input', return_value="Wrong Name"):
        attempts_carehome = handle_retirement_herring(room, "Question Laurence Tureaud", 1)
        assert attempts_carehome == 2
        assert len(location.rooms) == 1  # No new room added

    # Test when maximum attempts are reached
    with patch('builtins.input', return_value="Wrong Name"):
        attempts_carehome = handle_retirement_herring(room, "Question Laurence Tureaud", 2)
        assert attempts_carehome == 3
        assert room.text == "You obviously don't know anyone here, please leave."

    # Additional test to ensure text is set only on the last attempt
    room.text = None
    with patch('builtins.input', return_value="Wrong Name"):
        attempts_carehome = handle_retirement_herring(room, "Question Laurence Tureaud", 1)
        assert attempts_carehome == 2
        assert room.text is None  # Text should not be set yet

    with patch('builtins.input', return_value="Wrong Name"):
        attempts_carehome = handle_retirement_herring(room, "Question Laurence Tureaud", 2)
        assert attempts_carehome == 3
        assert room.text == "You obviously don't know anyone here, please leave."


def test_handle_restaurant():
    assert handle_restaurant("Examine salt", False) == True

def test_handle_archdiocese(capsys):
    with patch('project.print_csv') as mock_print_csv:
        handle_archdiocese("Question Very Rev. Sean Fitzgerald")
        mock_print_csv.assert_called_once_with("priests.csv")

def test_handle_agency():
    attempts_jack, money = handle_agency("Question Jack Malone", 0, 0)
    assert attempts_jack == 1
    assert money == 10

def test_handle_maeve():
    attempts_piggybank, money = handle_maeve("Examine Maeve's Piggybank", 0, 0)
    assert attempts_piggybank == 1
    assert money == 100

def test_handle_theo():
    room = Room("Theo's House", "Kitchen")
    assert handle_theo(room, True) == False

def test_handle_school():
    room = Room("Hawkins Collegiate", "Music Room", text="Test text")
    with patch('project.typingPrint') as mock_typing_print:
        with patch('project.game_over') as mock_game_over:
            handle_school(room)
            mock_typing_print.assert_called_once_with("Test text")
            mock_game_over.assert_called_once_with("You lose")

def test_handle_max():
    room = Room("Max's House", "Kitchen")
    assert handle_max(room, True) == False

def test_handle_occult():
    with patch('builtins.input', return_value='y'):
        money, cache = handle_occult("Examine The Amulet of the Yoth", 100, [])
        assert money == 0
        assert len(cache) == 1
        assert cache[0]['item'] == "The Amulet of the Yoth"

def test_handle_palm():
    with patch('builtins.input', return_value='y'):
        money = handle_palm("Question Mme. Avalonia", 60)
        assert money == 0

def test_handle_magic_box():
    with patch('builtins.input', return_value='y'):
        hours, attempts_giles, money, blessed_salt_bool, cache = handle_magic_box(
            "Examine Books on Demons, Magic, and Supernatural Creatures",
            10, 0, 100, False, []
        )
        assert hours == 9
        assert attempts_giles == 0
        assert money == 100
        assert blessed_salt_bool == False
        assert len(cache) == 0

def test_handle_library():
    locations = []
    handle_library("Examine a replica map of Hawkins from 1873", locations)
    assert len(locations) == 1
    assert locations[0].location == "Whispering Pine Cemetery"

def test_handle_theatre():
    cache, amulet_bool = handle_theatre("Examine a shattered amulet", [], False)
    assert len(cache) == 1
    assert cache[0]['item'] == "a shattered amulet"
    assert amulet_bool == True

def test_handle_mall():
    with patch('builtins.input', return_value='y'):
        money, cache, salt_bool = handle_mall("Examine salt", 10, [], False)
        assert money == 8
        assert len(cache) == 1
        assert cache[0]['item'] == "salt"
        assert salt_bool == True

def test_handle_cemetery():
    with pytest.raises(SystemExit):
        handle_cemetery(False, True, [], True, True)


def test_get_rooms_for_location():
    location1 = Location("Location1", [Room("Location1", "Room1"), Room("Location1", "Room2")])
    location2 = Location("Location2", [Room("Location2", "Room3")])
    locations = [location1, location2, "Quit Game"]

    rooms = get_rooms_for_location(location1, locations)
    assert len(rooms) == 2
    assert rooms[0].room == "Room1"
    assert rooms[1].room == "Room2"

    rooms = get_rooms_for_location("Location2", locations)
    assert len(rooms) == 1
    assert rooms[0].room == "Room3"

    rooms = get_rooms_for_location("Quit Game", locations)
    assert rooms == ["Quit Game"]

def test_handle_basement_visit(capsys):
    handle_basement_visit()
    captured = capsys.readouterr()
    assert "Performing a reverse image search" in captured.out

def test_initialize_act_three():
    locations, items = initialize_act_three()
    assert len(locations) > 0
    assert all(isinstance(loc, Location) for loc in locations)
    assert len(items) == 4
    assert all(isinstance(item, Inventory) for item in items)

def test_get_rooms_for_location():
    location1 = Location("Location1", [Room("Location1", "Room1"), Room("Location1", "Room2")])
    location2 = Location("Location2", [Room("Location2", "Room3")])
    locations = [location1, location2, "Quit Game"]

    rooms = get_rooms_for_location(location1, locations)
    assert len(rooms) == 2
    assert rooms[0].room == "Room1"
    assert rooms[1].room == "Room2"

    rooms = get_rooms_for_location("Location2", locations)
    assert len(rooms) == 1
    assert rooms[0].room == "Room3"

    rooms = get_rooms_for_location("Quit Game", locations)
    assert rooms == ["Quit Game"]

def test_handle_basement_visit(capsys):
    handle_basement_visit()
    captured = capsys.readouterr()
    assert "Performing a reverse image search" in captured.out
    assert "Cthulhu mythos" in captured.out
    assert "Tsathoggua's insatiable hunger for power" in captured.out

def test_initialize_act_three():
    locations, items = initialize_act_three()
    assert len(locations) > 0
    assert all(isinstance(loc, Location) for loc in locations)
    assert len(items) == 4
    assert all(isinstance(item, Inventory) for item in items)
    assert any(item.item == "a lock pick kit" for item in items)
    assert any(item.item == "a signal jammer" for item in items)
    assert any(item.item == "a shattered amulet" for item in items)
    assert any(item.item == "salt" for item in items)

def test_decoded_correct():
    test_input = """The Old Woods, Midnight
- a piece of a shattered amulet
- a vial of salt blessed by a local priest
Chant: Away Tsathoggua!"""
    index = "Examine a diary"
    action_room = Room(
        "Hawkins Factory",
        "Secret Room",
        items="a diary",
        item_description="a diary with pages filled with strange writings",
    )
    with patch('builtins.input', side_effect=[line for line in test_input.split('\n')] + [EOFError]):
        assert decoded(index, action_room) == True

def test_decoded_incorrect():
    test_input = "This is not the correct decoded message"
    index = "Examine a diary"
    action_room = Room(
        "Hawkins Factory",
        "Secret Room",
        items="a diary",
        item_description="a diary with pages filled with strange writings",
    )
    with patch('builtins.input', side_effect=[test_input, EOFError]):
        assert decoded(index, action_room) == False

def test_print_csv(capsys):
    mock_csv_content = """Name,Parish,Dates
Louis Kinsella,Ascension,2012-
Myles Barrett,Ascension,2008-2012
Christian O'Reilly,Ascension,1999-2008"""
    
    with patch("builtins.open", mock_open(read_data=mock_csv_content)) as mock_file:
        print_csv("priests.csv")
    
        captured = capsys.readouterr()
        expected_output = """Name                Parish     Dates
------------------  ---------  ---------
Louis Kinsella      Ascension  2012-
Myles Barrett       Ascension  2008-2012
Christian O'Reilly  Ascension  1999-2008"""
    assert captured.out.strip() == expected_output.strip()

def test_handle_archdiocese_prints_csv():
    with patch('project.print_csv') as mock_print_csv:
        handle_archdiocese("Question Very Rev. Sean Fitzgerald")
        mock_print_csv.assert_called_once_with("priests.csv")




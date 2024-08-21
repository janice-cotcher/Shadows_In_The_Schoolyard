import pytest
from unittest.mock import patch, MagicMock
from helper import (
    get_rooms_for_location,
    handle_location_options,
    get_commands,
    check_room_action,
    check_lock,
    decoded,
)
from map import Location, Room
from inventory import Inventory

def test_get_rooms_for_location():
    print("test_get_rooms_for_location is running")
    room1 = Room("Location1", "Room1")
    room2 = Room("Location1", "Room2")
    room3 = Room("Location2", "Room3")
    location1 = Location("Location1", [room1, room2])
    location2 = Location("Location2", [room3])
    locations = [location1, location2]

    print("Calling get_rooms_for_location with location1")
    assert get_rooms_for_location(location1, locations) == location1.rooms
    print("Calling get_rooms_for_location with 'Quit Game'")
    assert get_rooms_for_location("Quit Game", locations) == ["Quit Game"]
    print("Calling get_rooms_for_location with 'Location2'")
    assert get_rooms_for_location("Location2", locations) == location2.rooms
    print("Calling get_rooms_for_location with 'NonexistentLocation'")
    assert get_rooms_for_location("NonexistentLocation", locations) == []
    assert get_rooms_for_location("Check Inventory", []) == ["Check Inventory"]


@patch('builtins.input')
@patch('builtins.print')
def test_handle_location_options(mock_print, mock_input):
    mock_input.side_effect = ['1', '2']
    location = Location("TestLocation", [])
    cache = []

    assert handle_location_options(location, cache) == False
    assert handle_location_options(location, cache) == True

@patch('builtins.input')
def test_get_commands(mock_input):
    mock_input.side_effect = ['0', '4', '2']
    assert get_commands("Test prompt", 3) == 2

def test_check_room_action():
    room = Room("TestLocation", "TestRoom", items="TestItem", item_description="Test description")
    items = [Inventory("TestItem", "Test description")]
    cache = []

    result, _ = check_room_action("Examine TestItem", room, items, cache)
    assert isinstance(result, dict)
    assert result["item"] == "TestItem"
    assert result["description"] == "Test description"

    assert check_room_action("Question Person", room, items, cache) == False
    assert check_room_action("Leave TestRoom", room, items, cache) == True

def test_check_lock():
    cache_with_lock_pick = [{"item": "a lock pick kit", "description": "A set of lock picks"}]
    cache_without_lock_pick = [{"item": "other item", "description": "Some other item"}]

    assert check_lock(cache_with_lock_pick) == True
    assert check_lock(cache_without_lock_pick) == False

@patch('builtins.open')
def test_decoded(mock_open):
    mock_file = MagicMock()
    mock_file.read.return_value = "correct code"
    mock_open.return_value = mock_file

    room = Room("TestLocation", "TestRoom")
    
    with patch('builtins.input', side_effect=['correct code', '']):
        assert decoded("Examine a diary", room) == True

    with patch('builtins.input', side_effect=['wrong code', '']):
        assert decoded("Examine a diary", room) == False

# New test for Inventory class
def test_inventory():
    item = Inventory("Test Item", "This is a test item")
    assert str(item) == "Test Item"
    assert item.examine() == "Test Item: This is a test item"

    item_dict = item.to_dict()
    assert item_dict == {"item": "Test Item", "description": "This is a test item"}

    new_item = Inventory.from_dict(item_dict)
    assert new_item.item == "Test Item"
    assert new_item.description == "This is a test item"

# New test for Location and Room classes
def test_location_and_room():
    room1 = Room("House", "Living Room", person="Alice", description="sitting on the couch", items="Book")
    room2 = Room("House", "Kitchen")
    location = Location("House", [room1, room2])

    assert str(location) == "You are at House. Where do you want to go?\n - Living Room\n - Kitchen\n"
    assert str(room1) == "You are at House in the Living Room. You see Alice, sitting on the couch. You also see Book."
    assert str(room2) == "You are at House in the Kitchen. You see no one or no items of interest."

# def test_check_inventory():
#     # Call the function with "Check Inventory"
#     result = get_rooms_for_location("Check Inventory", [])
    
#     # Assert that the result is ["Check Inventory"]
#     assert result == ["Check Inventory"]

if __name__ == "__main__":
    pytest.main()
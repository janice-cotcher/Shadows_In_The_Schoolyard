import pytest
from unittest.mock import patch, Mock
from act_one import intro_text, act_one, initialize_act_one
from map import Location, Room
from inventory import Inventory
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_initialize_act_one():
    locations, items = initialize_act_one()

    assert len(locations) == 5
    assert isinstance(locations[0], Location)
    assert isinstance(locations[1], Location)
    assert isinstance(locations[2], Location)
    assert isinstance(locations[3], Location)
    assert locations[4] == "Quit Game"

    assert len(items) == 4
    assert all(isinstance(item, Inventory) for item in items)

@pytest.fixture
def mock_helpers():
   with patch('helper.get_location') as mock_get_location, \
        patch('helper.handle_location_options') as mock_handle_options, \
        patch('helper.get_room') as mock_get_room, \
        patch('helper.get_action') as mock_get_action, \
        patch('helper.check_room_action') as mock_check_action, \
        patch('helper.typingPrint') as mock_typing_print, \
        patch('helper.get_rooms_for_location') as mock_get_rooms_for_location:
       yield {
           'get_location': mock_get_location,
           'handle_options': mock_handle_options,
           'get_room': mock_get_room,
           'get_action': mock_get_action,
           'check_action': mock_check_action,
           'typing_print': mock_typing_print,
           'get_rooms_for_location': mock_get_rooms_for_location
       }

def test_act_one_inventory_interaction(mock_helpers):
    location_calls = 0
    handle_options_calls = 0
    get_room_calls = 0
    get_action_calls = 0
    check_action_calls = 0
    
    def flexible_get_location(*args, **kwargs):
        nonlocal location_calls
        location_calls += 1
        logger.debug(f"get_location called (#{location_calls}) with args: {args}, kwargs: {kwargs}")
        return "Hawkins Factory" if location_calls > 3 else Location("Hawkins Collegiate", [])

    def flexible_handle_options(*args, **kwargs):
        nonlocal handle_options_calls
        handle_options_calls += 1
        logger.debug(f"handle_options called (#{handle_options_calls}) with args: {args}, kwargs: {kwargs}")
        return handle_options_calls > 2

    def flexible_get_room(*args, **kwargs):
        nonlocal get_room_calls
        get_room_calls += 1
        logger.debug(f"get_room called (#{get_room_calls}) with args: {args}, kwargs: {kwargs}")
        return "Leave Hawkins Collegiate" if get_room_calls > 2 else Room("Hawkins Collegiate", "Journalism Classroom", items="a mysterious note")

    def flexible_get_action(*args, **kwargs):
        nonlocal get_action_calls
        get_action_calls += 1
        logger.debug(f"get_action called (#{get_action_calls}) with args: {args}, kwargs: {kwargs}")
        return f"Leave {flexible_get_room}" if get_action_calls > 2 else "Examine a mysterious note"

    def flexible_check_action(action, room, items, cache):
        nonlocal check_action_calls
        check_action_calls += 1
        logger.debug(f"check_action called (#{check_action_calls}) with action: {action}, room: {room}, items: {items}, cache: {cache}")
        if action == "Examine a mysterious note" and check_action_calls == 1:
            new_item = Inventory('a mysterious note', 'A cryptic message about Hawkins Factory')
            if new_item not in cache:
                cache.append(new_item)
                return cache
        elif check_action_calls == 2:
            return False
        else:
            return True

    mock_helpers['get_location'].side_effect = flexible_get_location
    mock_helpers['handle_options'].side_effect = flexible_handle_options
    mock_helpers['get_room'].side_effect = flexible_get_room
    mock_helpers['get_action'].side_effect = flexible_get_action
    mock_helpers['check_action'].side_effect = flexible_check_action
    mock_helpers['typing_print'].side_effect = lambda *args, **kwargs: None

    # Initialize cache with a starting item
    flashlight = Inventory('flashlight','A small, but bright flashlight')
    cache = [flashlight]
    
    logger.info(f"Initial cache contents: {cache}")
    logger.info("Starting act_one function")
    act_one(cache)
    logger.info("act_one function completed")

    logger.info(f"get_location called {location_calls} times")
    logger.info(f"handle_options called {handle_options_calls} times")
    logger.info(f"get_room called {get_room_calls} times")
    logger.info(f"get_action called {get_action_calls} times")
    logger.info(f"check_action called {check_action_calls} times")
    
    logger.info(f"Final cache contents: {cache}")

    assert len(cache) == 2, "Cache should contain two items"
    assert cache[0] == Inventory('flashlight','A small, but bright flashlight'), "First item in cache should be flashlight"
    assert cache[1] == Inventory('a mysterious note', 'A cryptic message about Hawkins Factory'), "Second item in cache should be a mysterious note"
    assert location_calls > 3, "get_location should be called more than 3 times"
    assert handle_options_calls > 0, "handle_options should be called at least once"
    assert get_room_calls > 0, "get_room should be called at least once"
    assert get_action_calls > 0, "get_action should be called at least once"
    assert check_action_calls > 0, "check_action should be called at least once"


def test_sarah_bartlett_special_case(mock_helpers):
    locations, _ = initialize_act_one()
    original_locations = locations.copy()

    location_calls = 0
    def flexible_get_location(*args, **kwargs):
        nonlocal location_calls
        location_calls += 1
        logger.debug(f"get_location called {location_calls} times")
        if location_calls == 1:
            return Location("Hawkins Daily News", [])
        else:
            return "Hawkins Factory"

    mock_helpers['get_location'].side_effect = flexible_get_location
    
    handle_options_calls = 0
    def flexible_handle_options(*args, **kwargs):
        nonlocal handle_options_calls
        handle_options_calls += 1
        logger.debug(f"handle_options called {handle_options_calls} times")
        return handle_options_calls > 1  # Return True after the first call to exit the location

    mock_helpers['handle_options'].side_effect = flexible_handle_options

    mock_helpers['get_rooms_for_location'].return_value = [Room("Hawkins Daily News", "Editor's Office", "Sarah Bartlett", "Emily's boss")]
    
    room_calls = 0
    def flexible_get_room(*args, **kwargs):
        nonlocal room_calls
        room_calls += 1
        logger.debug(f"get_room called {room_calls} times")
        if room_calls == 1:
            return Room("Hawkins Daily News", "Editor's Office", "Sarah Bartlett", "Emily's boss")
        else:
            return f"Leave Hawkins Daily News"

    mock_helpers['get_room'].side_effect = flexible_get_room
    
    action_calls = 0
    def flexible_get_action(*args, **kwargs):
        nonlocal action_calls
        action_calls += 1
        logger.debug(f"get_action called {action_calls} times")
        if action_calls == 1:
            return "Question Sarah Bartlett"
        else:
            return f"Leave Editor's Office"

    mock_helpers['get_action'].side_effect = flexible_get_action
    
    check_action_calls = 0
    def flexible_check_action(*args, **kwargs):
        nonlocal check_action_calls, locations
        check_action_calls += 1
        logger.debug(f"check_action called {check_action_calls} times")
        if check_action_calls == 1:
            # Simulate adding Hawkins Factory to locations
            if "Hawkins Factory" not in [loc if isinstance(loc, str) else loc.location for loc in locations]:
                locations.insert(-1, "Hawkins Factory")
            return False
        else:
            return True

    mock_helpers['check_action'].side_effect = flexible_check_action

    cache = []
    
    logger.info("Starting act_one function")
    act_one(cache)
    logger.info("act_one function completed")

    logger.info(f"get_location called {location_calls} times")
    logger.info(f"handle_options called {handle_options_calls} times")
    logger.info(f"get_room called {room_calls} times")
    logger.info(f"get_action called {action_calls} times")
    logger.info(f"check_action called {check_action_calls} times")

    # Check that Hawkins Factory was added to locations
    assert "Hawkins Factory" in [loc if isinstance(loc, str) else loc.location for loc in locations], "Hawkins Factory should be added to locations"
    
    # Check that Hawkins Factory was inserted at the correct position (second to last)
    assert locations[-2] == "Hawkins Factory", "Hawkins Factory should be the second-to-last location"

    # Check that the function exited after selecting Hawkins Factory
    assert location_calls == 2, "Expected act_one to exit after 'Hawkins Factory' was returned"

    # Check that only Hawkins Factory was added to the original locations
    assert len(locations) == len(original_locations) + 1, "Only Hawkins Factory should be added to the original locations"

    # Log the position of Hawkins Factory
    hawkins_factory_index = [i for i, loc in enumerate(locations) if (isinstance(loc, str) and loc == "Hawkins Factory") or (isinstance(loc, Location) and loc.location == "Hawkins Factory")][0]
    logger.info(f"Hawkins Factory is at index {hawkins_factory_index} in the locations list")


@pytest.mark.parametrize("invalid_input", ["Invalid Location", "Invalid Room", "Invalid Action"])
def test_act_one_invalid_inputs(mock_helpers, invalid_input):
    # Create a mock Room object
    mock_room = Mock()
    mock_room.room = "Kitchen"
    if invalid_input == "Invalid Location":
        mock_helpers['get_location'].side_effect = [ValueError, "Hawkins Factory"]
    elif invalid_input == "Invalid Room":
        mock_helpers['get_location'].side_effect = [Location("Hawkins Collegiate", []), "Hawkins Factory"]
        mock_helpers['get_rooms_for_location'].return_value = [Room("Hawkins Collegiate", "Journalism Classroom")]
        mock_helpers['get_room'].side_effect = [ValueError, "Leave Hawkins Collegiate"]
    else:  # Invalid Action
        mock_helpers['get_location'].side_effect = [Location("Hawkins Collegiate", []), "Hawkins Factory"]
        mock_helpers['get_rooms_for_location'].return_value = [Room("Hawkins Collegiate", "Journalism Classroom")]
        mock_helpers['get_room'].return_value = Room("Hawkins Collegiate", "Journalism Classroom")
        # mock_helpers['get_action'].side_effect = [ValueError, "Leave Room"]
        mock_helpers['get_action'].side_effect = [ValueError, f"Leave {mock_room.room}"]

    mock_helpers['handle_options'].return_value = False
    mock_helpers['check_action'].return_value = True

    cache = []
    
    
    try:
        act_one(cache)
    except ValueError:
        pass

    assert mock_helpers['get_location'].call_count > 0
    if invalid_input != "Invalid Location":
        assert mock_helpers['get_room'].call_count > 0
    if invalid_input == "Invalid Action":
        assert mock_helpers['get_action'].call_count > 0



if __name__ == "__main__":
    pytest.main(["-v", "--log-cli-level=DEBUG"])
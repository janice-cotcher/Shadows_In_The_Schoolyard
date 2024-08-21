from typing import List, Optional


class Location:
    """
    Represents a location in the game world.
    """

    def __init__(self, location: str, rooms: Optional[List["Room"]] = None):
        """
        Initialize a Location object.

        Args:
            location (str): The name of the location.
            rooms (Optional[List['Room']]): A list of Room objects within this location.
        """
        self.location = location
        self.rooms = rooms if rooms is not None else []

    def __str__(self) -> str:
        """
        Return a string representation of the Location.

        Returns:
            str: A description of the location and its rooms.
        """
        result = f"You are at {self.location}. Where do you want to go?\n"
        for room in self.rooms:
            result += f" - {room.room}\n"
        return result


class Room:
    """
    Represents a room within a location in the game world.
    """

    def __init__(
        self,
        location: str,
        room: str,
        person: Optional[str] = None,
        description: Optional[str] = None,
        text: Optional[str] = None,
        items: Optional[str] = None,
        item_description: Optional[str] = None,
    ):
        """
        Initialize a Room object.

        Args:
            location (str): The name of the location this room is in.
            room (str): The name of the room.
            person (Optional[str]): The name of a person in the room, if any.
            description (Optional[str]): A description of the person, if any.
            text (Optional[str]): Additional text associated with the room.
            items (Optional[str]): The name of an item in the room, if any.
            item_description (Optional[str]): A description of the item, if any.
        """
        self.location = location
        self.room = room
        self.person = person
        self.description = description
        self.text = text
        self.items = items
        self.item_description = item_description

    def __str__(self) -> str:
        """
        Return a string representation of the Room.

        Returns:
            str: A description of the room and its contents.
        """
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

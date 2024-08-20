class Location:
    def __init__(self, location, rooms=None):
        self.location = location
        self.rooms = rooms

    def __str__(self):
        result = f"You are at {self.location}. Where do you want to go?\n"
        for room in self.rooms:
            result += f" - {room}\n"
        return result


class Room(Location):
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
        super().__init__(location, [room])
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

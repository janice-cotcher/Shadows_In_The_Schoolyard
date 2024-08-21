from typing import Optional


class Inventory:
    """
    Represents an item in the game that can be collected and used by the player.
    """

    def __init__(self, item: str, description: Optional[str] = None):
        """
        Initialize an Inventory object.

        Args:
            item (str): The name of the item.
            description (Optional[str]): A description of the item. Defaults to None.
        """
        self.item = item
        self.description = description
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Inventory):
            return self.item == value.item and self.description == value.description
        else:
            return False

    def __str__(self) -> str:
        """
        Return a string representation of the Inventory item.

        Returns:
            str: The name of the item.
        """
        return self.item

    def to_dict(self) -> dict:
        """
        Convert the Inventory object to a dictionary.

        Returns:
            dict: A dictionary representation of the Inventory object.
        """
        return {"item": self.item, "description": self.description}
    

    @classmethod
    def from_dict(cls, data: dict) -> "Inventory":
        """
        Create an Inventory object from a dictionary.

        Args:
            data (dict): A dictionary containing 'item' and optionally 'description'.

        Returns:
            Inventory: An Inventory object created from the dictionary data.
        """
        return cls(data["item"], data.get("description"))

    def examine(self) -> str:
        """
        Provide a detailed description of the item.

        Returns:
            str: A string containing the item's name and description (if available).
        """
        if self.description:
            return f"{self.item}: {self.description}"
        else:
            return f"{self.item}: No additional information available."

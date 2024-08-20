class Inventory:
    def __init__(self, item, description=None):
        self.item = item
        self.description = description

    def __str__(self):
        return f"{self.item}"

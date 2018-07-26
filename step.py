class Step:
    """Corresponds to a step in a sequence."""

    def __init__(self, description: str, completed=False):
        self.description = description
        self.completed = completed

    def serialize(self) -> dict:
        """Returns a dict representation."""

        return {
            'description': self.description,
            'completed': self.completed
        }


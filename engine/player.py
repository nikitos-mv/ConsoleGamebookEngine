class Player:
    """
    The Player class stores player parameters that are set during the game.
    """

    def __init__(self, data: dict = None):
        """
        :param data: List of player parameters to set instead of default values.
        """

        self._achievements = []

        self.set_data_from_save(data or {})

    def add_achievement(self, achievement_id: str) -> bool:
        """
        Adds an achievement to the player if it has not been earned before.
        :param achievement_id: Achievement ID.
        :return: True if the achievement has not been earned by the player before, False otherwise.
        """

        if achievement_id not in self._achievements:
            self._achievements.append(achievement_id)

            return True
        else:
            return False

    def get_data_for_save(self) -> dict:
        """
        :return: Dictionary containing class attribute values to write to the save file.
        """

        data = {'_achievements': self._achievements}

        for attribute in self._get_attributes_for_save():
            if hasattr(self, attribute):
                data[attribute] = getattr(self, attribute)

        return data

    def set_data_from_save(self, data: dict) -> None:
        """
        :param data: A dictionary containing the class attribute values to set from the save file.
        """

        for attribute, value in data.items():
            if hasattr(self, attribute) and attribute in self._get_attributes_for_save():
                setattr(self, attribute, value)

    @staticmethod
    def _get_attributes_for_save() -> list:
        """
        :return: List of additional class attributes to write to the save file.
        """

        return []

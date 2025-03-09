from engine.player import Player as GenericPlayer

class Player(GenericPlayer):
    def __init__(self):
        super().__init__()

        self._properties = {
            'secret_ways': False
        }

    def set_property(self, key: str, value: bool) -> None:
        if key in self._properties:
            self._properties[key] = value

    def get_property(self, key: str) -> bool:
        if key in self._properties:
            return self._properties[key]

        return False

    @staticmethod
    def _get_attributes_for_save() -> list:
        return ['_properties']
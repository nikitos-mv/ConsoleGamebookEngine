import pickle, os, yaml
from yaml.parser import ParserError

from .player import *
from .scenario import *

class Game:
    """
    The main class of the game.
    """

    def __init__(
        self,
        scenario: Scenario,
        achievements: dict = None,
        player: Player = None,
        game_texts_yaml_path: str = '',
        save_file: str = './game.save'
    ):
        """
        :param scenario: An instance of the current scenario class.
        :param achievements: A list of all achievements in the game.
        :param player: An instance of the current player class.
        :param game_texts_yaml_path: Path to a yaml file containing texts available for use with the get_text method.
        :param save_file: Path to the save file of the current game.
        """

        self.scenario = scenario
        self.achievements = achievements or {}
        self.player = player or Player()

        self.game_texts = {}
        self.save_file = save_file

        try:
            with open(os.path.join(os.path.dirname(__file__), 'texts.yaml')) as f:
                self.game_texts = yaml.safe_load(f)

            with open(game_texts_yaml_path) as f:
                self.game_texts.update(yaml.safe_load(f))
        except (EOFError, FileNotFoundError, ParserError):
            pass

        try:
            with open(self.save_file, 'rb') as save_file:
                data = pickle.load(save_file)

                self.player.set_data_from_save(data['player'])
                self.current_move = scenario.moves[data['current_move']] or scenario.entry_move
        except (EOFError, FileNotFoundError, KeyError, pickle.UnpicklingError):
            self.current_move = scenario.entry_move

    def get_text(self, key: str, fallback: str = None) -> str:
        """
        :param key: The key of the text in the game_text module.
        :param fallback: The value that will be returned if the key does not exist.
        :return: The text from the game_text module.
        """

        if key in self.game_texts:
            return self.game_texts[key]

        return fallback if fallback is not None else key

    def add_achievement(self, achievement_id: str) -> None:
        """
        Adds an achievement to the player if it has not been earned before.
        :param achievement_id: Achievement ID.
        """

        if achievement_id not in self.achievements:
            return

        if self.player.add_achievement(achievement_id):
            print(
                '\033[1m{0}\033[0;0m'.format(
                    self.get_text('new_achievement').format(self.get_text(self.achievements[achievement_id]))
                )
            )

    def run(self) -> None:
        """
        Method for starting the game. Receives a choice from the player and proceeds to the desired scenario move.
        The game ends if explicitly stated in the ScenarioMove parameters or if there are no more available ways.
        """
        move = self.current_move

        while True:
            print(move.render(self))

            if move.is_end:
                break

            ways = [way for way in move.ways if way.is_available(self)]

            if not ways:
                print('\033[1m{0}\033[0;0m'.format(self.get_text('no_ways_available')))

                break

            for index, way in enumerate(ways, 1):
                print("\033[1m[{0}]\033[0;0m {1}".format(index, way.render(self)))

            while True:
                try:
                    chosen_way = int(input('\033[1m{0}\033[0;0m'.format(self.get_text('your_way_prompt'))))

                    next_way = ways[chosen_way - 1]
                    next_way.post_choose(self)
                    self.current_move = move = next_way.next_move

                    self._save_progress()

                    break
                except (ValueError, IndexError):
                    print('\033[1m{0}\033[0;0m'.format(self.get_text('enter_valid_way')))

        self._finalize()

    def _save_progress(self) -> None:
        """
        Method that writes the current game progress to a save file.
        """

        with open(self.save_file, 'wb+') as save_file:
            pickle.dump(
                {
                    'player': self.player.get_data_for_save(),
                    'current_move': self.current_move.move_id
                },
                save_file
            )

    def _finalize(self) -> None:
        """
        Method called after the game has finished. Displays information about the author and deletes the game save file.
        """

        print('\033[1m{0}\033[0;0m'.format(self.get_text('game_over')))

        print(self.get_text('credits', ''))

        if os.path.exists(self.save_file):
            os.remove(self.save_file)

from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from .game import Game

class ScenarioMove:
    """
    The ScenarioMove class represents a node in the scenario graph.
    """

    def __init__(
        self,
        move_id: str,
        description_key: str,
        ways: list[ScenarioWay] = None,
        is_end: bool = False
    ):
        """
        :param move_id: Unique move ID.
        :param description_key: Key of the description of the move (see Game.get_text).
        :param ways: List of available ways for current move (list of ScenarioWay objects).
        :param is_end: If True, current move considered final and ends the game.
        """
        self.move_id = move_id
        self.description_key = description_key
        self.ways = ways or []
        self.is_end = is_end

    def render(self, game: Game) -> str:
        return game.get_text(self.description_key)

class ScenarioWay:
    """
    The ScenarioWay class represents an edge in the scenario graph.
    """

    def __init__(
        self,
        way_id: str, description_key: str, next_move: ScenarioMove,
        achievements = None,
        is_available_callback: Callable[[Game], bool] = None,
        post_choose_callback: Callable[[Game]] = None
    ):
        """
        :param way_id: Unique way ID.
        :param description_key: Key of the description of the way (see Game.get_text).
        :param next_move: The object of the next ScenarioMove.
        :param achievements: List of achievements awarded to the player when moving this way.
        :param is_available_callback: Callback function to check if the way is available to the player.
        :param post_choose_callback: Callback function called when the player moves this way.
        """
        self.way_id = way_id
        self.description_key = description_key
        self.next_move = next_move
        self.achievements = achievements or []

        self.is_available_callback = is_available_callback
        self.post_choose_callback = post_choose_callback

    def render(self, game: Game) -> str:
        return game.get_text(self.description_key)

    def is_available(self, game: Game) -> bool:
        return not self.is_available_callback or self.is_available_callback(game)

    def post_choose(self, game: Game) -> None:
        for achievement_id in self.achievements:
            game.add_achievement(achievement_id)

        self.post_choose_callback and self.post_choose_callback(game)

class Scenario:
    """
    The Scenario class represents the current scenario of the game.
    """

    def __init__(self, entry_move: ScenarioMove):
        self.entry_move = entry_move

        self.moves = self._init_moves(entry_move)

    def _init_moves(self, move: ScenarioMove) -> dict:
        moves = {move.move_id: move}

        for way in move.ways:
            moves.update(self._init_moves(way.next_move))

        return moves

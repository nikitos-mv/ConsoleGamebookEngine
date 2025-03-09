from engine.scenario import *
from .player import Player

_next_move = ScenarioMove(
    '2', 'move_2',
    [
        ScenarioWay(
            '3', 'way_3',
            ScenarioMove('3', 'move_3', is_end = True),
            achievements = ['first_achievement']
        ),
        ScenarioWay(
            '4', 'way_3',
            ScenarioMove('4', 'move_4', is_end = True),
            is_available_callback = lambda g: g.player.get_property('secret_ways'),
            achievements = ['second_achievement']
        )
    ]
)

_entry_move = ScenarioMove(
    '1', 'move_1',
    [
        ScenarioWay('1', 'way_1', _next_move),
        ScenarioWay(
            '2', 'way_2', _next_move,
            post_choose_callback = lambda g: g.player.set_property('secret_ways', True)
        )
    ]
)

scenario = Scenario(_entry_move)

achievements = {
    'first_achievement': 'achievement_first',
    'second_achievement': 'achievement_second'
}

player = Player()

import sys
from engine.game import *

_move_4 = [
    ScenarioWay(
        '4', 'Go to fourth move',
        ScenarioMove('4','Fourth move',is_end=True)
    )
]

_entryMove = ScenarioMove(
    '0', 'Entry move',
    [
        ScenarioWay(
            '1', 'Go to first move',
            ScenarioMove( '1', 'First move', is_end = True)
        ),
        ScenarioWay(
            '2', 'Go to second way',
            ScenarioMove('2', 'Second move', _move_4)
        ),
        ScenarioWay(
            '3', 'Go to third way',
            ScenarioMove('3', 'Third move', _move_4)
        )
    ]
)

scenario = Scenario(_entryMove)

game = Game(scenario)

try:
    game.run()
except KeyboardInterrupt:
    sys.exit(0)
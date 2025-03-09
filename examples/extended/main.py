import sys
from engine.game import *
from game.game_data import scenario, achievements, player

game = Game(scenario, achievements, player, './game/texts.yaml')

try:
    game.run()
except KeyboardInterrupt:
    sys.exit(0)
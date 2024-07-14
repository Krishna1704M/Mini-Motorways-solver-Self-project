import sys

from mini_motorways import MiniMotorways

args = sys.argv
if len(args) < 2:
    print('Usage: python3 main.py [mode: sim-bfs/dfs-djk]')

game = MiniMotorways(mode=args[1])
game.run()

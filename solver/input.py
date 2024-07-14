import subprocess as sp
from time import sleep

from xdo import Xdo


class InputParser:
    """A class to control the inputs of the game."""

    def __init__(self, delay=0.5):
        """Initializes the parser"""
        self.xdo = Xdo()
        self.DELAY = delay
        self.OPTION_SEP = 85.0

        win_ids = self.xdo.search_windows(winname=b'Mini Motorways')
        if len(win_ids) == 0:
            print("No active window found")
            self.win_id = -1
        else:
            self.win_id = win_ids[0]

    def delay_decorator(func):
        def delayed_func(*args, **kwargs):
            sleep(args[0].DELAY)
            return func(*args, **kwargs)
        return delayed_func

    @delay_decorator
    def toggle_pause(self):
        """toggles the pause/play of the game"""
        self.xdo.send_keysequence_window(
            window=self.win_id, keysequence=b'space')

    @delay_decorator
    def activate_window(self):
        self.xdo.activate_window(window=self.win_id)

    @delay_decorator
    def set_grid_parameters(self, dim, cell_size):
        self.win_dim = self.xdo.get_window_size(window=self.win_id)
        self.dim = dim
        self.cell_size = cell_size

    @delay_decorator
    def _move_mouse(self, loc):
        self.xdo.move_mouse(x=int(loc[0]), y=int(loc[1]))

    @delay_decorator
    def _mouse_down(self, button=1):
        sp.call(['xdotool', 'mousedown', f'{button}'])

    @delay_decorator
    def _mouse_up(self, button=1):
        sp.call(['xdotool', 'mouseup', f'{button}'])

    @delay_decorator
    def connect(self, cell1, x_move, y_move):
        """Connects 2 cells with a road"""
        pos1 = self.win_dim.width/2 + (cell1[0] - self.dim[0]/2) * \
            self.cell_size + self.cell_size/2, self.win_dim.height/2 + \
            (cell1[1] - self.dim[1]/2)*self.cell_size + self.cell_size/2
        pos2 = pos1[0] + x_move*self.cell_size * \
            1.25, pos1[1] + y_move*self.cell_size*1.25
        self._move_mouse(loc=pos1)
        self._mouse_down(button=1)
        self._move_mouse(loc=pos2)
        self._mouse_up(button=1)

    @delay_decorator
    def disconnect(self, cell):
        pos = self.win_dim.width/2 + (cell[0] - self.dim[0]/2) * \
            self.cell_size + self.cell_size/2, self.win_dim.height/2 + \
            (cell[1] - self.dim[1]/2)*self.cell_size + self.cell_size/2
        self._move_mouse(loc=pos)
        self._mouse_down(button=3)
        self._mouse_up(button=3)

    @delay_decorator
    def roundabout_or_lights(self, option, cell):
        pos1 = self.win_dim.width/2 - option*self.OPTION_SEP, self.win_dim.height
        pos2 = self.win_dim.width/2 + (cell[0] - self.dim[0]/2) * \
            self.cell_size + self.cell_size/2, self.win_dim.height/2 + \
            (cell[1] - self.dim[1]/2)*self.cell_size + self.cell_size/2
        self._move_mouse(loc=pos1)
        sleep(0.5)
        self._mouse_down(button=1)
        self._move_mouse(loc=pos2)
        self._mouse_up(button=1)

    @delay_decorator
    def select_powerup(self, choice=1):
        pos = self.win_dim.width/2 + \
            (choice*2-3)*self.OPTION_SEP * \
            2, self.win_dim.height/2+self.OPTION_SEP
        self._move_mouse(loc=pos)
        self._mouse_down(button=1)
        self._mouse_up(button=1)


if __name__ == '__main__':
    inp = InputParser(delay=0.1)
    inp.activate_window()
    # inp.toggle_pause()
    inp.set_grid_parameters((16, 9), 84.0)
    # inp.connect((11, 1), -1, -1)
    # inp.connect((11, 1), -1, 0)
    # inp.connect((11, 1), -1, 1)
    # inp.connect((11, 1), 0, -1)
    # inp.connect((11, 1), 0, 1)
    # inp.connect((11, 1), 1, -1)
    # inp.connect((11, 1), 1, 0)
    # inp.connect((11, 1), 1, 1)
    # inp.disconnect((11, 1))
    inp.select_powerup(2)
    # inp.roundabout_or_lights(1, (11, 1))

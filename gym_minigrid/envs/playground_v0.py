from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class PlaygroundV0(MiniGridEnv):
    """
    Environment with multiple rooms and random objects.
    This environment has no specific goals or rewards.
    """

    def __init__(self):
        super().__init__(gridSize=19, maxSteps=100)
        self.reward_range = (0, 1)

    def _genGrid(self, width, height):
        # Create the grid
        grid = Grid(width, height)

        # Generate the surrounding walls
        grid.horzWall(0, 0)
        grid.horzWall(0, height-1)
        grid.vertWall(0, 0)
        grid.vertWall(width-1, 0)

        roomW = width // 3
        roomH = height // 3

        # NOTE: if we want no room to have two doors of the same color,
        # that adds difficulty. It's a graph coloring problem
        # We could generate the door positions first, and do the coloring
        # in a second pass through rejection sampling.

        # For each row of rooms
        for j in range(0, 3):

            # For each column
            for i in range(0, 3):
                xL = i * roomW
                yT = j * roomH
                xR = xL + roomW
                yB = yT + roomH

                # Bottom wall and door
                if i+1 < 3:
                    grid.vertWall(xR, yT, roomH)
                    pos = (xR, self._randInt(yT+1, yB-1))
                    color = self._randElem(COLOR_NAMES)
                    grid.set(*pos, Door(color))

                # Bottom wall and door
                if j+1 < 3:
                    grid.horzWall(xL, yB, roomW)
                    pos = (self._randInt(xL+1, xR-1), yB)
                    color = self._randElem(COLOR_NAMES)
                    grid.set(*pos, Door(color))

        # Randomize the player start position and orientation
        self.placeAgent(grid)

        # Place random objects in the world
        types = ['key', 'ball', 'box']
        for i in range(0, 12):
            objType = self._randElem(types)
            objColor = self._randElem(COLOR_NAMES)
            if objType == 'key':
                obj = Key(objColor)
            elif objType == 'ball':
                obj = Ball(objColor)
            elif objType == 'box':
                obj = Box(objColor)
            self.placeObj(grid, obj, self.startPos)

        # No explicit mission in this environment
        self.mission = ''

        return grid

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        return obs, reward, done, info

register(
    id='MiniGrid-Playground-v0',
    entry_point='gym_minigrid.envs:PlaygroundV0'
)

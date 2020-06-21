class Numbers:
    def __init__(self, numb: int, x: int, y: int):
        self.numb = numb
        self.x = x
        self.y = y


class Board:
    Start_poses = []
    Start_poses.append([[4, 4], [1, 1], [2, 1], [3, 1], [4, 1], [1, 2],
                        [2, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3],
                        [4, 3], [1, 4], [2, 4], [3, 4]])
    Start_poses.append([[1, 4], [3, 2], [3, 3], [3, 1], [4, 1], [2, 3],
                        [1, 1], [4, 3], [1, 3], [3, 4], [2, 4], [2, 2],
                        [2, 1], [4, 4], [4, 2], [1, 2]])
    Start_poses.append([[1, 4], [3, 1], [4, 1], [2, 1], [1, 3], [2, 4],
                        [1, 1], [3, 4], [4, 4], [3, 3],
                        [3, 2], [1, 2], [2, 3], [4, 3], [4, 2], [2, 2]])

    def __init__(self, size: int):
        self.size = size
        self.numbs = []
        self.freecell = [self.size, self.size]
        for i in range(1, self.size*self.size):
            self.numbs.append(Numbers(i, ((i-1) % self.size)+1,
                                      ((i-1)//self.size)+1))

    def is_move_possible(self, coord: dict):
        for each in coord.keys():
            if coord[each] < 0 or coord[each] > self.size:
                return False
        if not ((abs(coord['first_x']-coord['second_x']) == 1
                 and coord['first_y'] == coord['second_y']) or
                (abs(coord['first_y']-coord['second_y']) == 1
                 and coord['first_x'] == coord['second_x'])):
            return False
        if coord['second_x'] == self.freecell[0] \
                and coord['second_y'] == self.freecell[1]:
            return True
        return False

    def move_body(self, coord: dict):
        for numb in self.numbs:
            if coord['first_x'] == numb.x and coord['first_y'] == numb.y:
                numb.x, self.freecell[0] = self.freecell[0], numb.x
                numb.y, self.freecell[1] = self.freecell[1], numb.y
                break

    def move_cells(self, coord: dict):
        if self.is_move_possible(coord):
            self.move_body(coord)
            return True
        else:
            return False

    def check_for_solving(self):
        if not (self.freecell[0] == self.Start_poses[0][0][0]
                and self.freecell[1] == self.Start_poses[0][0][1]):
            return False
        for i in range(0, self.size * self.size-1):
            if not(self.numbs[i].x == self.Start_poses[0][i+1][0]
                   and self.numbs[i].y == self.Start_poses[0][i+1][1]):
                return False
        return True

    def start_pose(self, pos_number: int):
        self.freecell = self.Start_poses[pos_number][0].copy()
        self.numbs.clear()
        for i in range(1, self.size*self.size):
            self.numbs.append(Numbers(i, self.Start_poses[pos_number][i][0],
                                      self.Start_poses[pos_number][i][1]))

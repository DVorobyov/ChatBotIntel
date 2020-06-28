from game.Board import Board


class Renderer:

    @staticmethod
    def render_list(board: Board):  # list:int
        coord_list = []  # x: int , y: int
        render_queue = []
        for i in range(board.size*board.size):
            coord_list.append([i % board.size + 1, i // board.size+1])
        for cell in coord_list:
            if cell[0] == board.freecell[0] and cell[1] == board.freecell[1]:
                render_queue.append(0)
            for numb in board.numbs:
                if numb.x == cell[0] and numb.y == cell[1]:
                    render_queue.append(numb.numb)
        return render_queue

    @staticmethod
    def symbol_translate(numb: int):  # string
        if numb > 0:
            return chr(9312+numb-1)
        else:
            return chr(9711)

    @staticmethod
    def render(board: Board):
        board_draw = ''
        render_queue = Renderer.render_list(board)
        board_draw = chr(9679)+' '
        for i in range(0, board.size):
            board_draw += chr(ord('a')+i)+'  '
        counter = 0
        for i in range(1, len(render_queue)+1):
            if (i-1) % board.size == 0:
                counter += 1
                board_draw += '\n'+str(counter)+' '
            board_draw += Renderer.symbol_translate(render_queue[i-1])
        return board_draw

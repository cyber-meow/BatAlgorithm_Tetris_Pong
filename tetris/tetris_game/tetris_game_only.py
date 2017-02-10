from random import randrange as rand
from random import randint


# Define the shapes of the single parts
tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]


def rotate_clockwise(shape):
    return [ [ shape[y][x]
        for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
        	mat1[cy+off_y-1][cx+off_x] += val
    return mat1


def remove_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            if val:
                mat1[cy+off_y-1][cx+off_x] = 0
    return mat1


class grille(object):
    
    def __init__(self, cols=10, rows=22):
        self.cols = cols
        self.rows = rows
        self.board = self.new_board()
            
    def check_collision(self,shape,offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[ cy + off_y ][ cx + off_x ]:
                        return True
                except IndexError:
                        return True
        return False
            
    def remove_rows(self,rows):
        newboard = self.new_board()
        del_rows = []
        rows.reverse()
        decalage = len(rows)
        for y in range(decalage,self.rows):
            while rows != [] and y-decalage == rows[-1]:
                del_rows.append((rows[-1],self.board[rows[-1]]))
                rows.pop()
                decalage -= 1
            newboard[y] = self.board[y-decalage]
        while rows != [] and y+1-decalage == rows[-1]:
            del_rows.append((rows[-1],self.board[rows[-1]]))
            rows.pop()
            decalage -= 1
        self.board = newboard
        return del_rows
        
    def add_rows(self,rows):
        oldboard = self.new_board()
        rows.reverse()
        decalage = len(rows)
        y = 0
        while y < self.rows:
            while rows != [] and y == rows[-1][0]:
                oldboard[y] =  rows[-1][1]
                y += 1
                decalage -= 1
                rows.pop()
            oldboard[y] = self.board[y+decalage]
            y += 1
        self.board = oldboard
            	
    def new_board(self):
        board = [ [ 0 for x in range(self.cols) ] for y in range(self.rows) ]
        board += [[ 1 for x in range(self.cols)]]
        return board



class TetrisApp1(object):
    
    def __init__(self, cols=10, rows=22):
        self.cols = cols
        self.rows = rows
        self.grille = grille(cols,rows)
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()
         
    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(self.cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if self.grille.check_collision(self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.grille.board = self.grille.new_board()
        self.heights = []
        self.new_stone()
        self.lines = 0        

    def add_cl_lines(self, n):
        self.lines += n
        self.heights.extend([self.height_max()]*n)
	
    def move(self, delta_x):
        if not self.gameover:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > self.cols - len(self.stone[0]):
                new_x = self.cols - len(self.stone[0])
            if not self.grille.check_collision(
                self.stone,(new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self):
        if not self.gameover:
            self.stone_y += 1
            if self.grille.check_collision(self.stone,
                                           (self.stone_x, self.stone_y)):
                self.grille.board = join_matrixes(
                    self.grille.board,
                    self.stone,
                    (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = []
                for i in range(self.rows):
                    row = self.grille.board[i]
                    if 0 not in row:
                        cleared_rows.append(i)
                if cleared_rows != []:
                    self.add_cl_lines(len(cleared_rows))
                    self.grille.remove_rows(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover:
            while(not self.drop()):
                pass

    def rotate_stone(self):
        if not self.gameover:
            new_stone = rotate_clockwise(self.stone)
            if not self.grille.check_collision(new_stone,
                                             (self.stone_x, self.stone_y)):
                self.stone = new_stone
                
    
    def transformer(self):
        bo_trans = [[self.grille.board[j][i] for j in range(self.rows+1)] for i in range(self.cols)]
        return bo_trans

    def set_height_colonne(self):
        bo_trans = self.transformer()
        self.h_c = [self.rows]*self.cols
        for x,col in enumerate(bo_trans):
            y = 0
            while col[y] == 0:
                y += 1
                self.h_c[x] -= 1
    
    def height_max(self):
        self.set_height_colonne()
        return max(self.h_c)


class TetrisApp_z(TetrisApp1):
    
    def __init__(self, cols=10, rows=22):
        self.cols = cols
        self.rows = rows
        self.grille = grille(cols,rows)
        self.next_stone = tetris_shapes[randint(1,2)]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[randint(1,2)]
        self.stone_x = int(self.cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if self.grille.check_collision(self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True
            
            
class TetrisApp_z_ordre(TetrisApp1):
    
    def __init__(self, cols=10, rows=22):
        self.cols = cols
        self.rows = rows
        self.grille = grille(cols,rows)
        self.shape = 0
        self.next_stone = tetris_shapes[self.shape%2+1]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.shape += 1
        self.next_stone = tetris_shapes[self.shape%2+1]
        self.stone_x = int(self.cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if self.grille.check_collision(self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True



class TetrisApp_dans_lordre(TetrisApp1):
    
    def __init__(self, cols=10, rows=22):
        self.cols = cols
        self.rows = rows
        self.grille = grille(cols,rows)
        self.shape = 0
        self.next_stone = tetris_shapes[self.shape]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.shape += 1
        self.next_stone = tetris_shapes[self.shape%(len(tetris_shapes))]
        self.stone_x = int(self.cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if self.grille.check_collision(self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True
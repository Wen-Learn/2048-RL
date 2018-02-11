# -*- coding: utf-8 -*-
'''
Created on Sat Feb 10 23:22:48 2018

@author: Wen

'''
import numpy as np
import random

# the 2048 game

class Board(object):
    def __init__(self, board_size=4):
        self.board_size = board_size
        self.actions = ['L', 'U', 'R', 'D']
        # sometimes certain action is not available
        self.available_actions = self.actions
        self.new_num = [2, 4]
        self.game_over = False
        self.indices = np.arange(board_size)
        # use 2 arrays to record the state of the board
        # 1-D array is easy to choose empty cells, 2-D array easy to check game status
        self.state = np.zeros(board_size * board_size)
        self.state_square = np.zeros((board_size, board_size))
        # randomly fill two cells in the board
        self.update()
        self.update()
        self.check_all()
    
    # check whether sliding to left is available
    def check(self):
        available = False
        # the game ends only if all actions are unavailable
        # check for sliding left
        # for other directions rotate the board and call the same function
        for i in self.indices:
            # store the original values in the row for update
            values = list(self.state_square[i])
            empty_indices = [j for j in self.indices if values[j] == 0]
            # if all cells are empty then continue to check the next row
            if len(empty_indices) == self.board_size:
                continue
            num_indices = [j for j in self.indices if values[j] > 0]
            # as long as the rightmost number is in the right of the leftmost empty cell then the action is available
            if empty_indices != []:
                if min(empty_indices) < max(num_indices):
                    available = True
                    break
            # otherwise only can move if adjacent cells are of the same value
            # in this case if number of numbered cells has to be greater than 1
            num_len = len(num_indices)
            if num_len < 2:
                continue
            else:
                for j in range(num_len - 1):
                    if values[num_indices[j]] == values[num_indices[j+1]]:
                        available = True
                        break
        return available
    
    # check all directions, if there is no available moves then game over
    def check_all(self):
        self.available_actions = []
        
        action = 'L'
        if self.check():
            self.available_actions.append(action)
            
        action = 'U'
        self.state_square = np.rot90(self.state_square, 1)
        if self.check():
            self.available_actions.append(action)
        self.state_square = np.rot90(self.state_square, 3)
        
        action = 'D'
        self.state_square = np.rot90(self.state_square, 3)
        if self.check():
            self.available_actions.append(action)
        self.state_square = np.rot90(self.state_square, 1)
        
        action = 'R'
        self.state_square = np.flip(self.state_square, 1)
        if self.check():
            self.available_actions.append(action)
        self.state_square = np.flip(self.state_square, 1)
        
        if self.available_actions == []:
            self.game_over = True
        else:
            self.game_over = False
    
    # slide the board to the left
    def slide(self):
        for i in self.indices:
            # store the original values in the row for update
            # need to make a new list, otherwise it is merely a reference
            values = list(self.state_square[i])
            empty_indices = [j for j in self.indices if values[j] == 0]
            # if all cells are empty then continue to check the next row
            if len(empty_indices) == self.board_size:
                continue
            num_indices = [j for j in self.indices if values[j] > 0]
            num_len = len(num_indices)
            
            self.state_square[i] = 0
            if num_len < 2:
                self.state_square[i][0] = values[num_indices[0]]
            else:
                j = 0
                pos = 0
                while j < num_len:
                    # whether reaches the last element
                    if j < num_len - 1:
                        if values[num_indices[j]] == values[num_indices[j+1]]:
                            self.state_square[i][pos] = 2 * values[num_indices[j]]
                            j += 2
                            pos += 1
                            continue
                        
                    self.state_square[i][pos] = values[num_indices[j]]
                    j += 1
                    pos += 1    
    
    # randomly choose an empty cell to fill it with 2 or 4 randomly
    def update(self):
        idx = random.choice([i for i in range(self.board_size * self.board_size) if self.state[i] == 0])
        new_num = random.choice(self.new_num)
        # need to update both state arrays
        self.state[idx] = self.state_square[int(np.floor(idx / self.board_size))][idx % self.board_size]  = new_num
    
    # make a move using a certain action
    def move(self, action):
        # for different action, rotate the matrix correspondingly and slide to the left
        # then restore the matrix afterward
        # 'U' and 'D' corresponds to rotate 90 and 270 degrees
        # 'R' corresponds to flip the matrix
        if not action in self.available_actions:
            print(action, 'is not an available action.')
            return False
        
        print('Making a move:', action)
        if action == 'R':
            self.state_square = np.flip(self.state_square, 1)
            self.slide()
            self.state_square = np.flip(self.state_square, 1)
        else:
            rot = self.actions.index(action)
            self.state_square = np.rot90(self.state_square, rot)
            self.slide()
            self.state_square = np.rot90(self.state_square, 4 - rot)
        
        self.state = self.state_square.flat[:]
        
        return True
        
    # make a random move
    def random_move(self):
        self.move(random.choice(self.available_actions))
    
    def score(self):
        return max(self.state)
    
    def show(self):
        print(self.state_square.astype(int))

if __name__ == '__main__':
    board = Board(4)
    board.show()
    steps = 0
    while not board.game_over:
        steps += 1
        board.random_move()
        board.update()
        board.show()
        board.check_all()
        if board.game_over:
            print('Game over!')
            print('Score:', board.score())
            print('Steps:', steps)
            break
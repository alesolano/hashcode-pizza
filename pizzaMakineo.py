#
# Google Hash Code 2017 - Practice Round
#
# Copyright (c) 2017 Team "Makineo"
#
# Version 1.0
#


import numpy as np
import math
import sys


def read_file(filename):
    '''
    Read the file.
    Return the pizza as a binary matrix: Tomatoes = 1, Mushrooms = 0
    Also, return the minimum ingredients required for each slice,
    and the maximum cells allowed for each slice.
    '''
    
    with open(filename, 'r') as f:
        line = f.readline()
        rows, cols, min_ings, max_cells = [int(n) for n in line.split()]
        
        pizza = np.zeros([rows, cols])
        for row in range(rows):
            for ing, col in zip(f.readline(), range(cols)):
                if ing == 'T':
                    pizza[row, col] = 1
                else:
                    pizza[row, col] = 0
    
    return pizza, min_ings, max_cells


class PizzaCutter:
    
    def __init__(self, pizza, L, H):
        self.pizza = pizza
        self.L = L
        self.H = H
    
    def isInside(self, R, C):
        '''
        Check if the slice is within the boundaries of the pizza
        '''
        try:
            assert (R[0] >= 0) and (C[0] >= 0)
            self.pizza[R[0], C[0]] # try if the upper left corner is inside the pizza
            self.pizza[R[1], C[1]] # try if the lower right corner is inside the pizza
            return True
        except:
            return False
    
    def satisfyH(self, R, C):
        '''
        Check if the slice satisfies the H condition.
        Also, prevent the slice to include cells of other slices.
        '''
        legal = False
        if self.isInside(R, C):
            slic = self.pizza[R[0]:R[1]+1, C[0]:C[1]+1] 
            if slic.size <= self.H and not math.isnan(slic.sum()):
                # if there's one or more cells with NaN value, the sum is NaN
                legal = True    
        return legal
    
    def satisfyL(self, R, C):
        '''
        Check if the slice satisfies the L condition
        '''
        slic = self.pizza[R[0]:(R[1]+1), C[0]:(C[1]+1)] # slice of pizza
        tomatoes = np.sum(slic)
        mushrooms = np.size(slic) - tomatoes
        
        if (tomatoes >= self.L) and (mushrooms >= self.L):
            return True
        else:
            return False
    
    @staticmethod
    def enlargeSlice(R, C, direction):
        '''
        Enlarge the pizza to the direction given
        '''
        newR = list(R)
        newC = list(C)
        if direction == 'right':
            newC[1] += 1
            nextDir = 'down'
        elif direction == 'down':
            newR[1] += 1
            nextDir = 'left'
        elif direction == 'left':
            newC[0] -= 1
            nextDir = 'up'
        elif direction == 'up':
            newR[0] -= 1
            nextDir = 'right'
        return newR, newC, nextDir
    
    
    def newSlice(self, point):
        '''
        Take a seed point and returns a slice if possible.
        point = [row, column]
        
        The returned slices is defined by R and C
        R: list [row_min, row_max] of the slice
        C: list [col_min, col_max] of the slice
        '''
        
        Rfinal = [point[0], point[0]]
        Cfinal = [point[1], point[1]]
        direction = 'right'
        out = False
        
        while(not out):
            legal = False
            counter = 0
            while(counter < 3):
                # Try enlarge the slice by all four directions
                R, C, direction = self.enlargeSlice(Rfinal, Cfinal, direction)
                if self.satisfyH(R, C):
                    legal = True
                    Rfinal = R
                    Cfinal = C
                    print(Rfinal, Cfinal)
                    break
                counter += 1
            if not legal:
                out = True
        
        success = self.satisfyL(Rfinal, Cfinal)
        return success, Rfinal, Cfinal
    
    def updatePizza(self, R, C):
        '''
        Fill with NaN a slice of the pizza
        '''
        slic = np.empty([R[1]-R[0]+1, C[1]-C[0]+1])
        slic[:] = None
        self.pizza[R[0]:R[1]+1, C[0]:C[1]+1] = slic
    
    def start(self):
        '''
        Try to generate a slice from each cell of the pizza
        '''
        self.slices = []
        for row in range(self.pizza.shape[0]):
            for col in range(self.pizza.shape[1]):
                if not math.isnan(self.pizza[row][col]):
                    success, R, C = self.newSlice([row,col])
                    if success:
                        print("Success")
                        self.slices += [[R[0], C[0], R[1], C[1]]]
                        self.updatePizza(R, C)
        print(self.pizza)


def write_file(cutter, filename):
    '''
    Write the output file
    '''
    with open(filename, 'w') as f:
        f.write('{}\n'.format(len(cutter.slices)))
        for slic in cutter.slices:
            f.write(' '.join([str(item) for item in slic]) + '\n')


def main():
    '''
    Main function
    '''
    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    print('Running on file %s' % sys.argv[1])

    pizza, L, H = read_file(sys.argv[1])
    cortapisa = PizzaCutter(pizza, L, H)
    cortapisa.start()

    write_file(cortapisa, sys.argv[2])


if __name__ == '__main__':
    main()
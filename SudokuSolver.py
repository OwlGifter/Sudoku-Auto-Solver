# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:03:51 2023

@author: Zabdiel Hernandez
"""
import numpy as np
import matplotlib.pyplot as plt

class Sudoku:
    def __init__(self, A):
        #set string or array to the main array in the sudoku class
        if(type(A) == str):
            NA = [i for i in A]
            for i in range(len(A)):
                if NA[i] == '.':
                    NA[i] = 0
                else:
                    NA[i] = int(NA[i])
            NA = np.array(NA)
            NA = NA.reshape(9,9)
            self.S = np.copy(NA)
        else:
            self.S = np.copy(A)
    
    def print(self):
        print(self.S)
    
    def draw(self, title = '', show_rc_nums = False, show_valid_vals = False):
        #draw the lines
        fig, self.ax = plt.subplots(figsize = (8,8))
        for i in range(0,10,3):
            self.ax.plot([i,i], [0,9], linewidth = 2, color = 'k')
            self.ax.plot([0,9], [i,i], linewidth = 2, color = 'k')
        for i in range(1,9):
            self.ax.plot([i,i], [0,9], linewidth = 1, color = 'k')
            self.ax.plot([0,9], [i,i], linewidth = 1, color = 'k')
        
        #print row and column
        if show_rc_nums:
            for i in range(9):
                self.ax.text((-.5), (i+.5), str(i), size = 12, color = 'r',
                             ha = "center", va = "center")
                self.ax.text((i+.5), (-.5), str(i), size = 12, color = 'r',
                             ha = "center", va = "center")
                
        #print values
        for i in range(9):
            for j in range(9):
                if self.S[i,j] != 0:
                    self.ax.text((j+.5), (i+.5), str(self.S[i,j]), size = 18,
                                 ha = "center", va = "center")
        
        
        #print valid values using green numbers if wanted
        if show_valid_vals and hasattr(self, 'V'):
            for i in range(9):
                for j in range(9):
                    if self.S[i,j] == 0:
                        for n in self.V[(i,j)]:
                            n1 = n-1
                            self.ax.text((j+.5+(n1%3-1)*.25), (i+.5+(n1//3-1)*.25),
                                         color = 'g', ha = "center", va = "center")
        
        self.ax.axis('off')
        self.ax.set_title(title, y=-.05, size = 18)
        self.ax.set_aspect(1.0)
        self.ax.invert_yaxis()
        plt.show()
        
    def find_neighbors(self):
        # filling dictionary N so that N[(r,c)], where (r,c) are
        # coordinates of a cell, contains the set of cells that
        # are in the same row, column or 3 by 3 region as cell (r,c)
        
        self.N = {}
        # add neighbors in column and row
        for i in range(9):
            for j in range(9):
                tempr = int (i/3)*3
                tempc = int (j/3)*3
                tempSet = set()
                for k in range(9):
                    tempSet.add((i,k))
                    tempSet.add((k,j))
                #add neighbors in 3 by 3 square
                for t in range(3):
                    for k in range(3):
                        tempSet.add(((tempr)+t, (tempc)+k))
                tempSet.discard((i,j))
                tempList = list(tempSet)
                self.N[(i,j)] = tempList
    
    def init_valid(self):
        #Fill out dictionary V so that V[(r,c)], where (r,c) are
        # coordinates of a cell, contains the set of ints that can
        # be written in cell (r,c) without braking sudoku rules
        #If a number has already been written in cell (r,c), then
        #V[(r,c)] should contain the empty set
        
        self.V = {(i,j) : set(np.arange(1,10)) for i in range(9) for j in range(9)}
        for i in range(9):
            for j in range(9):
                if self.S[i,j] != 0:
                    self.V[i,j].clear()
                else:
                    for k in self.N[i,j]:
                        if self.S[k] != 0:
                            temp = self.S[k]
                            self.V[i,j].discard(temp)
    
    def solve(self):
        self.find_neighbors()
        self.init_valid()
        known = set()
        for i in range(9):
            for j in range(9):
                if len(self.V[i,j]) == 1:
                    tempc = list(self.V[i,j])
                    known.add((tempc[0], i, j))
        while len(known) > 0:
            known2 = known.copy()
            for i in known:
                self.S[i[1], i[2]] = i[0]
                self.V[(i[1], i[2])] = set()
                known2.discard(i)
            self.init_valid()
            for i in range(9):
                for j in range(9):
                    if len(self.V[i,j]) ==1:
                        tempc = list(self.V[i,j])
                        known2.add((tempc[0], i, j))
            known = known2.copy()
        filled = True
        empty = False
        for i in range(9):
            for j in range(9):
                if self.S[i,j] == 0:
                    filled = False
                    if len(self.V[i,j]) == 0:
                        empty = True
        if(filled):
            return 1
        else:
            if(empty):
                return -1
            return 0
        
    def to_string(self):
        #returns a string of length 81 representing the board
        tempstr = ''
        tempArr = np.copy(self.S)
        tempArr = tempArr.reshape(-1)
        for i in tempArr:
            if(i == 0):
                tempstr += '.'
            else:
                tempstr += str(i)
        return tempstr
    
    
    
    
def solve_backtrack(s):
    #uses back tracking to look for possible solutions
    S = Sudoku(s)
    sol = S.solve()
    if(sol == 1):
        return S.to_string()
    if(sol == -1):
        return None
    
    for i in range(9):
        for j in range(9):
            if S.S[i,j] == 0:
                for v in S.V[i,j]:
                    S.S[i,j] = v
                    sol = solve_backtrack(S.to_string())
                    if sol != None:
                        return sol
                return None


        
def askForUnSolvedSudoku():
    int = input("Please put in a unsolved sudoku using 0's as an empty slot,make sure there are no spaces: \n")
    
    
    return int       
        
B = askForUnSolvedSudoku()
s = solve_backtrack(B) 
S = Sudoku(s)
S.draw()
        
        
        
        
        
        
        
        

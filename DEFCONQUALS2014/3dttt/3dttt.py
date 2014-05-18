from autosockets import *
import random
import re

s = socket('3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me',1234)

used = []

def display_board(board):
    for i,x in enumerate(board):
        if i%3 == 0:
            print "=============="
        print x 


def best_move(board):
    first = board[:3]
    second = board[3:6]
    third = board[6:]
    boards = [first, second, third]

    try:
        if second[1][1] == " ":
            return "1,1,1"
        if second[0][0] == " ":
            return "0,0,1"
        if second[0][2] == " ":
            return "2,0,1"
        if second[2][0] == " ":
            return "0,2,1"
        if second[2][2] == " ":
            return "2,2,1"
    except:
        print board

    # check horizontal 3d
    for x in range(3):
        for y in range(3):
            row = [first[x][y], second[x][y], third[x][y]]
            if row.count('O') == 2 and row.count(' ') == 1:
                print "horizontal 3d"
                if row.index(' ') == 0:
                    return "{0},{1},{2}".format(y, x, 0)
                elif row.index(' ') == 1:
                    return "{0},{1},{2}".format(y, x, 1)
                elif row.index(' ') == 2:
                    return "{0},{1},{2}".format(y, x, 2)

    # check diagonal 3d
    diag1 = [first[2][2], second[1][1], third[0][0]]
    diag2 = [first[2][0], second[1][1], third[0][2]]
    diag3 = [first[0][2], second[1][1], third[2][0]]
    diag4 = [first[0][0], second[1][1], third[2][2]]
    diags = [diag1, diag2, diag3, diag4]
    for i, row in enumerate(diags):
        if row.count('O') == 2 and row.count(' ') == 1:
            print "diagonal 3d"
            print i, row
            if i == 0:
                loc = row.index(" ")
                if loc == 0:
                    return "{0},{1},{2}".format(2, 2, loc)
                elif loc == 1:
                    return "{0},{1},{2}".format(1, 1, loc)
                elif loc == 2:
                    return "{0},{1},{2}".format(0, 0, loc)
            elif i == 1:
                loc = row.index(" ")
                if loc == 0:
                    return "{0},{1},{2}".format(0, 2, loc)
                elif loc == 1:
                    return "{0},{1},{2}".format(1, 1, loc)
                elif loc == 2:
                    return "{0},{1},{2}".format(2, 0, loc)
            elif i == 2:
                loc = row.index(" ")
                if loc == 0:
                    return "{0},{1},{2}".format(2, 0, loc)
                elif loc == 1:
                    return "{0},{1},{2}".format(1, 1, loc)
                elif loc == 2:
                    return "{0},{1},{2}".format(0, 2, loc)
            elif i == 3:
                loc = row.index(" ")
                if loc == 0:
                    return "{0},{1},{2}".format(0, 0, loc)
                elif loc == 1:
                    return "{0},{1},{2}".format(1, 1, loc)
                elif loc == 2:
                    return "{0},{1},{2}".format(2, 2, loc)


    for j,y in enumerate(boards):
        try:
            if y[1][1] == " ":
                return "1,1,{0}".format(j)
            if y[0][0] == " ":
                return "0,0,{0}".format(j)
            if y[0][2] == " ":
                return "2,0,{0}".format(j)
            if y[2][0] == " ":
                return "0,2,{0}".format(j)
            if y[2][2] == " ":
                return "2,2,{0}".format(j)
        except:
            print board

        # check horizontal
        for i,x in enumerate(y): 
            if x.count('X') == 2 and x.count(' ') == 1:
                print "horizontal"
                return "{0},{1},{2}".format(x.index(' '), i, j)

        # check vertical
        col1=[y[0][0], y[0][1], y[0][2]]
        col2=[y[1][0], y[1][1], y[1][2]]
        col3=[y[2][0], y[2][1], y[2][2]]
        cols = [col1, col2, col3]
        for k, col in enumerate(cols):
            if col.count('X') == 2 and col.count(' ')==1:
                print "vertical"
                return "{0},{1},{2}".format(k, col.index(' '), j)

        # check diagonal
        diag1 = [y[0][0], y[1][1], y[2][2]]
        diag2 = [y[0][2], y[1][1], y[2][0]]
        if diag1.count('X') == 2 and diag1.count(" ") == 1:
            print "diagonal"
            return "{0},{1},{2}".format(diag1.index(" "), diag1.index(" "),j)

    # just play a move
    for i,y in enumerate(boards):
        for j, line in enumerate(y):
            if line.count(" ") > 0:
                print "garbage"
                return "{0},{1},{2}".format(line.index(' '), j, i)



def parse_board(board):
    final = []
    board = board[board.find(' x 0   1   2    z=0'):board.find('Choose Wisely (x,y,z):')]
    board = board.split('\n')
    for x in board:
        if len(x) > 0 and (x[0] == "0" or x[0] == "1" or x[0] == "2"):
            # print x
            final.append( (x[3], x[7], x[11]) )
    return final

while 1: 
    data = s.recv()
    print repr(data)
    if "You've won" in data:
        print " "
        print " "
        print " "
        print " "
        print data[data.find("You've won"):data.find('...')]
        print " "
        print " "
        print " "
        print " "
    if "play again" in data:
        data = data[data.find("play again"):]
    board = parse_board(data)
    # print ""
    # display_board( board )
    # print ""
    move = best_move(board)+'\n'
    # print move
    s.send(move)
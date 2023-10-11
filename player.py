import pygame
import chess
from variable import *

def player_turn(board, xmouse, ymouse, mychess, promote):
    global tmp1, tmp2
    x = (xmouse - 32) // 62
    y = (ymouse - 32) // 62
    if 0 <= x <= 7 and 0 <= y <= 7:
        square = chess.square(x, 7 - y)
        piece = board.piece_at(square)
        if piece and piece.color == mychess:
            for i in board.legal_moves:
                j = str(i)
                if j[0] == chr(ord('a') + x) and j[1] == str(8 - y):
                    m = ord(j[2]) - ord('a')
                    n = int(j[3])
                    pygame.draw.rect(screen, green, pygame.Rect(32 + m * size, 32 + (8 - n) * size, size, size))
                    tmp1, tmp2 = x, y
        else:
            move = str(chr(ord('a') + tmp1)) + str(8 - tmp2) + str(chr(ord('a') + x)) + str(8 - y)
            for i in board.legal_moves:
                j = str(i)
                if len(j) == 4:
                    if j[0:4] == move:
                        board.push(i)
                        move_history.append(str(i))
                        break
                else:
                    if j[0:4] == move and j[4] == promote:
                        board.push(i)
                        move_history.append(str(i))
                        break

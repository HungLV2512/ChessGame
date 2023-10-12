import pygame
import chess
from player import player_turn
from variable import *
    
if __name__ == "__main__":
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                xmouse, ymouse = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                if mychess == '':
                    mychess = chess.BLACK
                    turn = 1
                    start = True
                else:
                    promote = 'b'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                if mychess == '':
                    mychess = chess.WHITE
                    turn = 0
                    start = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                promote = 'r'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                promote = 'n'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                promote = 'q'
            
        if start == False:
            draw_text('Press B(Black) or W(White)', (0, 200), 64, whitee)
            draw_text('to choose', (250, 300), 64, whitee)
            
        else:
            draw_board()
            
            pre_move()
            
            if turn == 1:
                move = computer.get_computer_move(depth)
                board.push(move)
                move_history.append(str(move))
                turn = 0
            
            if turn == 0:
                length = len(move_history)
                player_turn(board, xmouse, ymouse, mychess, promote)
                if len(move_history) - length == 1:
                    turn = 1
                    xmouse, ymouse = 0, 0

            if xmouse >= 560 and ymouse >= 500:
                if len(move_history) >= 2:
                    board.pop()
                    move_history.pop()
                    board.pop()
                    move_history.pop()
                    xmouse, ymouse = 0, 0
            
            draw_pieces_and_texts(mychess, promote)
            
            end_game()
            
        fpsClock.tick(FPS)    
        pygame.display.flip()
        screen.fill((0, 0, 0))

    pygame.quit()
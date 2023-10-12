import pygame
import chess
from ai import AI

pygame.init()
FPS = 20
fpsClock = pygame.time.Clock()

width, height = 720, 560
size = 62
white = (232, 235, 239)
grey = (125, 135, 150)
green = (50, 205, 50)
yellow = (255, 223, 0)
blue = (0, 0, 128)
purple = (128, 0, 128)
red = (255, 0, 0)
whitee = (255, 255, 255)

screen = pygame.display.set_mode((width, height))

board = chess.Board()
computer = AI(board)
move_history = []
depth = 3

turn = -1
mychess = ''
run = True
tmp1, tmp2 = -1, -1
xmouse, ymouse = -1, -1
start = False
last_move = ''
promote = 'q'

pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load('images/black/blackknight.png'))

blackbishop = pygame.image.load('images/black/blackbishop.png')
blackking = pygame.image.load('images/black/blackking.png')
blackknight = pygame.image.load('images/black/blackknight.png')
blackpawn = pygame.image.load('images/black/blackpawn.png')
blackqueen = pygame.image.load('images/black/blackqueen.png')
blackrook = pygame.image.load('images/black/blackrook.png')

whitebishop = pygame.image.load('images/white/whitebishop.png')
whiteking = pygame.image.load('images/white/whiteking.png')
whiteknight = pygame.image.load('images/white/whiteknight.png')
whitepawn = pygame.image.load('images/white/whitepawn.png')
whitequeen = pygame.image.load('images/white/whitequeen.png')
whiterook = pygame.image.load('images/white/whiterook.png')

def draw_piece(piece_type, color, image):
    for i in board.pieces(piece_type, color):
        x = 7 - (i // 8)
        y = i % 8
        screen.blit(image, (32 + y * size, 32 + x * size))

def draw_text(x, pos, s, color):
    font = pygame.font.SysFont('Times New Roman', s)
    text = font.render(x, True, color)
    screen.blit(text, pos)
    
def draw_board():
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white, pygame.Rect(32 + i * size, 32 + j * size, size, size))
            else:
                pygame.draw.rect(screen, grey, pygame.Rect(32 + i * size, 32 + j * size, size, size))
                
def end_game():
    if board.is_checkmate():
        draw_text('Black win', (200, 250), 64, red) if board.turn else draw_text('White win', (200, 250), 64, red)
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        draw_text('Draw', (200, 250), 64, red)
        
def draw_pieces_and_texts(mychess, promote):
         
    draw_piece(chess.PAWN, chess.WHITE, whitepawn)
    draw_piece(chess.PAWN, chess.BLACK, blackpawn)
    draw_piece(chess.KNIGHT, chess.WHITE, whiteknight)
    draw_piece(chess.KNIGHT, chess.BLACK, blackknight)
    draw_piece(chess.BISHOP, chess.WHITE, whitebishop)
    draw_piece(chess.BISHOP, chess.BLACK, blackbishop)
    draw_piece(chess.ROOK, chess.WHITE, whiterook)
    draw_piece(chess.ROOK, chess.BLACK, blackrook)
    draw_piece(chess.QUEEN, chess.WHITE, whitequeen)
    draw_piece(chess.QUEEN, chess.BLACK, blackqueen)
    draw_piece(chess.KING, chess.WHITE, whiteking)
    draw_piece(chess.KING, chess.BLACK, blackking)   
    
    pygame.draw.rect(screen, blue, pygame.Rect(560, 0, 260, 560))
    draw_text('Promote : ' + promote, (560, 0), 32, whitee)
    
    length = len(move_history)
    if length < 10:
        for i in range(length):
            draw_text(str(i + 1) + ' : ' + move_history[i], (560, 300 + i * 20), 18, whitee)
    else:
        for i in range(10):
            draw_text(str(length - 9 + i) + ' : ' + move_history[length - 10 + i], (560, 300 + i * 20), 18, whitee)
            
    pygame.draw.rect(screen, purple, pygame.Rect(560, 500, 160, 60))
    draw_text('Undo', (600, 510), 40, whitee)
    
    for i in range(8):
        draw_text(str(8 - i), (8, 42 + size * i), 32, whitee)
        draw_text(str(8 - i), (536, 42 + size * i), 32, whitee)
        draw_text(chr(ord('a') + i), (56 + size * i, -6), 32, whitee)
        draw_text(chr(ord('a') + i), (56 + size * i, 524), 32, whitee)
    
def pre_move():
    if len(move_history) != 0:
        last_move = move_history[-1]
        x1 = ord(last_move[0]) - ord('a')
        y1 = int(last_move[1])
        x2 = ord(last_move[2]) - ord('a')
        y2 = int(last_move[3])
        pygame.draw.rect(screen, yellow, pygame.Rect(32 + x1 * size, 32 + (8 - y1) * size, size, size))
        pygame.draw.rect(screen, yellow, pygame.Rect(32 + x2 * size, 32 + (8 - y2) * size, size, size))
        
    if board.is_check() and not board.is_checkmate():
        draw_text('Check', (200, 250), 64, red)
        for move in board.legal_moves:
            str_move = str(move)
            x1 = ord(str_move[0]) - ord('a')
            y1 = int(str_move[1])
            pygame.draw.rect(screen, purple, pygame.Rect(32 + x1 * size, 32 + (8 - y1) * size, size, size))
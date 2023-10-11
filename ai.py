import chess
from tables import *

class AI:
    def __init__(self, board):
        self.board = board
        
    def evaluate_move(self, move):
        self.board.push(move)
        attacked_pieces = len(self.board.attackers(chess.WHITE, move.to_square))
        self.board.pop()
        return attacked_pieces

    def sort_moves(self, maximizingPlayers):
        legal_moves = list(self.board.legal_moves)
        legal_moves.sort(key=lambda move: self.evaluate_move(move), reverse=maximizingPlayers)
        return legal_moves
        
    def evaluate_board(self):
        
        if self.board.is_stalemate():
            return 0
        if self.board.is_insufficient_material():
            return 0
        if self.board.is_seventyfive_moves():
            return 0
        if self.board.is_fivefold_repetition():
            return 0
        
        pawn = self.calculate_material_value(chess.PAWN)
        knight = self.calculate_material_value(chess.KNIGHT)
        bishop = self.calculate_material_value(chess.BISHOP)
        rook = self.calculate_material_value(chess.ROOK)
        queen = self.calculate_material_value(chess.QUEEN)
        king = self.calculate_material_value(chess.KING)
        
        material = 100*pawn + 320*knight + 330*bishop + 500*rook + 900*queen + 20000*king
        
        pawns = self.calculate_piece_value(chess.PAWN, pawnstable)
        knights = self.calculate_piece_value(chess.KNIGHT, knightstable)
        bishops = self.calculate_piece_value(chess.BISHOP, bishopstable)
        rooks = self.calculate_piece_value(chess.ROOK, rookstable)
        queens = self.calculate_piece_value(chess.QUEEN, queenstable)
        kings = self.calculate_piece_value(chess.KING, kingstable)
        
        eval = material + pawns + knights + bishops+ rooks+ queens + kings
        if self.board.turn:
            return eval
        else:
            return -eval
    
    def calculate_material_value(self, piece_type):
        w = len(self.board.pieces(piece_type, chess.WHITE))
        b = len(self.board.pieces(piece_type, chess.BLACK))
        return w - b
    
    def calculate_piece_value(self, piece_type, table):
        piece_value = sum([table[i] for i in self.board.pieces(piece_type, chess.WHITE)])
        piece_value += sum([-table[chess.square_mirror(i)] for i in self.board.pieces(piece_type, chess.BLACK)])
        return piece_value
    
    def get_move(self, n):
        x = n // 8
        y = n % 8
        return 8 * (7 - x) + y
    
    def eval_board(self, pre_score, from_move, from_piece, to_move, to_piece, tables, pieces):
        from_piece = from_piece.symbol().upper()
        to_piece = to_piece.symbol().upper() if to_piece is not None else None
        from_index = self.get_move(from_move)
        to_index = self.get_move(to_move)
        if to_piece is None:
            
            if self.board.turn:
                pre_score += tables[from_piece][to_index] - tables[from_piece][from_index]
            else:
                pre_score += tables[from_piece][chess.square_mirror(to_index)] - tables[from_piece][chess.square_mirror(from_index)]
                    
        else:
            
            if self.board.turn:
                pre_score += tables[from_piece][to_index] - tables[from_piece][from_index]
                pre_score += pieces[to_piece] + tables[to_piece][chess.square_mirror(to_index)]
            else:
                pre_score += tables[from_piece][chess.square_mirror(to_index)] - tables[from_piece][chess.square_mirror(from_index)]
                pre_score += pieces[to_piece] + tables[to_piece][to_index] 
            
        return -pre_score
    
    def alphabeta(self, alpha, beta, depth, maximizingPlayer):
        if depth == 0 :
            return self.quiesce(alpha, beta, 0, 0, None, 0, None, 0, False)
        sorted_moved = self.sort_moves(maximizingPlayer)
        if maximizingPlayer:
            maxEval = -9999
            for move in sorted_moved:
                self.board.push(move)
                eval = self.alphabeta(alpha, beta, depth - 1, False)
                self.board.pop()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = 9999
            for move in sorted_moved:
                self.board.push(move)
                eval = self.alphabeta(alpha, beta, depth - 1, True)
                self.board.pop()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
    
    def quiesce(self, alpha, beta, depth, from_move, from_piece, to_move, to_piece, pre_score, check):
        if depth == 0 or check == True:
            score_board = self.evaluate_board()
        else:
            score_board = self.eval_board(pre_score, from_move, from_piece, to_move, to_piece, tables, pieces)
            
        if score_board >= beta :
            return beta
        alpha = max(alpha, score_board)
        
        if depth == 3:
            return alpha
        
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                check = False
                if self.board.is_en_passant(move) or self.board.is_castling(move) or len(str(move)) == 5:
                    check = True
                tmp1, tmp2 = move.from_square, move.to_square
                tmp3, tmp4 = self.board.piece_at(tmp1), self.board.piece_at(tmp2)
                self.board.push(move)     
                score = -self.quiesce(-beta, -alpha, depth + 1, tmp1, tmp3, tmp2, tmp4, score_board, check)
                self.board.pop()
                if score >= beta :
                    return beta
                alpha = max(alpha, score) 
        return alpha
    
    def get_computer_move(self, depth):
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = -self.alphabeta(-beta, -alpha, depth - 1, True)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            alpha = max(alpha, board_value)
            self.board.pop()
        return best_move
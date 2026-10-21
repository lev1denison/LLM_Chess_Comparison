"""Scoring checks without inference or research-data access."""
import chess
from run_llm_puzzles import score_move

board = chess.Board()
assert score_move(board, 'e2e4\n', 'e2e4') == ('correct', 'e2e4')
assert score_move(board, 'd2d4', 'e2e4')[0] == 'legal_incorrect'
assert score_move(board, 'e2e5', 'e2e4')[0] == 'illegal_move'
assert score_move(board, 'My move: e2e4', 'e2e4')[0] == 'unparseable'
assert score_move(board, '', 'e2e4')[0] == 'unparseable'
board.push_uci('e2e4')
assert score_move(board, 'e7e5', 'e7e5')[0] == 'correct'
promotion = chess.Board('7k/P7/8/8/8/8/8/7K w - - 0 1')
assert score_move(promotion, 'a7a8q', 'a7a8q')[0] == 'correct'
print('Scoring checks passed: correct, wrong, illegal, formatting, side-to-move, promotion.')

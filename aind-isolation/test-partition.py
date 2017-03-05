import random
import unittest
import timeit
import sys

import isolation
import game_agent

from collections import Counter
from copy import deepcopy
from copy import copy
from functools import wraps
from queue import Queue
from threading import Thread
from multiprocessing import TimeoutError
from queue import Empty as QueueEmptyError
from importlib import reload




def CreateBoard():
	test_depth = 1
	adversary_location = (0, 0)  # top left corner
	iterative_search = False
	search_method = "minimax"
	heuristic = lambda g, p: 0.  # return 0 everywhere

        # create a player agent & a game board
	agentUT = game_agent.CustomPlayer(test_depth, heuristic, iterative_search, search_method)
	agentUT2 = game_agent.CustomPlayer(test_depth, heuristic, iterative_search, search_method)
	return isolation.Board(agentUT, agentUT2),agentUT

def AddPartitionRow(board):
	board.apply_move((3,0))
	board.apply_move((3,6))
	board.apply_move((3,1))
	board.apply_move((3,5))
	board.apply_move((3,2))
	board.apply_move((3,4))
	board.apply_move((3,3))
	board.apply_move((2,4))
	board.apply_move((4,3))
def AddPartitionRowWin(board):
	board.apply_move((2,0))
	board.apply_move((2,6))
def AddPartitionRowLost(board):
	board.apply_move((4,0))
	board.apply_move((4,6))
def AddPartitionRowSameSide(board):
	board.apply_move((3,0))
	board.apply_move((3,6))
	board.apply_move((3,1))
	board.apply_move((3,5))
	board.apply_move((3,2))
	board.apply_move((3,4))
	board.apply_move((3,3))
	board.apply_move((4,4))
	board.apply_move((4,3))

def AddPartitionColumn(board):
	board.apply_move((0,3))
	board.apply_move((6,3))
	board.apply_move((1,3))
	board.apply_move((5,3))
	board.apply_move((2,3))
	board.apply_move((4,3))
	board.apply_move((3,3))
	board.apply_move((4,4))
	board.apply_move((3,2))
def AddPartitionColumnWin(board):
	board.apply_move((0,4))
	board.apply_move((6,4))
def AddPartitionColumnLost(board):
	board.apply_move((0,2))
	board.apply_move((6,2))
def AddPartitionColumnSameSide(board):
	board.apply_move((0,3))
	board.apply_move((6,3))
	board.apply_move((1,3))
	board.apply_move((5,3))
	board.apply_move((2,3))
	board.apply_move((4,3))
	board.apply_move((3,3))
	board.apply_move((4,4))
	board.apply_move((3,4))


def TestPartitionRow():
	board,player=CreateBoard()
	AddPartitionRow(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if not existe:
		print("Fail test TestPartitionRow")
		return False
	if result!=0:
		print("Fail test TestPartitionRow result:" + str(result))
		return False
	return True
def TestPartitionRowWin():
	board,player=CreateBoard()
	AddPartitionRowWin(board)
	AddPartitionRow(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if not existe:
		print("Fail test TestPartitionRowWin")
		return False
	if result<=0:
		print("Fail test TestPartitionRowWin result:" + str(result))
		return False
	return True
def TestPartitionRowLost():
	board,player=CreateBoard()
	AddPartitionRowLost(board)
	AddPartitionRow(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if not existe:
		print("Fail test TestPartitionRowLost")
		return False
	if result>=0:
		print("Fail test TestPartitionRowLost result:" + str(result))
		return False
	return True
def TestPartitionRowSameSide():
	board,player=CreateBoard()
	AddPartitionRowSameSide(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if existe:
		print("Fail test TestPartitionRowSameSide")
		return False
	return True
def TestPartitionColumn():
	board,player=CreateBoard()
	AddPartitionColumn(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if not existe:
		print("Fail test TestPartitionColumn")
		return False
	if result!=0:
		print("Fail test TestPartitionColumn result:" + str(result))
		return False
	return True
def TestPartitionColumnWin():
	board,player=CreateBoard()
	AddPartitionColumnWin(board)
	AddPartitionColumn(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if not existe:
		print("Fail test TestPartitionColumnWin")
		return False
	if result<=0:
		print("Fail test TestPartitionRColumnWin result:" + str(result))
		return False
	return True
def TestPartitionColumnLost():
	board,player=CreateBoard()
	AddPartitionColumnLost(board)
	AddPartitionColumn(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if not existe:
		print("Fail test TestPartitionColumnLost")
		return False
	if result>=0:
		print("Fail test TestPartitionRColumnLost result:" + str(result))
		return False
	return True
def TestPartitionColumnSameSide():
	board,player=CreateBoard()
	AddPartitionColumnSameSide(board)
	print(board.to_string())
	existe,result=CheckPartition(board,player)
	if  existe:
		print("Fail test TestPartitionColumnSameSide")
		return False
	return True





def CheckPartition(board,player):
	blank=board.get_blank_spaces()
	for r in range(board.height):
		if all( (r,c) not in blank for c in range(board.width)):
			print("Fila: " + str(r) + " E partition")
			(r_player,c_player)=board.get_player_location(player)
			(r_opponent,c_opponent)=board.get_player_location(board.get_opponent(player))
			if (r_player>r) and (r_opponent<r):
					print("Fila: " + str(r) + " E partition con componentes separados maior")
					result=sum( 1 for (r_b,c_b) in blank if r_b>r) - sum( 1 for (r_b,c_b) in blank if r_b<r)
					return True,result;
			if (r_player<r) and (r_opponent>r):
					print("Fila: " + str(r) + " E partition con componentes separados menor")
					result=sum( 1 for (r_b,c_b) in blank if r_b<r) - sum( 1 for (r_b,c_b) in blank if r_b>r)
					return True,result;
	for c in range(board.width):
		if all( (r,c) not in blank for r in range(board.height)):
			print("Column: " + str(c) + " E partition")
			(r_player,c_player)=board.get_player_location(player)
			(r_opponent,c_opponent)=board.get_player_location(board.get_opponent(player))
			if (c_player>c) and  (c_opponent<c):
					print("Column: " + str(c) + " E partition con componentes separados")
					result=sum( 1 for (r_b,c_b) in blank if c_b>c) - sum( 1 for (r_b,c_b) in blank if c_b<c)
					return True,result;
			if (c_player<c) and (c_opponent>c):
					print("Column: " + str(c) + " E partition con componentes separados")
					result=sum( 1 for (r_b,c_b) in blank if c_b<c) - sum( 1 for (r_b,c_b) in blank if c_b>c)
					return True,result;
	return False,0



def TestSimetry():
	board,player=CreateBoard()
	board.apply_move((0,3))
	if CheckSimetry(board,player,2)==2:
		print("TestSimetry fallo 1")
		return False
	board.apply_move((3,3))
	if CheckSimetry(board,player,2)==2:
		print("TestSimetry fallo 2")
		return False
	board.apply_move((1,0))
	board.apply_move((6,6))
	board.apply_move((0,0))
	if CheckSimetry(board,player,2)!=2:
		print("TestSimetry fallo 3")
		return False
	return True

def CheckSimetry(board,player,acc):
	if board.move_count<2:
		return 0
	if (player==board.inactive_player):
		if (board.width%2==1) and (board.height%2==1):
			r_center=board.height//2
			c_center=board.height//2
			(r_player,c_player)=board.get_player_location(player)
			(r_opponent,c_opponent)=board.get_player_location(board.get_opponent(player))
			if ((r_player-r_center)==(r_center-r_opponent)) and ((c_player-c_center)==(c_center-c_opponent)):
				return acc
	return 0

def TestCenter():
	board,player=CreateBoard()
	board.apply_move((0,3))
	board.apply_move((3,3))
	print(custom_score_center(board, player))
	board.apply_move((6,6))
	print(custom_score_center(board, player))
	board.apply_move((2,2))
	board.apply_move((4,4))
	print(custom_score_center(board, player))
	board.apply_move((0,6))
	print(custom_score_center(board, player))

def custom_score_center(game, player,coef_my=1,coef_other=1):
    (r_player,c_player)=game.get_player_location(player)
    (r_opponent,c_opponent)=game.get_player_location(game.get_opponent(player))
    centrado_player=min(r_player,game.height-1-r_player) + min(c_player, game.width-1-c_player )
    centrado_opossite=min(r_opponent,game.height-1-r_opponent ) + min(c_opponent,game.width-1-c_opponent )
    print (str((r_player,c_player)) + "vs" + str((r_opponent,c_opponent)) + "   " +
    	str(centrado_player) + "-" + str(centrado_opossite) + "-->" )
    return float(coef_my * centrado_player-coef_other *centrado_opossite)

def free_side(game,player):
	(r_player,c_player)=game.get_player_location(player)
	(r_opponent,c_opponent)=game.get_player_location(game.get_opponent(player))
	directions = [(-1, -1), (-1, 0), (0, -1), (-1, 1),(0,1),(1,0),(1,1),(1,-1)]
	valid_moves_player = [(r_player+dr,c_player+dc) for dr, dc in directions if game.move_is_legal((r_player+dr,c_player+dc))]
	valid_moves_opponent = [(r_opponent+dr,c_opponent+dc) for dr, dc in directions if game.move_is_legal((r_opponent+dr,c_opponent+dc))]
	print((r_player,c_player))
	print(valid_moves_player)
	print((r_opponent,c_opponent))
	print(valid_moves_opponent )
	return float(len(valid_moves_player) - len(valid_moves_opponent))
def TestFree():
	board,player=CreateBoard()
	board.apply_move((0,3))
	board.apply_move((3,3))
	print(board.to_string())
	print(free_side(board, player))
	board.apply_move((6,6))
	print(board.to_string())
	print(free_side(board, player))
	board.apply_move((2,2))
	board.apply_move((4,4))
	print(board.to_string())
	print(free_side(board, player))
	board.apply_move((0,6))
	print(board.to_string())
	print(free_side(board, player))


test_past=True
if not TestPartitionRow():
	test_past=False
if not TestPartitionRowWin():
	test_past=False
if not TestPartitionRowLost():
	test_past=False
if not TestPartitionRowSameSide():
	test_past=False
if not TestPartitionColumn():
	test_past=False
if not TestPartitionColumnWin():
	test_past=False
if not TestPartitionColumnLost():
	test_past=False
if not TestPartitionColumnSameSide():
	test_past=False
if not TestSimetry():
	test_past=False
if test_past:
	print("Pasados todos os test")
TestCenter()
TestFree()


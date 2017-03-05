"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math
import sys

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """
    First get player score and the compare
    player score=Number of possible moves for player +
                coef * Distance to the edge of the board for player +
                coef * Free  positions empy arround player
    We employ a coef = 2/3 for the opponent
    My best score
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    return custom_eval_player(game,player,1) - 2/3 * custom_eval_player(game,game.get_opponent(player),1)

def custom_score_1(game, player):
    """
    3 Board measure:
        E1.-Number of possible moves for the player minus  Number of possible moves for opponent
        E2.-Distance to the edge of the board for the player minus Distance to the edge of the board for the opponent.
        E3.-Free  positions arround player  minus Free  positions arround opponent
    E1 with coef = 2
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    return 2 *  custom_score_moves(game, player) +  custom_score_center(game, player) +custom_score_free_side(game,player)
def custom_score_2(game, player):
    """
    3 Board measure:
        E1.-Number of possible moves for the player minus  Number of possible moves for opponent
        E2.-Distance to the edge of the board for the player minus Distance to the edge of the board for the opponent.
        E3.-Free  positions arround player  minus Free  positions arround opponent
    percent_moves = (Move_max - move done) / Move Max
    score= E1 +  percent_moves * E2 + percent_moves * E3
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    p=percent_moves(game)
    return custom_score_moves(game, player) + p* custom_score_center(game, player) +custom_score_free_side(game,player)
def custom_score_3(game, player):
    """
    3 Board measure:
        E1.-Number of possible moves for the player minus  Number of possible moves for opponent
        E2.-Distance to the edge of the board for the player minus Distance to the edge of the board for the opponent.
        E3.-Free  positions arround player  minus Free  positions arround opponent
    percent_moves = (Move_max - move done) / Move Max
    score= E1 +  1/percent_moves * E2 + percent_moves * E3
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    p=percent_moves(game)
    return custom_score_moves(game, player) + 1/p* custom_score_center(game, player) + p *custom_score_free_side(game,player)
def custom_score_4(game, player):
    """
    3 Board measure:
        E1.-Number of possible moves for the player minus  Number of possible moves for opponent
        E2.-Distance to the edge of the board for the player minus Distance to the edge of the board for the opponent.
        E3.-Free  positions arround player  minus Free  positions arround opponent
    percent_moves = (Move_max - move done) / Move Max
    score= E1 +  0.5/percent_moves * E2 + 0.5 * percent_moves * E3
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    p=percent_moves(game)
    return custom_score_moves(game, player) +  0.5/p* custom_score_center(game, player) + 0.5 * p *custom_score_free_side(game,player)




def percent_moves(game):
    #percent_moves = (Move_max - move done) / Move Max
    moves_max=game.width * game.height
    moves_done=game.move_count;
    return float((moves_max-moves_done)/moves_max)

def custom_score_moves(game, player):
    #E1.-Number of possible moves for the player minus  Number of possible moves for opponent
    own_moves = len( game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves )

def custom_score_center(game, player):
    #E2.-Distance to the edge of the board for the player minus Distance to the edge of the board for the opponent.
    (r_player,c_player)=game.get_player_location(player)
    (r_opponent,c_opponent)=game.get_player_location(game.get_opponent(player))
    #Get Distance
    centrado_player=min(r_player,game.height-1-r_player) + min(c_player, game.width-1-c_player )
    centrado_opossite=min(r_opponent,game.height-1-r_opponent ) + min(c_opponent,game.width-1-c_opponent )
    return float(centrado_player-centrado_opossite)

def custom_score_free_side(game,player):
    #E3.-Free  positions arround player  minus Free  positions arround opponent
    (r_player,c_player)=game.get_player_location(player)
    (r_opponent,c_opponent)=game.get_player_location(game.get_opponent(player))
    directions = [(-1, -1), (-1, 0), (0, -1), (-1, 1),(0,1),(1,0),(1,1),(1,-1)]
    valid_moves_player = [(r_player+dr,c_player+dc) for dr, dc in directions if game.move_is_legal((r_player+dr,c_player+dc))]
    valid_moves_opponent = [(r_opponent+dr,c_opponent+dc) for dr, dc in directions if game.move_is_legal((r_opponent+dr,c_opponent+dc))]
    return float(len(valid_moves_player) - len(valid_moves_opponent))

def custom_eval_player(game,player,p):
    """
    player score=Number of possible moves for player +
                coef * Distance to the edge of the board border for player +
                coef * Free  positions arround player
    """
    own_moves = len( game.get_legal_moves(player))
    (r_player,c_player)=game.get_player_location(player)
    centrado_player=min(r_player,game.height-1-r_player) + min(c_player, game.width-1-c_player )
    directions = [(-1, -1), (-1, 0), (0, -1), (-1, 1),(0,1),(1,0),(1,1),(1,-1)]
    valid_moves_player = [(r_player+dr,c_player+dc) for dr, dc in directions if game.move_is_legal((r_player+dr,c_player+dc))]
    return float(own_moves + p * centrado_player + p * len(valid_moves_player) )

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if len(legal_moves)==0:
            return (-1,-1)
        depth=0
        score=0
        move_max=(-1,-1)
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            #print("Entrado tray")
            if self.iterative:
                for d in range(1,sys.maxsize):
                    if self.time_left()<=self.TIMER_THRESHOLD :
                        # No more time, return
                         return move_max
                    depth=d
                    if self.method=='minimax':
                        score_new,move_new=self.minimax(game, depth)
                    else:
                        score_new,move_new=self.alphabeta(game,depth)
                    if move_new==(-1,-1):
                        # No more move, return
                        return move_max
                    if (score_new>=score) :
                        # We get best score, update
                        score=score_new
                        move_max=move_new
            else:
                if self.method=='minimax':
                    score,move=self.minimax(game, self.search_depth)
                else:
                    score,move=self.alphabeta(game,self.search_depth)
                return move
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return move_max
        # Return the best move from the last completed search iteration
        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            # No more time, return
            raise Timeout()
        move_max=(-1,-1)
        legal_moves=game.get_legal_moves()
        if len(legal_moves)==0 or depth==0:
            #No more move
            return self.score(game,self),(-1,-1)
        if maximizing_player:
            score=-math.inf
            for move in legal_moves:
                new_game = game.forecast_move(move)
                if (depth==1) :
                     # Last level, get score
                    new_score=self.score(new_game,self)
                else:
                    # For this move test the next level
                    new_score,move_2= self.minimax(new_game,depth=depth-1,maximizing_player=False)
                if (new_score>score):
                    # Best score, update
                   score=new_score
                   move_max=move
        else:
            score=math.inf
            for move in legal_moves:
                new_game = game.forecast_move(move)
                if (depth==1) :
                    # Last level, get score
                    new_score=self.score(new_game,self)
                else:
                    # For this move test the next level
                    new_score,move_2=self.minimax(new_game,depth=depth-1)
                if (new_score<score):
                    # Best score, update
                   score=new_score
                   move_max=move

        return score, move_max





    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            # No more time, return
            raise Timeout()
        move_max=(-1,-1)

        legal_moves=game.get_legal_moves()
        if len(legal_moves)==0 or depth==0:
            # No more move or last level
            return self.score(game,self),(-1,-1)
        if maximizing_player:
            v=-math.inf
            for move in legal_moves:
                new_game = game.forecast_move(move)
                if (depth==1):
                    #Last level, get value
                    new_score=self.score(new_game,self)
                else:
                    #For this movement test next level
                    new_score,move_2= self.alphabeta(new_game,depth=depth-1,maximizing_player=False,alpha=alpha,beta=beta)
                if (new_score>v):
                    v=new_score
                    move_max=move
                if v>=beta:
                    # Imposible to get a best solution,finish
                    return float(v),move_max
                alpha=max(alpha,v)
        else:
            v=math.inf
            for move in legal_moves:
                new_game = game.forecast_move(move)
                if (depth==1):
                    #Last level, get value
                    new_score=self.score(new_game,self)
                else:
                    #For this movement test next level
                    new_score,move_2=self.alphabeta(new_game,depth=depth-1,alpha=alpha,beta=beta)
                if (new_score<v):
                   v=new_score
                   move_max=move
                if v<=alpha:
                    # Imposible to get a best solution,finish
                    return float(v),move_max
                beta=min(beta,v)
        return float(v),move_max


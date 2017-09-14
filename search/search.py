# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

 

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  from game import Directions
  from util import Stack

  class node:  
    def __init__(self,state,parent_state,action,score,posible_transitions):
      self.state=state
      self.parent_state=parent_state
      self.action=action
      self.score=score
      self.posible_transitions=posible_transitions 
  new_node=node(problem.getStartState(),None,None,0,problem.getSuccessors(problem.getStartState()))
  pila =Stack();
  pila.push(new_node);
  explored=[];
  explored.append(new_node.state);
  while (pila.isEmpty()==False):
    working_node=pila.pop()
    print("Working " + str(working_node.state) + " " + str(working_node.action) + " " + str(working_node.posible_transitions ))
    while len(working_node.posible_transitions)>0:
      (state,action,score)=working_node.posible_transitions[0];
      working_node.posible_transitions=working_node.posible_transitions[1:];
      if (problem.isGoalState(state)):
        print "Alcanzado Goal:" +  str(state);
        retorno=[];
        retorno.append(action)
        retorno.append(working_node.action);
        while (pila.isEmpty()==False):
          working_node=pila.pop();
          if (working_node.action!=None):
            retorno.append(working_node.action)
        print("N accions:" + str(len(retorno)))    
        retorno=list(reversed(retorno))
        print(len(retorno))
        return  retorno;
      print("New state" + str(state) +"-->"+ action)
      if (state not in explored):
        print("New node" + str(state) +"-->"+ action)
        new_node=node(state,working_node.state,action,working_node.score+ score,problem.getSuccessors(state))
        pila.push(working_node);
        pila.push(new_node);
        explored.append(new_node.state);
        break;
  print "Finish bucle";

  return  []

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  from game import Directions
  from util import PriorityQueue
  class node:  
    def __init__(self,state,parent,action,score,posible_transitions):
      self.state=state
      self.parent=parent
      self.action=action
      self.score=score
      self.posible_transitions=posible_transitions
  def is_in_explored(state):
    for n in explored:
      if n.state==state:
        return True;
    return False;

  def return_solution(node):
    lst_actions=[]
    working_node=node;
    while working_node!=None:
      if working_node.action!=None:
        lst_actions.append(working_node.action);
      working_node=working_node.parent;
    print("Len Solucion:"  + str(len(lst_actions)))
    print(lst_actions)
    return list(reversed(lst_actions))

  frontier=PriorityQueue();  
  new_node=node(problem.getStartState(),None,None,0,problem.getSuccessors(problem.getStartState()))
  frontier.push(new_node,0);
  explored=[];
  while (frontier.isEmpty()==False):
    working_node=frontier.pop()
    explored.append(working_node)
    print("Working " + str(working_node.state) + " " + str(working_node.action) + " " + str(working_node.posible_transitions ))
    if (problem.isGoalState(working_node.state)):
        print "Alcanzado Goal:" +  str(state);
        return return_solution(working_node)
    while len(working_node.posible_transitions)>0:
      (state,action,score)=working_node.posible_transitions[0];
      working_node.posible_transitions=working_node.posible_transitions[1:];
      print("New state" + str(state) +"-->"+ action)
      if is_in_explored(state)==False:
        print("New node" + str(state) +"-->"+ action)
        new_node=node(state,working_node,action,working_node.score+ score,problem.getSuccessors(state))
        frontier.push(new_node,working_node.score+ 1);
  print "Finish bucle";

  return  []

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  from game import Directions
  from util import PriorityQueue
  class node:  
    def __init__(self,state,parent,action,score,posible_transitions):
      self.state=state
      self.parent=parent
      self.action=action
      self.score=score
      self.posible_transitions=posible_transitions
  def is_in_explored(state):
    for n in explored:
      if n.state==state:
        return True;
    return False;

  def return_solution(node):
    lst_actions=[]
    working_node=node;
    while working_node!=None:
      if working_node.action!=None:
        lst_actions.append(working_node.action);
      working_node=working_node.parent;
    print("Len Solucion:"  + str(len(lst_actions)))
    print(lst_actions)
    return list(reversed(lst_actions))
  frontier=PriorityQueue();  
  new_node=node(problem.getStartState(),None,None,0,problem.getSuccessors(problem.getStartState()))
  frontier.push(new_node,0);
  explored=[];
  while (frontier.isEmpty()==False):
    working_node=frontier.pop()
    explored.append(working_node)
    print("Working " + str(working_node.state) + " " + str(working_node.action) + " " + str(working_node.posible_transitions ))
    if (problem.isGoalState(working_node.state)):
        print "Alcanzado Goal:" +  str(state);
        return return_solution(working_node)
    while len(working_node.posible_transitions)>0:
      (state,action,score)=working_node.posible_transitions[0];
      working_node.posible_transitions=working_node.posible_transitions[1:];
      print("New state" + str(state) +"-->"+ action)
      if is_in_explored(state)==False:
        print("New node" + str(state) +"-->"+ action)
        new_node=node(state,working_node,action,working_node.score+ score,problem.getSuccessors(state))
        frontier.push(new_node,working_node.score+ score);
  print "Finish bucle";

  return  []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

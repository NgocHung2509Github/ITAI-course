# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    visited = set()
    # let visited hold set of traversed positions {(x,y),...}
    stack = util.Stack()
    # stack contains [(position(x,y),[path]),...] -> (a list of tuples)
    stack.push((problem.getStartState(), []))  # getStartState() return (x, y) of the start state

    while not stack.isEmpty():
        pos, path = stack.pop()  # pop() return the most current item in stack
        # let pos be the current position and path is the path from start state to current

        # check if the popped node is visited
        if pos not in visited:
            visited.add(pos)
            # add the popped node to the visited set

            # if the popped node is the goal, return its path
            if problem.isGoalState(pos):
                return path

            # if not the goal, find its successors and push to the stack
            successors = problem.getSuccessors(pos)  # a list contains ((x, y), [path], pathCost)
            for node in successors:
                if node[0] not in visited:
                    stack.push((node[0], path + [node[1]]))

    # if failed to find path to the goal, return an empty list
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # same with dfs but use queue
    visited = set()
    queue = util.Queue()
    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():

        pos, path = queue.pop()

        if pos not in visited:
            visited.add(pos)

            if problem.isGoalState(pos):
                return path

            successors = problem.getSuccessors(pos)
            for node in successors:
                if node[0] not in visited:
                    queue.push((node[0], path + [node[1]]))

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Pr_q = util.PriorityQueue()
    visited = dict()
    state = problem.getStartState()
    nd = {}
    nd["pred"] = None
    nd["act"] = None
    nd["state"] = state
    nd["cost"] = 0
    Pr_q.push(nd, nd["cost"])

    while not Pr_q.isEmpty():
        nd = Pr_q.pop()
        state = nd["state"]
        cost = nd["cost"]

        if state in visited:
            continue
        visited[state] = True
        if problem.isGoalState(state):
            break
        for suc in problem.getSuccessors(state):
            if suc[0] not in visited:
                new_nd = {}
                new_nd["pred"] = nd
                new_nd["state"] = suc[0]
                new_nd["act"] = suc[1]
                new_nd["cost"] = suc[2] + cost
                Pr_q.push(new_nd, new_nd["cost"])
    actions = []
    while nd["act"] is not None:
        actions.insert(0, nd["act"])
        nd = nd["pred"]
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Pr_q = util.PriorityQueue()
    visited = dict()

    state = problem.getStartState()
    nd = {}
    nd["pred"] = None
    nd["act"] = None
    nd["state"] = state
    nd["cost"] = 0
    nd["eq"] = heuristic(state, problem)
    Pr_q.push(nd, nd["cost"] + nd["eq"])

    while not Pr_q.isEmpty():
        nd = Pr_q.pop()
        state = nd["state"]
        cost = nd["cost"]
        v = nd["eq"]

        if state in visited:
            continue
        visited[state] = True
        if problem.isGoalState(state):
            break
        for suc in problem.getSuccessors(state):
            if suc[0] not in visited:
                new_nd = {}
                new_nd["pred"] = nd
                new_nd["state"] = suc[0]
                new_nd["act"] = suc[1]
                new_nd["cost"] = suc[2] + cost
                new_nd["eq"] = heuristic(new_nd["state"], problem)
                Pr_q.push(new_nd, new_nd["cost"] + new_nd["eq"])
    actions = []
    while nd["act"] is not None:
        actions.insert(0, nd["act"])
        nd = nd["pred"]
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

def q1a_solver(problem: q1a_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

class AStarData:
    # YOUR CODE HERE
    def __init__(self, problem: q1a_problem):
        self.frontier = util.PriorityQueue()
        self.explored = set()
        self.start_state = problem.getStartState()
        self.goal = problem.startingGameState.getFood().asList()[0]


def astar_initialise(problem: q1a_problem):
    # YOUR CODE HERE
    astarData = AStarData(problem)
    heuristic_cost = astar_heuristic(astarData.start_state, astarData.goal)
    astarData.frontier.push((astarData.start_state, [], 0), heuristic_cost)
    return astarData

def astar_loop_body(problem: q1a_problem, astarData: AStarData):
    # YOUR CODE HERE
    if astarData.frontier.isEmpty():
        return True, []
    current_state, actions, current_cost = astarData.frontier.pop()

    if current_state in astarData.explored:
        return False, None
    astarData.explored.add(current_state)

    if problem.isGoalState(current_state):
        return True, actions

    for successor, action, step_cost in problem.getSuccessors(current_state):
        if successor not in astarData.explored:
            new_cost = current_cost + step_cost  # g(n)
            heuristic_cost = astar_heuristic(successor, astarData.goal)  # h(n)
            total_cost = new_cost + heuristic_cost  # f(n)

            new_actions = actions + [action]

            astarData.frontier.push((successor, new_actions, new_cost), total_cost)

    return False, None

def astar_heuristic(current, goal):
    # YOUR CODE HERE
    if goal is None:
        return 0
    return abs(goal[0] - current[0]) + abs(goal[1] - current[1])
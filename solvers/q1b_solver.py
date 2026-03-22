#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
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
    def __init__(self, problem: q1b_problem):
        self.frontier = util.PriorityQueue()
        self.explored = set()
        self.start_state = problem.getStartState()
        self.goals = problem.startingGameState.getFood().asList()
        self.selected_goal = self.select_bestGoal(problem)
        self.cost_so_far = {self.start_state: 0}

    def bfs_shortest_path(self, problem, start_pos, target_foods):
        queue = [(start_pos, 0)]
        visited = set()
        visited.add(start_pos)
        while queue:
            pos, cost = queue.pop(0)
            if pos in target_foods:
                return cost
            for successor, _, step_cost in problem.getSuccessors(pos):
                if successor not in visited:
                    visited.add(successor)
                    queue.append((successor, cost + step_cost))
        return -1

    def select_bestGoal(self, problem):
        if not self.goals:
            return None
        distances = {}
        for food in self.goals:
            cost = self.bfs_shortest_path(problem, self.start_state, {food})
            if cost != -1:
                distances[food] = cost
        if not distances:
            return None
        return min(distances, key=lambda x: distances[x])

def astar_initialise(problem: q1b_problem):
    # YOUR CODE HERE
    # astarData = AStarData(problem)
    # heuristic_cost = astar_heuristic(astarData.start_state, astarData.goals)
    # astarData.frontier.push((astarData.start_state, [], 0), heuristic_cost)
    # return astarData
    astarData = AStarData(problem)
    if astarData.selected_goal is None:
        return astarData
    heuristic_cost = astar_heuristic(astarData.start_state, [astarData.selected_goal])
    astarData.frontier.push((astarData.start_state, [], 0), heuristic_cost)
    return astarData

def astar_loop_body(problem: q1b_problem, astarData: AStarData):
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
        if successor in astarData.explored:
            continue
        new_cost = current_cost + step_cost
        if successor not in astarData.cost_so_far or new_cost < astarData.cost_so_far[successor]:
            astarData.cost_so_far[successor] = new_cost
            heuristic_cost = astar_heuristic(successor, [astarData.selected_goal])
            total_cost = new_cost + heuristic_cost
            new_actions = actions + [action]
            astarData.frontier.push((successor, new_actions, new_cost), total_cost)

    return False, None

def astar_heuristic(current, goals):
    # YOUR CODE HERE
    # return 0
    if not goals:
        return 0
    distance = min(abs(goal[0] - current[0]) + abs(goal[1] - current[1]) for goal in goals)
    k = 10
    distance_factor = k * distance
    return distance + distance_factor
    # return min(abs(goal[0] - current[0]) + abs(goal[1] - current[1]) for goal in goals)
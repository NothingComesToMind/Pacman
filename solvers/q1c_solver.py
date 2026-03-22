#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    # YOUR CODE HERE
    start_pos, all_food = problem.getStartState()
    reachable_food = find_reachable_foods(problem, start_pos, all_food)
    if not reachable_food:
        print("No reachable food dots found.")
        return []
    problem.getStartState = lambda: (start_pos, tuple(reachable_food))
    print(f"Found {len(reachable_food)} reachable food dots out of {len(all_food)} total.")
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False

    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f"Number of node expansions: {num_expansions}")
    return result


class AStarData:

    def __init__(self, problem: q1c_problem):
        self.frontier = util.PriorityQueue()
        self.visited_cost = {}
        self.start_state = problem.getStartState()


def astar_initialise(problem: q1c_problem):
    astarData = AStarData(problem)
    pacman_position, food_positions = astarData.start_state
    heuristic_cost = astar_heuristic(pacman_position, food_positions)
    astarData.frontier.push((astarData.start_state, [], 0), heuristic_cost)
    return astarData


def astar_loop_body(problem: q1c_problem, astarData: AStarData):
    if astarData.frontier.isEmpty():
        return True, []

    (pacman_position, remaining_food), actions, current_cost = astarData.frontier.pop()

    state_key = (pacman_position, frozenset(remaining_food))
    if state_key in astarData.visited_cost and astarData.visited_cost[state_key] <= current_cost:
        return False, None
    astarData.visited_cost[state_key] = current_cost

    if not remaining_food:
        return True, actions

    for (successor, new_food_list), action, step_cost in problem.getSuccessors((pacman_position, remaining_food)):
        new_cost = current_cost + step_cost
        heuristic_cost = astar_heuristic(successor, new_food_list)
        total_cost = new_cost + heuristic_cost

        new_state_key = (successor, frozenset(new_food_list))
        if new_state_key not in astarData.visited_cost or total_cost < astarData.visited_cost.get(new_state_key,
                                                                                                  float('inf')):
            new_actions = actions + [action]
            astarData.frontier.push(((successor, new_food_list), new_actions, new_cost), total_cost)

    return False, None


def astar_heuristic(current, food_list):
    if not food_list:
        return 0
    distances = [abs(current[0] - food[0]) + abs(current[1] - food[1]) for food in food_list]
    max_distance = max(distances) if distances else 0

    if len(food_list) < 10:
        k = 2
    elif 30 > len(food_list) >= 10:
        k = 8
    elif 100 > len(food_list) >= 30:
        k = 10
    elif 200 > len(food_list) >= 100:
        k = 50
    else:
        k = 90
    food_count_penalty = len(food_list) * k
    return max_distance + food_count_penalty


def find_reachable_foods(problem, start_pos, all_food):

    food_set = set(all_food)
    reachable_food = []
    queue = [(start_pos, 0)]
    visited = set()
    walls = problem.startingGameState.getWalls()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        pos, cost = queue.pop(0)
        if pos in visited:
            continue
        visited.add(pos)

        if pos in food_set:
            reachable_food.append(pos)
            if len(reachable_food) == len(food_set):
                break

        for dx, dy in directions:
            next_x, next_y = int(pos[0] + dx), int(pos[1] + dy)
            if not walls[next_x][next_y]:
                queue.append(((next_x, next_y), cost + 1))

    return reachable_food

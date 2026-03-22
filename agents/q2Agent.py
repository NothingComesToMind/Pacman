import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"

        def evaluate_state(game_state):
            pacman_loc = game_state.getPacmanPosition()
            food_grid = game_state.getFood()
            ghost_data = game_state.getGhostStates()
            inf = 100000000.0
            FOOD_SCORE = 10.0
            GHOST_PENALTY = -10.0
            SCARED_GHOST_BONUS = 100.0
            total_score = game_state.getScore()
            food_positions = food_grid.asList()
            if food_positions:
                food_distances = [(pos, manhattanDistance(pacman_loc, pos)) for pos in food_positions]
                food_distances.sort(key=lambda x: x[1])
                closest_food = food_distances[0][1]
                total_score += FOOD_SCORE / (closest_food + 1e-6)
            else:
                total_score += FOOD_SCORE

            # ghost_scared_durations = [ghost.scaredTimer for ghost in ghost_data]
            # closest_ghost_dist = min([manhattanDistance(pacman_loc, ghost.configuration.pos) for ghost in ghost_data])
            # ghost_risk = -10 / closest_ghost_dist if closest_ghost_dist != 0 else 0
            # scared_time_sum = sum(ghost_scared_durations)

            for ghost in ghost_data:
                dist_to_ghost = manhattanDistance(pacman_loc, ghost.getPosition())
                if dist_to_ghost == 0:
                    return -inf
                else:
                    if ghost.scaredTimer > 0:
                        total_score += SCARED_GHOST_BONUS / dist_to_ghost
                    else:
                        total_score += GHOST_PENALTY / dist_to_ghost

            return total_score

        def alpha_beta(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose():
                return evaluate_state(state)
            if depth >= self.depth - 1:
                return evaluate_state(state)


            num_agents = state.getNumAgents()
            next_agent = (agentIndex + 1) % num_agents
            next_depth = depth if next_agent != 0 else depth + 1

            legal_actions = state.getLegalActions(agentIndex)
            if not legal_actions:
                return evaluate_state(state)

            if agentIndex == 0:
                value = -float('inf')
                for action in legal_actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, alpha_beta(successor, next_depth, next_agent, alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value

            else:
                value = float('inf')
                for action in legal_actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = min(value, alpha_beta(successor, next_depth, next_agent, alpha, beta))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return value



        best_action = None
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        legal_actions = gameState.getLegalActions(0)
        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            value = alpha_beta(successor, depth=0, agentIndex=1, alpha=alpha, beta=beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)

        return best_action if best_action is not None else Directions.STOP



